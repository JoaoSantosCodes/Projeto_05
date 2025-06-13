import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageTk
import io
import textwrap
import os
import smtplib
from email.message import EmailMessage
import win32com.client
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Consulta de Lojas e Serviços")
        self.root.geometry("1200x600")  # Aumentei a largura para acomodar mais colunas

        # Criar notebook (abas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)

        # Aba de Lojas
        self.tab_lojas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_lojas, text="Relação de Lojas")

        # Aba de Serviços
        self.tab_servicos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_servicos, text="Inventário")

        # Configurar aba de Lojas
        self.setup_lojas_tab()
        
        # Configurar aba de Serviços
        self.setup_servicos_tab()

    def setup_lojas_tab(self):
        # Frame para filtros
        filter_frame = ttk.LabelFrame(self.tab_lojas, text="Filtros")
        filter_frame.pack(padx=5, pady=5, fill="x")

        # Campo de busca
        ttk.Label(filter_frame, text="Buscar:").pack(side="left", padx=5)
        self.search_lojas = ttk.Entry(filter_frame)
        self.search_lojas.pack(side="left", padx=5, fill="x", expand=True)
        ttk.Button(filter_frame, text="Buscar", command=self.search_lojas_data).pack(side="left", padx=5)

        # Botão para gerar carimbo
        ttk.Button(filter_frame, text="Gerar Carimbo", command=self.gerar_carimbo_loja).pack(side="left", padx=5)

        # Treeview para mostrar dados
        columns = ("status", "peop", "nome", "endereco", "bairro", "cidade", "uf", "cep", 
                  "horario_semana", "horario_sabado", "horario_domingo", "funcionamento", "vd_novo")
        
        self.tree_lojas = ttk.Treeview(self.tab_lojas, columns=columns, show="headings")
        
        # Configurar cabeçalhos
        headers = {
            "status": "STATUS",
            "peop": "PEOP",
            "nome": "LOJAS",
            "endereco": "ENDEREÇO",
            "bairro": "BAIRRO",
            "cidade": "CIDADE",
            "uf": "UF",
            "cep": "CEP",
            "horario_semana": "2ª a 6ª",
            "horario_sabado": "SAB",
            "horario_domingo": "DOM",
            "funcionamento": "FUNC.",
            "vd_novo": "VD NOVO"
        }
        
        for col, header in headers.items():
            self.tree_lojas.heading(col, text=header)
            # Ajustar largura das colunas
            if col in ["nome", "endereco"]:
                self.tree_lojas.column(col, width=200)
            elif col in ["horario_semana", "horario_sabado", "horario_domingo", "funcionamento"]:
                self.tree_lojas.column(col, width=80)
            else:
                self.tree_lojas.column(col, width=100)

        # Scrollbar horizontal e vertical
        y_scrollbar = ttk.Scrollbar(self.tab_lojas, orient="vertical", command=self.tree_lojas.yview)
        x_scrollbar = ttk.Scrollbar(self.tab_lojas, orient="horizontal", command=self.tree_lojas.xview)
        self.tree_lojas.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Posicionar elementos
        self.tree_lojas.pack(padx=5, pady=5, fill="both", expand=True)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar.pack(side="bottom", fill="x")

        # Carregar dados iniciais
        self.load_lojas_data()

    def setup_servicos_tab(self):
        # Frame para filtros
        filter_frame = ttk.LabelFrame(self.tab_servicos, text="Filtros")
        filter_frame.pack(padx=5, pady=5, fill="x")

        # Campo de busca
        ttk.Label(filter_frame, text="Buscar:").pack(side="left", padx=5)
        self.search_servicos = ttk.Entry(filter_frame)
        self.search_servicos.pack(side="left", padx=5, fill="x", expand=True)
        ttk.Button(filter_frame, text="Buscar", command=self.search_servicos_data).pack(side="left", padx=5)

        # Botão para gerar carimbo
        ttk.Button(filter_frame, text="Gerar Carimbo", command=self.gerar_carimbo_inventario).pack(side="left", padx=5)

        # Treeview para mostrar dados
        columns = ("people", "operadora", "circuito_designacao", "novo_circuito_designacao", "id_vivo", "novo_id_vivo")
        
        self.tree_servicos = ttk.Treeview(self.tab_servicos, columns=columns, show="headings")
        
        # Configurar cabeçalhos
        headers = {
            "people": "PEOP",
            "operadora": "Operadora",
            "circuito_designacao": "Circuito/Designação",
            "novo_circuito_designacao": "Novo Circuito/Designação",
            "id_vivo": "ID VIVO",
            "novo_id_vivo": "Novo ID Vivo"
        }
        
        for col, header in headers.items():
            self.tree_servicos.heading(col, text=header)
            # Ajustar largura das colunas
            if col in ["circuito_designacao", "novo_circuito_designacao"]:
                self.tree_servicos.column(col, width=200)
            else:
                self.tree_servicos.column(col, width=150)

        # Scrollbar horizontal e vertical
        y_scrollbar = ttk.Scrollbar(self.tab_servicos, orient="vertical", command=self.tree_servicos.yview)
        x_scrollbar = ttk.Scrollbar(self.tab_servicos, orient="horizontal", command=self.tree_servicos.xview)
        self.tree_servicos.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Posicionar elementos
        self.tree_servicos.pack(padx=5, pady=5, fill="both", expand=True)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar.pack(side="bottom", fill="x")

        # Carregar dados iniciais
        self.load_servicos_data()

    def load_lojas_data(self, search_term=""):
        # Limpar dados existentes
        for item in self.tree_lojas.get_children():
            self.tree_lojas.delete(item)

        # Conectar ao banco de dados
        conn = sqlite3.connect('inventario.db')
        
        # Construir query
        query = """
            SELECT status, 
                   CASE 
                       WHEN peop LIKE 'L%' THEN substr(peop, 2)
                       WHEN peop LIKE 'VD%' THEN substr(peop, 3)
                       ELSE peop 
                   END as peop,
                   nome, endereco, bairro, cidade, uf, cep,
                   horario_semana, horario_sabado, horario_domingo, funcionamento, vd_novo 
            FROM lojas
        """
        if search_term:
            query += f" WHERE nome LIKE '%{search_term}%' OR peop LIKE '%{search_term}%'"
        query += " LIMIT 1000"

        # Carregar dados
        df = pd.read_sql_query(query, conn)
        for _, row in df.iterrows():
            self.tree_lojas.insert("", "end", values=(
                row['status'],
                row['peop'],
                row['nome'],
                row['endereco'],
                row['bairro'],
                row['cidade'],
                row['uf'],
                row['cep'],
                row['horario_semana'],
                row['horario_sabado'],
                row['horario_domingo'],
                row['funcionamento'],
                row['vd_novo']
            ))
        
        conn.close()

    def load_servicos_data(self, search_term=""):
        # Limpar dados existentes
        for item in self.tree_servicos.get_children():
            self.tree_servicos.delete(item)

        # Conectar ao banco de dados
        conn = sqlite3.connect('inventario.db')
        
        # Construir query
        query = """
            SELECT people, operadora, circuito_designacao, novo_circuito_designacao, id_vivo, novo_id_vivo 
            FROM servicos_internet
        """
        if search_term:
            query += f" WHERE people LIKE '%{search_term}%' OR circuito_designacao LIKE '%{search_term}%'"
        query += " LIMIT 1000"

        # Carregar dados
        df = pd.read_sql_query(query, conn)
        for _, row in df.iterrows():
            self.tree_servicos.insert("", "end", values=(
                row['people'],
                row['operadora'],
                row['circuito_designacao'],
                row['novo_circuito_designacao'],
                row['id_vivo'],
                row['novo_id_vivo']
            ))
        
        conn.close()

    def search_lojas_data(self):
        search_term = self.search_lojas.get()
        self.load_lojas_data(search_term)

    def search_servicos_data(self):
        search_term = self.search_servicos.get()
        self.load_servicos_data(search_term)

    def gerar_carimbo_loja(self):
        selected = self.tree_lojas.selection()
        if not selected:
            messagebox.showwarning("Seleção necessária", "Selecione uma loja para gerar o carimbo.")
            return
        values = self.tree_lojas.item(selected[0], 'values')
        carimbo_texto = f"""
PEOP: {values[1]}
LOJAS: {values[2]}
ENDEREÇO: {values[3]}
BAIRRO: {values[4]}
CIDADE: {values[5]}
UF: {values[6]}
CEP: {values[7]}

2ª a 6ª: {values[8]}
SAB / DOM: {values[9]} / {values[10]}
FUNC.: {values[11]}
VD NOVO: {values[12]}

----------------------------------------
CONTATO COMMAND CENTER
Telefone: (11) 3274-7527
E-mail: central.comando@dpsp.com.br

MENSAGEM DE ABERTURA DE CHAMADO NOS PORTAIS
LOJA VD {values[1]} FAVOR LIGAR PARA CONFIRMAR A NORMALIZAÇÃO E LIBERAÇÃO DE ACESSO COM A CENTRAL DE COMANDO | HORÁRIO DE FUNCIONAMENTO: 24 HORAS | SÁB 24 HORAS | DOM 24 HORAS
"""
        # Exibir em popup apenas a imagem
        top = tk.Toplevel(self.root)
        top.title("Carimbo - Relação de Lojas")
        try:
            img = self.gerar_png_carimbo(carimbo_texto, f"carimbo_loja_{values[1]}.png", return_image=True)
            max_width = 900
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height))
            img_tk = ImageTk.PhotoImage(img)
            label_img = tk.Label(top, image=img_tk)
            label_img.image = img_tk  # manter referência
            label_img.pack(padx=10, pady=10)
        except Exception as e:
            tk.Label(top, text=f"Erro ao carregar imagem: {e}", fg="red").pack()
        png_path = f"carimbos/carimbo_loja_{values[1]}.png"
        tk.Label(top, text=f"PNG salvo como carimbo_loja_{values[1]}.png").pack()

        # HTML personalizado (igual ao Outlook)
        peop = values[1]
        loja = values[2]
        assunto = f"{peop} | {loja} - Link Inoperante"
        assinatura = "<br>Atenciosamente,<br>"
        html = f'''
        <html><body>
        <p>Prezados,</p>
        <p>Identificamos que o link da loja <b>{peop} | {loja}</b> está inoperante. Seguem os dados necessários para abertura do reparo:</p>
        <table cellpadding="4" cellspacing="0" border="1" style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:14px;">
            <tr style="background:#b4d2ff;font-weight:bold;text-align:center;"><td colspan="2" style="font-size:20px;">Relação de Lojas</td></tr>
            <tr style="background:#b4d2ff;font-weight:bold;"><td>PEOP</td><td>{peop}</td></tr>
            <tr style="background:#5dc0d6;font-weight:bold;"><td>LOJAS</td><td>{loja}</td></tr>
            <tr style="background:#5dc0d6;font-weight:bold;"><td>ENDEREÇO</td><td>{values[3]}</td></tr>
            <tr style="background:#5dc0d6;font-weight:bold;"><td>BAIRRO</td><td>{values[4]}</td></tr>
            <tr style="background:#5dc0d6;font-weight:bold;"><td>CIDADE</td><td>{values[5]}</td></tr>
            <tr style="background:#5dc0d6;font-weight:bold;"><td>UF</td><td>{values[6]}</td></tr>
            <tr style="background:#5dc0d6;font-weight:bold;"><td>CEP</td><td>{values[7]}</td></tr>
            <tr style="background:#fff7b2;font-weight:bold;"><td>2ª a 6ª</td><td>{values[8]}</td></tr>
            <tr style="background:#fff7b2;font-weight:bold;"><td>SAB / DOM</td><td>{values[9]} / {values[10]}</td></tr>
            <tr style="background:#fff7b2;font-weight:bold;"><td>FUNC.</td><td>{values[11]}</td></tr>
            <tr style="background:#fff7b2;font-weight:bold;"><td>VD NOVO</td><td>{values[12]}</td></tr>
            <tr>
                <td colspan="2" style="background:#ed1c24;color:#fff;font-weight:bold;text-align:left;">
                    CONTATO COMMAND CENTER<br>
                    Telefone: (11) 3274-7527<br>
                    E-mail: <a href="mailto:central.comando@dpsp.com.br" style="color:#fff;">central.comando@dpsp.com.br</a>
                </td>
            </tr>
            <tr>
                <td colspan="2" style="background:#333;color:#ffe000;font-weight:bold;text-align:center;">MENSAGEM DE ABERTURA DE CHAMADO NOS PORTAIS</td>
            </tr>
            <tr>
                <td colspan="2" style="background:#fff7b2;color:#000;font-weight:bold;text-align:left;">
                    LOJA VD {peop} FAVOR LIGAR PARA CONFIRMAR A NORMALIZAÇÃO E LIBERAÇÃO DE ACESSO COM A CENTRAL DE COMANDO | HORÁRIO DE FUNCIONAMENTO: 24 HORAS | SÁB 24 HORAS | DOM 24 HORAS
                </td>
            </tr>
        </table>
        <p>Agradecemos pela atenção{assinatura}</p>
        </body></html>
        '''

        def enviar_email_smtp():
            if not messagebox.askyesno("Confirmação", "Deseja realmente enviar este e-mail para operacionaldpsp@gmail.com?"):
                return
            try:
                smtp_server = 'smtp.gmail.com'
                smtp_port = 587
                username = 'OperacionalDPSP@gmail.com'
                password = 'mxqi oerj ndda edvx'
                destinatario = 'operacionaldpsp@gmail.com'
                msg = MIMEMultipart()
                msg['From'] = username
                msg['To'] = destinatario
                msg['Subject'] = assunto
                msg.attach(MIMEText(html, 'html'))
                # Anexar PNG
                with open(png_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="carimbo_loja_{peop}.png"')
                    msg.attach(part)
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(username, password)
                    server.send_message(msg)
                messagebox.showinfo("E-mail enviado", "E-mail enviado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro ao enviar e-mail", str(e))

        btn_email_smtp = tk.Button(top, text="Enviar por E-mail (Gmail/SMTP)", command=enviar_email_smtp)
        btn_email_smtp.pack(pady=5)

        # Botão Outlook já existente
        def enviar_email_outlook():
            try:
                outlook = win32com.client.Dispatch('outlook.application')
                mail = outlook.CreateItem(0)
                mail.To = "operacionaldpsp@gmail.com"
                mail.Subject = assunto
                mail.HTMLBody = html
                mail.Display()
            except Exception as e:
                messagebox.showerror("Erro ao abrir Outlook", str(e))
        btn_email_outlook = tk.Button(top, text="Enviar por E-mail (Outlook)", command=enviar_email_outlook)
        btn_email_outlook.pack(pady=5)

    def gerar_png_carimbo(self, texto, filename, return_image=False):
        # Criar pasta carimbos se não existir
        pasta = 'carimbos'
        if not os.path.exists(pasta):
            os.makedirs(pasta)
        # Ajustar o caminho do arquivo
        filename = os.path.join(pasta, os.path.basename(filename))
        # Definições de layout e cores
        largura = 800
        altura_linha = 40
        margem = 18
        fonte_padrao = ImageFont.load_default()
        try:
            fonte_titulo = ImageFont.truetype("arialbd.ttf", 28)
            fonte_campo = ImageFont.truetype("arial.ttf", 18)
            fonte_campo_bold = ImageFont.truetype("arialbd.ttf", 18)
            fonte_bloco = ImageFont.truetype("arialbd.ttf", 17)
        except:
            fonte_titulo = fonte_padrao
            fonte_campo = fonte_padrao
            fonte_campo_bold = fonte_padrao
            fonte_bloco = fonte_padrao
        azul_titulo = (180, 210, 255)
        azul_campo = (200, 230, 255)
        ciano = (170, 230, 230)
        amarelo = (255, 255, 180)
        amarelo_msg = (255, 230, 80)
        vermelho = (200, 30, 30)
        cinza = (80, 80, 80)
        branco = (255, 255, 255)
        preto = (0, 0, 0)
        # Parse do texto em blocos
        lines = texto.strip().split('\n')
        if lines[0].strip().upper().startswith("PEOP") or lines[0].strip().upper().startswith("PEOPLE"):
            titulo = "Relação de Lojas"
        else:
            titulo = "Inventário"
        campos = []
        horarios = []
        contato = []
        msg_portal = []
        msg_final = []
        bloco = 0
        for line in lines:
            if '--------' in line:
                bloco += 1
                continue
            if bloco == 0:
                campos.append(line)
            elif bloco == 1:
                horarios.append(line)
            elif bloco == 2:
                contato.append(line)
            elif bloco == 3:
                msg_portal.append(line)
            elif bloco == 4:
                msg_final.append(line)
        campos_labels = [c.split(':')[0].strip() for c in campos if ':' in c]
        campos_values = [c.split(':',1)[1].strip() for c in campos if ':' in c]
        campos_ciano = [1,2,3,4,5] if titulo=="Inventário" else []
        campos_azul = [0] if titulo=="Relação de Lojas" else []
        campos_amarelo = list(range(len(campos_labels), len(campos_labels)+len(horarios)))
        n_linhas = 1 + len(campos_labels) + len(horarios) + 1 + len(contato) + 1 + len(msg_portal) + len(msg_final)
        altura = n_linhas * altura_linha + 2*margem + 40
        img = Image.new('RGB', (largura, altura), branco)
        draw = ImageDraw.Draw(img)
        y = margem
        # Título
        draw.rectangle([0, y, largura, y+altura_linha], fill=azul_titulo)
        bbox = draw.textbbox((0, 0), titulo, font=fonte_titulo)
        w = bbox[2] - bbox[0]
        draw.text(((largura-w)//2, y+8), titulo, font=fonte_titulo, fill=preto)
        y += altura_linha
        # Campos principais
        for i, (label, value) in enumerate(zip(campos_labels, campos_values)):
            cor = branco
            if i in campos_ciano:
                cor = ciano
            if i in campos_azul:
                cor = azul_campo
            if i in campos_amarelo:
                cor = amarelo
            draw.rectangle([0, y, largura//2, y+altura_linha], fill=cor)
            draw.rectangle([largura//2, y, largura, y+altura_linha], fill=branco)
            draw.text((margem, y+10), label, font=fonte_campo_bold, fill=preto)
            value_lines = textwrap.wrap(value, width=38)
            for j, vline in enumerate(value_lines):
                draw.text((largura//2+margem, y+10+j*20), vline, font=fonte_campo, fill=preto)
            y += altura_linha
        # Horários/amarelo
        for h in horarios:
            draw.rectangle([0, y, largura, y+altura_linha], fill=amarelo)
            draw.text((margem, y+10), h, font=fonte_campo_bold, fill=preto)
            y += altura_linha
        # Bloco contato (amarelo claro, borda vermelha)
        if contato:
            draw.rectangle([0, y, largura, y+altura_linha*len(contato)], fill=amarelo)
            draw.rectangle([0, y, largura, y+altura_linha*len(contato)], outline=vermelho, width=3)
            for i, c in enumerate(contato):
                draw.text((margem, y+10+i*20), c, font=fonte_bloco, fill=preto)
            y += altura_linha*len(contato)
        # Bloco mensagem portal (cinza escuro + amarelo)
        if msg_portal:
            draw.rectangle([0, y, largura, y+altura_linha], fill=cinza)
            draw.text((margem, y+10), msg_portal[0], font=fonte_bloco, fill=amarelo_msg)
            y += altura_linha
        # Mensagem final (amarelo destaque)
        for m in msg_final:
            draw.rectangle([0, y, largura, y+altura_linha], fill=amarelo_msg)
            m_lines = textwrap.wrap(m, width=90)
            for j, mline in enumerate(m_lines):
                draw.text((margem, y+10+j*20), mline, font=fonte_bloco, fill=preto)
            y += altura_linha*len(m_lines)
        # Bordas
        draw.rectangle([0, 0, largura-1, altura-1], outline=(100,100,100), width=3)
        img.save(filename)
        if return_image:
            return img

    def gerar_carimbo_inventario(self):
        selected = self.tree_servicos.selection()
        if not selected:
            messagebox.showwarning("Seleção necessária", "Selecione um item para gerar o carimbo.")
            return
        values = self.tree_servicos.item(selected[0], 'values')
        # Para os horários, buscar na tabela de lojas pelo people
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        cursor.execute("SELECT horario_semana, horario_sabado, horario_domingo, funcionamento FROM lojas WHERE peop=? OR peop=?", (values[0], 'VD'+values[0]))
        row = cursor.fetchone()
        if row:
            horario_semana, horario_sabado, horario_domingo, funcionamento = row
        else:
            horario_semana = horario_sabado = horario_domingo = funcionamento = ''
        conn.close()
        carimbo_texto = f"""
People: {values[0]}
Operadora: {values[1]}
Circuito/Designação: {values[2]}
Novo Circuito/Designação: {values[3]}
ID VIVO: {values[4]}
Novo ID Vivo: {values[5]}

2ª a 6ª: {horario_semana}
SAB / DOM: {horario_sabado} / {horario_domingo}
FUNC.: {funcionamento}

----------------------------------------
CONTATO COMMAND CENTER
Telefone: (11) 3274-7527
E-mail: central.comando@dpsp.com.br

MENSAGEM DE ABERTURA DE CHAMADO NOS PORTAIS
LOJA VD {values[0]} FAVOR LIGAR PARA CONFIRMAR A NORMALIZAÇÃO E LIBERAÇÃO DE ACESSO COM A CENTRAL DE COMANDO | HORÁRIO DE FUNCIONAMENTO: 24 HORAS | SÁB 24 HORAS | DOM 24 HORAS
"""
        # Exibir em popup apenas a imagem
        top = tk.Toplevel(self.root)
        top.title("Carimbo - Inventário")
        try:
            img = self.gerar_png_carimbo(carimbo_texto, f"carimbo_inventario_{values[0]}.png", return_image=True)
            max_width = 900
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height))
            img_tk = ImageTk.PhotoImage(img)
            label_img = tk.Label(top, image=img_tk)
            label_img.image = img_tk  # manter referência
            label_img.pack(padx=10, pady=10)
        except Exception as e:
            tk.Label(top, text=f"Erro ao carregar imagem: {e}", fg="red").pack()
        png_path = f"carimbos/carimbo_inventario_{values[0]}.png"
        tk.Label(top, text=f"PNG salvo como carimbo_inventario_{values[0]}.png").pack()

        # HTML personalizado (igual ao Outlook)
        peop = values[0]
        loja = values[2]
        assunto = f"{peop} | {loja} - Link Inoperante"
        assinatura = "<br>Atenciosamente,<br>"
        html = f'''
        <html><body>
        <p>Prezados,</p>
        <p>Identificamos que o link da loja <b>{peop} | {loja}</b> está inoperante. Seguem os dados necessários para abertura do reparo:</p>
        <table cellpadding="4" cellspacing="0" border="1" style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:14px;">
            <tr style="background:#b4d2ff;font-weight:bold;text-align:center;"><td colspan="2" style="font-size:20px;">Inventário</td></tr>
            <tr style="background:#b4d2ff;font-weight:bold;"><td>People</td><td>{peop}</td></tr>
            <tr style="background:#5dc0d6;font-weight:bold;"><td>Operadora</td><td>{values[1]}</td></tr>
            <tr style="background:#5dc0d6;font-weight:bold;"><td>Circuito/Designação</td><td>{values[2]}</td></tr>
            <tr style="background:#5dc0d6;font-weight:bold;"><td>Novo Circuito/Designação</td><td>{values[3]}</td></tr>
            <tr style="background:#5dc0d6;font-weight:bold;"><td>ID VIVO</td><td>{values[4]}</td></tr>
            <tr style="background:#5dc0d6;font-weight:bold;"><td>Novo ID Vivo</td><td>{values[5]}</td></tr>
            <tr style="background:#fff7b2;font-weight:bold;"><td>2ª a 6ª</td><td>{horario_semana}</td></tr>
            <tr style="background:#fff7b2;font-weight:bold;"><td>SAB / DOM</td><td>{horario_sabado} / {horario_domingo}</td></tr>
            <tr style="background:#fff7b2;font-weight:bold;"><td>FUNC.</td><td>{funcionamento}</td></tr>
            <tr>
                <td colspan="2" style="background:#ed1c24;color:#fff;font-weight:bold;text-align:left;">
                    CONTATO COMMAND CENTER<br>
                    Telefone: (11) 3274-7527<br>
                    E-mail: <a href="mailto:central.comando@dpsp.com.br" style="color:#fff;">central.comando@dpsp.com.br</a>
                </td>
            </tr>
            <tr>
                <td colspan="2" style="background:#333;color:#ffe000;font-weight:bold;text-align:center;">MENSAGEM DE ABERTURA DE CHAMADO NOS PORTAIS</td>
            </tr>
            <tr>
                <td colspan="2" style="background:#fff7b2;color:#000;font-weight:bold;text-align:left;">
                    LOJA VD {peop} FAVOR LIGAR PARA CONFIRMAR A NORMALIZAÇÃO E LIBERAÇÃO DE ACESSO COM A CENTRAL DE COMANDO | HORÁRIO DE FUNCIONAMENTO: 24 HORAS | SÁB 24 HORAS | DOM 24 HORAS
                </td>
            </tr>
        </table>
        <p>Agradecemos pela atenção{assinatura}</p>
        </body></html>
        '''

        def enviar_email_smtp():
            if not messagebox.askyesno("Confirmação", "Deseja realmente enviar este e-mail para operacionaldpsp@gmail.com?"):
                return
            try:
                smtp_server = 'smtp.gmail.com'
                smtp_port = 587
                username = 'OperacionalDPSP@gmail.com'
                password = 'mxqi oerj ndda edvx'
                destinatario = 'operacionaldpsp@gmail.com'
                msg = MIMEMultipart()
                msg['From'] = username
                msg['To'] = destinatario
                msg['Subject'] = assunto
                msg.attach(MIMEText(html, 'html'))
                # Anexar PNG
                with open(png_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="carimbo_inventario_{peop}.png"')
                    msg.attach(part)
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(username, password)
                    server.send_message(msg)
                messagebox.showinfo("E-mail enviado", "E-mail enviado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro ao enviar e-mail", str(e))

        btn_email_smtp = tk.Button(top, text="Enviar por E-mail (Gmail/SMTP)", command=enviar_email_smtp)
        btn_email_smtp.pack(pady=5)

        # Botão Outlook já existente
        def enviar_email_outlook():
            try:
                outlook = win32com.client.Dispatch('outlook.application')
                mail = outlook.CreateItem(0)
                mail.To = "operacionaldpsp@gmail.com"
                mail.Subject = assunto
                mail.HTMLBody = html
                mail.Display()
            except Exception as e:
                messagebox.showerror("Erro ao abrir Outlook", str(e))
        btn_email_outlook = tk.Button(top, text="Enviar por E-mail (Outlook)", command=enviar_email_outlook)
        btn_email_outlook.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop() 