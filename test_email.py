import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml
from dotenv import load_dotenv

def test_email_send():
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Carrega configurações
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Obtém credenciais
    email_user = os.getenv('EMAIL_USER')
    email_password = os.getenv('EMAIL_PASSWORD')
    
    if not email_user or not email_password:
        print("Erro: Credenciais de e-mail não encontradas no arquivo .env")
        return
    
    # Configura mensagem
    msg = MIMEMultipart()
    msg['From'] = config['notifications']['email']['sender_email']
    msg['To'] = config['notifications']['email']['recipient_email']
    msg['Subject'] = f"{config['notifications']['email']['subject_prefix']} Teste de Envio"
    
    body = """
    Este é um e-mail de teste do sistema de atualização automática.
    
    Se você está recebendo este e-mail, significa que:
    1. As configurações de e-mail estão corretas
    2. As credenciais estão funcionando
    3. O sistema de notificações está pronto para uso
    
    Data e hora do teste: {}
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Conecta ao servidor SMTP
        print("Conectando ao servidor SMTP...")
        with smtplib.SMTP(config['notifications']['email']['smtp_server'], 
                         config['notifications']['email']['smtp_port']) as server:
            server.starttls()
            print("Iniciando autenticação...")
            server.login(email_user, email_password)
            print("Enviando e-mail de teste...")
            server.send_message(msg)
            print("E-mail enviado com sucesso!")
            
    except Exception as e:
        print(f"Erro ao enviar e-mail: {str(e)}")

if __name__ == "__main__":
    from datetime import datetime
    test_email_send() 