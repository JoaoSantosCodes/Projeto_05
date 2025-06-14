import os
import smtplib
import pytest
from email.mime.text import MIMEText

@pytest.mark.integration
def test_send_mail_env():
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASSWORD')
    destinatario = os.environ.get('EMAIL_TEST_RECEIVER')

    if not all([username, password, destinatario]):
        pytest.skip('Variáveis de ambiente EMAIL_USER, EMAIL_PASSWORD e EMAIL_TEST_RECEIVER não definidas.')

    msg = MIMEText('Teste de envio seguro via pytest.')
    msg['Subject'] = 'Teste seguro'
    msg['From'] = username
    msg['To'] = destinatario

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(username, [destinatario], msg.as_string())
    except Exception as e:
        pytest.fail(f'Falha ao enviar e-mail: {e}') 