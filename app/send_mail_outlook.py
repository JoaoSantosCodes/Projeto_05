import win32com.client

# Cria uma instância do Outlook
outlook = win32com.client.Dispatch('outlook.application')
mail = outlook.CreateItem(0)  # 0 = olMailItem

mail.To = 'Operacionaldpsp@gmail.com'
mail.Subject = 'Teste de envio via Outlook Desktop'
mail.Body = 'Este é um teste de envio de e-mail usando o Outlook Desktop via Python.'

# Para anexar arquivos, descomente a linha abaixo e ajuste o caminho
# mail.Attachments.Add(r'C:\Cursor\Projeto_02\carimbos\carimbo_loja_1080.png')

mail.Send()  # Para enviar direto
# mail.Display()  # Para abrir a janela de e-mail antes de enviar

print('E-mail enviado com sucesso!') 