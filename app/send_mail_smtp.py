"""
Script de envio de e-mail via SMTP (Gmail) usando variável de ambiente para a senha.

Antes de rodar, defina a variável de ambiente EMAIL_PASSWORD com a senha de app do Gmail:
No PowerShell:
    $env:EMAIL_PASSWORD="SUA_SENHA_DE_APP"
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server = 'smtp.gmail.com'
smtp_port = 587
username = 'OperacionalDPSP@gmail.com'
password = 'mxqi oerj ndda edvx'  # Senha de app fornecida

destinatario = 'Operacionaldpsp@gmail.com'

msg = MIMEMultipart()
msg['From'] = username
msg['To'] = destinatario
msg['Subject'] = 'Teste SMTP via Python'
msg.attach(MIMEText('Este é um teste de envio de e-mail via SMTP automatizado.', 'plain'))

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(username, password)
    server.send_message(msg)

print('E-mail enviado com sucesso!') 