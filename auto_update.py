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
from logging.handlers import RotatingFileHandler
import hashlib
import argparse
from cryptography.fernet import Fernet
import git

# Função para configurar logging diário e log de erros
def setup_logging():
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(log_dir, f'auto_update_{today}.log')
    error_log_file = os.path.join(log_dir, 'auto_update_errors.log')

    # Logger principal
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers = []  # Limpa handlers antigos

    # Handler para log diário
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=7, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    # Handler para log de erros
    error_handler = RotatingFileHandler(error_log_file, maxBytes=2*1024*1024, backupCount=5, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(error_handler)

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)

setup_logging()

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

def hash_file(filepath):
    """Calcula o hash SHA256 de um arquivo."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def generate_backup_integrity(backup_path):
    """Gera um arquivo integrity.json com os hashes SHA256 de todos os arquivos do backup."""
    integrity = {}
    for root, dirs, files in os.walk(backup_path):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, backup_path)
            integrity[rel_path] = hash_file(file_path)
    integrity_file = os.path.join(backup_path, 'integrity.json')
    with open(integrity_file, 'w', encoding='utf-8') as f:
        json.dump(integrity, f, indent=2)
    logging.info(f"Arquivo de integridade gerado: {integrity_file}")

def get_encryption_key():
    """Obtém a chave de criptografia do ambiente ou de um arquivo."""
    key = os.getenv('BACKUP_ENCRYPTION_KEY')
    if key:
        return key.encode()
    key_file = 'backup.key'
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    return None

def encrypt_file(filepath, fernet):
    """Criptografa um arquivo usando Fernet."""
    with open(filepath, 'rb') as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    with open(filepath, 'wb') as f:
        f.write(encrypted)

def encrypt_backup(backup_path):
    """Criptografa todos os arquivos do backup, exceto integrity.json."""
    key = get_encryption_key()
    if not key:
        logging.info("Chave de criptografia não definida. Backup NÃO será criptografado.")
        return
    fernet = Fernet(key)
    for root, dirs, files in os.walk(backup_path):
        for file in files:
            if file == 'integrity.json':
                continue
            file_path = os.path.join(root, file)
            encrypt_file(file_path, fernet)
            logging.info(f"Arquivo criptografado: {file_path}")
    logging.info(f"Backup criptografado com sucesso: {backup_path}")

def create_backup(config):
    """Cria um backup do diretório atual, gera arquivo de integridade e criptografa se habilitado."""
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
        ignore = shutil.ignore_patterns(*config['backup'].get('ignore_patterns', []))

        shutil.copytree('.', backup_path, ignore=ignore)
        logging.info(f"Backup criado em: {backup_path}")

        # Remove backups antigos se exceder o limite
        backups = sorted([d for d in os.listdir(backup_dir) 
                         if os.path.isdir(os.path.join(backup_dir, d))])
        while len(backups) > config['backup']['max_backups']:
            old_backup = os.path.join(backup_dir, backups.pop(0))
            shutil.rmtree(old_backup)
            logging.info(f"Backup antigo removido: {old_backup}")

        # Gerar arquivo de integridade
        generate_backup_integrity(backup_path)

        # Criptografar backup se habilitado
        if config['backup'].get('encryption_enabled', False):
            encrypt_backup(backup_path)

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

def check_backup_integrity(backup_path, notify_on_fail=False, config=None, problems=None):
    """Verifica a integridade dos arquivos de backup usando o integrity.json."""
    integrity_file = os.path.join(backup_path, 'integrity.json')
    if not os.path.exists(integrity_file):
        msg = f"[ERRO] Arquivo de integridade não encontrado em {backup_path}"
        print(msg)
        if notify_on_fail and problems is not None:
            problems.append(msg)
        return False
    with open(integrity_file, 'r', encoding='utf-8') as f:
        integrity = json.load(f)
    all_ok = True
    for rel_path, expected_hash in integrity.items():
        file_path = os.path.join(backup_path, rel_path)
        if not os.path.exists(file_path):
            msg = f"[ERRO] Arquivo ausente: {rel_path} em {backup_path}"
            print(msg)
            all_ok = False
            if notify_on_fail and problems is not None:
                problems.append(msg)
            continue
        actual_hash = hash_file(file_path)
        if actual_hash != expected_hash:
            msg = f"[ERRO] Hash divergente: {rel_path} em {backup_path}\n  Esperado: {expected_hash}\n  Encontrado: {actual_hash}"
            print(msg)
            all_ok = False
            if notify_on_fail and problems is not None:
                problems.append(msg)
    if all_ok:
        print(f"[OK] Backup {backup_path} íntegro!")
    else:
        print(f"[FALHA] Integridade comprometida em {backup_path}")
    return all_ok

def check_all_backups(config, notify_on_fail=False):
    """Verifica a integridade de todos os backups existentes e envia notificação se houver falhas."""
    backup_dir = config['backup']['directory']
    if not os.path.exists(backup_dir):
        print("Nenhum backup encontrado.")
        return
    backups = sorted([d for d in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, d))])
    if not backups:
        print("Nenhum backup encontrado.")
        return
    problems = []
    for backup in backups:
        backup_path = os.path.join(backup_dir, backup)
        check_backup_integrity(backup_path, notify_on_fail=notify_on_fail, config=config, problems=problems)
    if notify_on_fail and problems:
        subject = "Alerta: Problemas de integridade em backup(s)"
        message = "Foram detectados problemas de integridade nos seguintes backups:\n\n" + "\n".join(problems)
        send_email_notification(subject, message, config)
        print("[ALERTA] Notificação de integridade enviada por e-mail!")

def print_status(config):
    print("\n===== STATUS DO SISTEMA DE BACKUP =====\n")
    # Backups
    backup_dir = config['backup']['directory']
    print("Backups recentes:")
    if not os.path.exists(backup_dir):
        print("  Nenhum backup encontrado.")
    else:
        backups = sorted([d for d in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, d))], reverse=True)
        for backup in backups[:5]:
            backup_path = os.path.join(backup_dir, backup)
            integrity_file = os.path.join(backup_path, 'integrity.json')
            encrypted = False
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    if file != 'integrity.json':
                        with open(os.path.join(root, file), 'rb') as f:
                            if f.read(1) == b'g':  # Fernet encrypted files start with 'g'
                                encrypted = True
                                break
                break
            status = "Criptografado" if encrypted else "Aberto"
            integrity = "OK" if os.path.exists(integrity_file) else "Sem integridade"
            print(f"  - {backup} | {status} | Integridade: {integrity}")
    # Últimos commits
    print("\nÚltimos commits automáticos:")
    try:
        repo = git.Repo('.')
        for commit in repo.iter_commits('main', max_count=5):
            msg = commit.message.strip().replace('\n', ' ')
            print(f"  - {commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S')} | {msg}")
    except Exception as e:
        print(f"  [ERRO] Não foi possível ler os commits: {e}")
    # Últimos erros
    print("\nErros recentes:")
    error_log = os.path.join('logs', 'auto_update_errors.log')
    if os.path.exists(error_log):
        with open(error_log, 'r', encoding='utf-8') as f:
            lines = f.readlines()[-5:]
            for line in lines:
                print(f"  {line.strip()}")
    else:
        print("  Nenhum erro registrado.")
    print("\n========================================\n")

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
    parser = argparse.ArgumentParser(description="Auto Update System")
    parser.add_argument('--check-backups', action='store_true', help='Verifica a integridade de todos os backups')
    parser.add_argument('--notify', action='store_true', help='Envia notificação por e-mail se houver falhas de integridade')
    parser.add_argument('--status', action='store_true', help='Exibe status dos backups, commits e erros recentes')
    args = parser.parse_args()

    if args.check_backups:
        config = load_config()
        check_all_backups(config, notify_on_fail=args.notify)
    elif args.status:
        config = load_config()
        print_status(config)
    else:
        main() 