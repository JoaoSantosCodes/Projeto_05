import os
import time
import subprocess
from datetime import datetime
import logging
import sys
import yaml
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_update.log'),
        logging.StreamHandler()
    ]
)

def load_config():
    """Carrega as configurações do arquivo YAML"""
    try:
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Erro ao carregar configurações: {str(e)}")
        return None

def send_email_notification(subject, message, config):
    """Envia notificação por e-mail"""
    if not config['notifications']['email']['enabled']:
        return

    # Verifica se as configurações necessárias estão presentes
    required_configs = [
        'sender_email',
        'recipient_email',
        'smtp_server',
        'smtp_port'
    ]
    
    missing_configs = [cfg for cfg in required_configs 
                      if not config['notifications']['email'].get(cfg)]
    
    if missing_configs:
        logging.error(f"Configurações de e-mail incompletas. Faltando: {', '.join(missing_configs)}")
        return

    # Verifica se as variáveis de ambiente estão definidas
    email_user = os.getenv('EMAIL_USER')
    email_password = os.getenv('EMAIL_PASSWORD')
    
    if not email_user or not email_password:
        logging.error("Variáveis de ambiente EMAIL_USER e/ou EMAIL_PASSWORD não definidas")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = config['notifications']['email']['sender_email']
        msg['To'] = config['notifications']['email']['recipient_email']
        msg['Subject'] = f"{config['notifications']['email']['subject_prefix']} {subject}"
        
        msg.attach(MIMEText(message, 'plain'))
        
        with smtplib.SMTP(config['notifications']['email']['smtp_server'], 
                         config['notifications']['email']['smtp_port']) as server:
            server.starttls()
            try:
                server.login(email_user, email_password)
            except smtplib.SMTPAuthenticationError:
                logging.error("Falha na autenticação SMTP. Verifique as credenciais.")
                return
            except Exception as e:
                logging.error(f"Erro ao autenticar no servidor SMTP: {str(e)}")
                return
                
            try:
                server.send_message(msg)
                logging.info("Notificação por e-mail enviada com sucesso")
            except Exception as e:
                logging.error(f"Erro ao enviar e-mail: {str(e)}")
                
    except Exception as e:
        logging.error(f"Erro ao configurar e-mail: {str(e)}")

def create_backup(config):
    """Cria um backup do diretório atual"""
    if not config['backup']['enabled']:
        return None

    try:
        backup_dir = config['backup']['directory']
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_path = os.path.join(backup_dir, backup_name)

        # Ignora diretórios que não devem ser incluídos no backup
        ignore = shutil.ignore_patterns(
            '.git', '.venv', '__pycache__', '*.pyc',
            '*.log', 'backups', 'node_modules'
        )

        shutil.copytree('.', backup_path, ignore=ignore)
        logging.info(f"Backup criado em: {backup_path}")

        # Remove backups antigos se exceder o limite
        backups = sorted([d for d in os.listdir(backup_dir) 
                         if os.path.isdir(os.path.join(backup_dir, d))])
        while len(backups) > config['backup']['max_backups']:
            old_backup = os.path.join(backup_dir, backups.pop(0))
            shutil.rmtree(old_backup)
            logging.info(f"Backup antigo removido: {old_backup}")

        return backup_path
    except Exception as e:
        logging.error(f"Erro ao criar backup: {str(e)}")
        return None

def run_command(command):
    """Executa um comando e retorna o resultado"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            logging.error(f"Comando falhou: {command}")
            logging.error(f"Erro: {result.stderr}")
            return None
        return result.stdout.strip()
    except Exception as e:
        logging.error(f"Erro ao executar comando '{command}': {str(e)}")
        return None

def check_changes():
    """Verifica se há mudanças no repositório"""
    status = run_command("git status --porcelain")
    if status is None:
        return False
    return bool(status)

def get_branch_name():
    """Obtém o nome da branch atual"""
    return run_command("git branch --show-current") or "main"

def commit_and_push(config):
    """Faz commit e push das alterações"""
    try:
        branch = get_branch_name()
        logging.info(f"Branch atual: {branch}")
        
        # Cria backup antes do commit
        backup_path = create_backup(config)
        
        # Adiciona todas as alterações
        run_command("git add .")
        
        # Cria mensagem de commit com timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Auto-update: {timestamp}"
        
        # Faz o commit
        run_command(f'git commit -m "{commit_message}"')
        
        # Faz o push
        run_command(f"git push origin {branch}")
        
        success_message = f"Atualização realizada com sucesso: {commit_message}"
        logging.info(success_message)
        
        # Envia notificação de sucesso
        if backup_path:
            success_message += f"\nBackup criado em: {backup_path}"
        send_email_notification("Atualização Concluída", success_message, config)
        
        return True
    except Exception as e:
        error_message = f"Erro ao fazer commit/push: {str(e)}"
        logging.error(error_message)
        send_email_notification("Erro na Atualização", error_message, config)
        return False

def main():
    """Loop principal do script"""
    config = load_config()
    if not config:
        logging.error("Não foi possível carregar as configurações. Encerrando...")
        return

    logging.info("="*50)
    logging.info("Iniciando script de atualização automática")
    logging.info(f"Diretório atual: {os.getcwd()}")
    logging.info(f"Python version: {sys.version}")
    logging.info(f"Configurações carregadas: {json.dumps(config, indent=2)}")
    logging.info("="*50)
    
    retry_count = 0
    while True:
        try:
            if check_changes():
                logging.info("Mudanças detectadas, realizando commit e push...")
                if commit_and_push(config):
                    retry_count = 0
                else:
                    retry_count += 1
                    if retry_count >= config['update']['max_retries']:
                        error_message = f"Máximo de tentativas ({config['update']['max_retries']}) excedido"
                        logging.error(error_message)
                        send_email_notification("Erro Crítico", error_message, config)
                        break
            else:
                logging.info("Nenhuma mudança detectada")
                retry_count = 0
            
            # Espera o intervalo configurado
            logging.info(f"Aguardando {config['update']['interval']} segundos para próxima verificação...")
            time.sleep(config['update']['interval'])
            
        except KeyboardInterrupt:
            logging.info("Script interrompido pelo usuário")
            break
        except Exception as e:
            error_message = f"Erro inesperado: {str(e)}"
            logging.error(error_message)
            send_email_notification("Erro Inesperado", error_message, config)
            time.sleep(config['update']['interval'])

if __name__ == "__main__":
    main() 