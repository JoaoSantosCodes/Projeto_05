import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
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
import tkinter.font as tkfont

def add_tooltip(widget, text):
    tooltip = None
    def on_enter(event):
        nonlocal tooltip
        x = event.x_root + 20
        y = event.y_root + 10
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1, font=("Arial", 10))
        label.pack()
    def on_leave(event):
        nonlocal tooltip
        if tooltip:
            tooltip.destroy()
            tooltip = None
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Consulta de Lojas e Serviços")
        self.root.geometry("1200x600")
        self.theme = "light"
        self.style = ttk.Style()
        self.set_theme(self.theme)
        # Botão de alternância de tema
        theme_btn = ttk.Button(root, text="🌙 Tema Escuro", command=self.toggle_theme)
        theme_btn.pack(pady=2, anchor="ne", padx=10)
        self.theme_btn = theme_btn
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

    def set_theme(self, theme):
        if theme == "dark":
            bg = "#23272e"
            fg = "#f1f1f1"
            entry_bg = "#2d323b"
            entry_fg = "#f1f1f1"
            tree_bg = "#23272e"
            tree_fg = "#f1f1f1"
            select_bg = "#3a3f4b"
            select_fg = "#ffe000"
            self.style.theme_use('clam')
            self.style.configure("TFrame", background=bg)
            self.style.configure("TLabel", background=bg, foreground=fg)
            self.style.configure("TButton", background="#444", foreground="#ffe000")
            self.style.configure("TEntry", fieldbackground=entry_bg, foreground=entry_fg)
            self.style.configure("TCombobox", fieldbackground=entry_bg, background=entry_bg, foreground=entry_fg)
            self.style.configure("Treeview", background=tree_bg, foreground=tree_fg, fieldbackground=tree_bg)
            self.style.map("Treeview", background=[('selected', select_bg)], foreground=[('selected', select_fg)])
            self.root.configure(bg=bg)
        else:
            bg = "#f5f6fa"
            fg = "#23272e"
            entry_bg = "#fff"
            entry_fg = "#23272e"
            tree_bg = "#fff"
            tree_fg = "#23272e"
            select_bg = "#b4d2ff"
            select_fg = "#23272e"
            self.style.theme_use('clam')
            self.style.configure("TFrame", background=bg)
            self.style.configure("TLabel", background=bg, foreground=fg)
            self.style.configure("TButton", background="#1976d2", foreground="#fff")
            self.style.configure("TEntry", fieldbackground=entry_bg, foreground=entry_fg)
            self.style.configure("TCombobox", fieldbackground=entry_bg, background=entry_bg, foreground=entry_fg)
            self.style.configure("Treeview", background=tree_bg, foreground=tree_fg, fieldbackground=tree_bg)
            self.style.map("Treeview", background=[('selected', select_bg)], foreground=[('selected', select_fg)])
            self.root.configure(bg=bg)

    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.set_theme("dark")
            self.theme_btn.config(text="☀️ Tema Claro")
        else:
            self.theme = "light"
            self.set_theme("light")
            self.theme_btn.config(text="🌙 Tema Escuro")

    def setup_lojas_tab(self):
        # Frame para filtros
        filter_frame = ttk.LabelFrame(self.tab_lojas, text="Filtros")
        filter_frame.pack(padx=5, pady=5, fill="x")

        # Campo de busca
        ttk.Label(filter_frame, text="Buscar:").pack(side="left", padx=5)
        self.search_lojas = ttk.Entry(filter_frame)
        self.search_lojas.pack(side="left", padx=5, fill="x", expand=True)
        self.search_lojas.bind('<Return>', lambda e: self.search_lojas_data())

        # Filtro UF
        ttk.Label(filter_frame, text="UF:").pack(side="left", padx=5)
        self.uf_var = tk.StringVar()
        self.uf_combo = ttk.Combobox(filter_frame, textvariable=self.uf_var, width=5, state="readonly")
        self.uf_combo.pack(side="left", padx=5)
        self.uf_combo['values'] = self.get_unique_values('lojas', 'uf')
        self.uf_combo.set('')

        # Filtro Operadora
        ttk.Label(filter_frame, text="Operadora:").pack(side="left", padx=5)
        self.operadora_var = tk.StringVar()
        self.operadora_combo = ttk.Combobox(filter_frame, textvariable=self.operadora_var, width=12, state="readonly")
        self.operadora_combo.pack(side="left", padx=5)
        self.operadora_combo['values'] = self.get_unique_values('servicos_internet', 'operadora')
        self.operadora_combo.set('')

        # Botão para buscar
        ttk.Button(filter_frame, text="Buscar", command=self.search_lojas_data).pack(side="left", padx=5)
        # Botão para exportar
        ttk.Button(filter_frame, text="Exportar CSV", command=self.export_lojas_csv).pack(side="left", padx=5)
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
        self.search_servicos.bind('<Return>', lambda e: self.search_servicos_data())

        # Filtro UF
        ttk.Label(filter_frame, text="UF:").pack(side="left", padx=5)
        self.uf_serv_var = tk.StringVar()
        self.uf_serv_combo = ttk.Combobox(filter_frame, textvariable=self.uf_serv_var, width=5, state="readonly")
        self.uf_serv_combo.pack(side="left", padx=5)
        self.uf_serv_combo['values'] = self.get_unique_values('lojas', 'uf')
        self.uf_serv_combo.set('')

        # Filtro Operadora
        ttk.Label(filter_frame, text="Operadora:").pack(side="left", padx=5)
        self.operadora_serv_var = tk.StringVar()
        self.operadora_serv_combo = ttk.Combobox(filter_frame, textvariable=self.operadora_serv_var, width=12, state="readonly")
        self.operadora_serv_combo.pack(side="left", padx=5)
        self.operadora_serv_combo['values'] = self.get_unique_values('servicos_internet', 'operadora')
        self.operadora_serv_combo.set('')

        # Botão para buscar
        ttk.Button(filter_frame, text="Buscar", command=self.search_servicos_data).pack(side="left", padx=5)
        # Botão para exportar
        ttk.Button(filter_frame, text="Exportar CSV", command=self.export_servicos_csv).pack(side="left", padx=5)
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

    def get_unique_values(self, table, column):
        conn = sqlite3.connect('inventario.db')
        try:
            df = pd.read_sql_query(f"SELECT DISTINCT {column} FROM {table} WHERE {column} IS NOT NULL AND {column} != '' ORDER BY {column}", conn)
            return tuple(df[column].dropna().astype(str).tolist())
        except Exception:
            return ()
        finally:
            conn.close()

    def load_lojas_data(self, search_term="", uf="", operadora=""):
        for item in self.tree_lojas.get_children():
            self.tree_lojas.delete(item)
        conn = sqlite3.connect('inventario.db')
        # Query multi-campos e filtros
        query = """
            SELECT l.status, 
                   CASE 
                       WHEN l.peop LIKE 'L%' THEN substr(l.peop, 2)
                       WHEN l.peop LIKE 'VD%' THEN substr(l.peop, 3)
                       ELSE l.peop 
                   END as peop,
                   l.nome, l.endereco, l.bairro, l.cidade, l.uf, l.cep,
                   l.horario_semana, l.horario_sabado, l.horario_domingo, l.funcionamento, l.vd_novo
            FROM lojas l
            LEFT JOIN servicos_internet s ON l.peop = s.people OR l.peop = substr(s.people,2) OR l.peop = substr(s.people,3)
        """
        where = []
        params = []
        if search_term:
            where.append("(l.nome LIKE ? OR l.peop LIKE ? OR l.endereco LIKE ? OR l.cidade LIKE ? OR l.bairro LIKE ? OR s.operadora LIKE ? OR s.circuito_designacao LIKE ?)")
            for _ in range(7):
                params.append(f"%{search_term}%")
        if uf:
            where.append("l.uf = ?")
            params.append(uf)
        if operadora:
            where.append("s.operadora = ?")
            params.append(operadora)
        if where:
            query += " WHERE " + " AND ".join(where)
        query += " GROUP BY l.peop LIMIT 1000"
        df = pd.read_sql_query(query, conn, params=params)
        for _, row in df.iterrows():
            self.tree_lojas.insert("", "end", values=(
                row['status'], row['peop'], row['nome'], row['endereco'], row['bairro'], row['cidade'], row['uf'], row['cep'],
                row['horario_semana'], row['horario_sabado'], row['horario_domingo'], row['funcionamento'], row['vd_novo']
            ))
        if df.empty:
            self.tree_lojas.insert("", "end", values=("Nenhum resultado encontrado",) + ("",)*12)
        conn.close()

    def load_servicos_data(self, search_term="", uf="", operadora=""):
        for item in self.tree_servicos.get_children():
            self.tree_servicos.delete(item)
        conn = sqlite3.connect('inventario.db')
        query = """
            SELECT s.people, s.operadora, s.circuito_designacao, s.novo_circuito_designacao, s.id_vivo, s.novo_id_vivo, l.uf
            FROM servicos_internet s
            LEFT JOIN lojas l ON s.people = l.peop OR s.people = 'L' || l.peop OR s.people = 'VD' || l.peop
        """
        where = []
        params = []
        if search_term:
            where.append("(s.people LIKE ? OR s.operadora LIKE ? OR s.circuito_designacao LIKE ? OR s.novo_circuito_designacao LIKE ? OR s.id_vivo LIKE ? OR l.nome LIKE ? OR l.cidade LIKE ?)")
            for _ in range(7):
                params.append(f"%{search_term}%")
        if uf:
            where.append("l.uf = ?")
            params.append(uf)
        if operadora:
            where.append("s.operadora = ?")
            params.append(operadora)
        if where:
            query += " WHERE " + " AND ".join(where)
        query += " GROUP BY s.people, s.operadora, s.circuito_designacao LIMIT 1000"
        df = pd.read_sql_query(query, conn, params=params)
        for _, row in df.iterrows():
            self.tree_servicos.insert("", "end", values=(
                row['people'], row['operadora'], row['circuito_designacao'], row['novo_circuito_designacao'], row['id_vivo'], row['novo_id_vivo']
            ))
        if df.empty:
            self.tree_servicos.insert("", "end", values=("Nenhum resultado encontrado",) + ("",)*5)
        conn.close()

    def search_lojas_data(self):
        search_term = self.search_lojas.get()
        uf = self.uf_var.get()
        operadora = self.operadora_var.get()
        self.load_lojas_data(search_term, uf, operadora)

    def search_servicos_data(self):
        search_term = self.search_servicos.get()
        uf = self.uf_serv_var.get()
        operadora = self.operadora_serv_var.get()
        self.load_servicos_data(search_term, uf, operadora)

    def gerar_carimbo_loja(self):
        selected = self.tree_lojas.selection()
        if not selected:
            messagebox.showwarning("Seleção necessária", "Selecione uma loja para gerar o carimbo.")
            return
        values = self.tree_lojas.item(selected[0], 'values')
        peop = values[1]
        # Buscar todos os links do inventário correspondente
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        cursor.execute("SELECT operadora, circuito_designacao, novo_circuito_designacao, id_vivo, novo_id_vivo FROM servicos_internet WHERE people=? OR people=? OR people=?", (peop, 'L'+peop, 'VD'+peop))
        rows_inv = cursor.fetchall()
        conn.close()
        # Se houver múltiplos links, pedir seleção
        link_idx = 0
        incluir_todos = False
        if len(rows_inv) > 1:
            sel_popup = tk.Toplevel(self.root)
            sel_popup.title("Selecione o link/operadora")
            sel_popup.resizable(False, False)
            sel_popup.grab_set()
            sel_popup.focus_set()
            tk.Label(sel_popup, text="Selecione o link/operadora para o carimbo:", font=("Arial", 12, "bold")).pack(padx=10, pady=8)
            # Cabeçalho de colunas
            header = tk.Frame(sel_popup)
            header.pack(padx=10, pady=(0, 2))
            for col, w in zip(["Operadora", "Circuito", "Novo Circuito", "ID VIVO", "Novo ID"], [14, 18, 18, 14, 14]):
                tk.Label(header, text=col, font=("Arial", 10, "bold"), width=w, anchor="w").pack(side="left")
            var = tk.IntVar(value=0)
            for idx, row in enumerate(rows_inv):
                row_frame = tk.Frame(sel_popup)
                row_frame.pack(padx=10, pady=1, fill="x")
                tk.Radiobutton(row_frame, variable=var, value=idx).pack(side="left")
                for val, w in zip(row, [14, 18, 18, 14, 14]):
                    tk.Label(row_frame, text=val, font=("Arial", 10), width=w, anchor="w").pack(side="left")
            var_todos = tk.BooleanVar()
            def marcar_todos():
                var.set(-1)
                var_todos.set(True)
            todos_frame = tk.Frame(sel_popup)
            todos_frame.pack(padx=10, pady=8, fill="x")
            tk.Checkbutton(todos_frame, text="Incluir todos os links (tabela)", variable=var_todos, font=("Arial", 11, "bold"), fg="#1976d2", command=marcar_todos).pack(side="left")
            def confirmar():
                nonlocal link_idx, incluir_todos
                link_idx = var.get()
                incluir_todos = var_todos.get()
                sel_popup.destroy()
            btn_conf = tk.Button(sel_popup, text="Confirmar", bg="#1976d2", fg="#fff", font=("Arial", 11, "bold"), padx=10, pady=4, command=confirmar)
            btn_conf.pack(pady=(0, 10))
            self.root.wait_window(sel_popup)
        # Montar carimbo_texto e HTML
        if rows_inv and (incluir_todos or link_idx == -1):
            # Tabela de todos os links
            tabela_links = "\n".join([
                f"Operadora: {r[0]} | Circuito: {r[1]} | Novo Circuito: {r[2]} | ID VIVO: {r[3]} | Novo ID: {r[4]}" for r in rows_inv
            ])
            tabela_html = "".join([
                f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>" for r in rows_inv
            ])
            carimbo_texto = f"""
PEOP: {values[1]}
LOJAS: {values[2]}
ENDEREÇO: {values[3]}
BAIRRO: {values[4]}
CIDADE: {values[5]}
UF: {values[6]}
CEP: {values[7]}
VD NOVO: {values[12]}
{tabela_links}
2ª a 6ª: {values[8]}
SAB / DOM: {values[9]} / {values[10]}
FUNC.: {values[11]}

----------------------------------------
CONTATO COMMAND CENTER
Telefone: (11) 3274-7527
E-mail: central.comando@dpsp.com.br

MENSAGEM DE ABERTURA DE CHAMADO NOS PORTAIS
LOJA VD {values[1]} FAVOR LIGAR PARA CONFIRMAR A NORMALIZAÇÃO E LIBERAÇÃO DE ACESSO COM A CENTRAL DE COMANDO | HORÁRIO DE FUNCIONAMENTO: 24 HORAS | SÁB 24 HORAS | DOM 24 HORAS
"""
        else:
            if rows_inv:
                operadora, circuito, novo_circuito, id_vivo, novo_id_vivo = rows_inv[link_idx]
            else:
                operadora = circuito = novo_circuito = id_vivo = novo_id_vivo = ''
            carimbo_texto = f"""
PEOP: {values[1]}
LOJAS: {values[2]}
ENDEREÇO: {values[3]}
BAIRRO: {values[4]}
CIDADE: {values[5]}
UF: {values[6]}
CEP: {values[7]}
VD NOVO: {values[12]}
Operadora: {operadora}
Circuito/Designação: {circuito}
Novo Circuito/Designação: {novo_circuito}
ID VIVO: {id_vivo}
Novo ID Vivo: {novo_id_vivo}
2ª a 6ª: {values[8]}
SAB / DOM: {values[9]} / {values[10]}
FUNC.: {values[11]}

----------------------------------------
CONTATO COMMAND CENTER
Telefone: (11) 3274-7527
E-mail: central.comando@dpsp.com.br

MENSAGEM DE ABERTURA DE CHAMADO NOS PORTAIS
LOJA VD {values[1]} FAVOR LIGAR PARA CONFIRMAR A NORMALIZAÇÃO E LIBERAÇÃO DE ACESSO COM A CENTRAL DE COMANDO | HORÁRIO DE FUNCIONAMENTO: 24 HORAS | SÁB 24 HORAS | DOM 24 HORAS
"""
        print("[DEBUG] carimbo_texto:")
        print(carimbo_texto)
        # Proteção contra múltiplos popups
        if getattr(self, 'popup_aberto', False):
            return
        self.popup_aberto = True
        top = tk.Toplevel(self.root)
        top.title("Carimbo - Relação de Lojas + Inventário")
        top.geometry("900x700")
        top.minsize(700, 500)
        top.resizable(True, True)
        top.configure(bg="#f4f6fa")
        def on_close():
            self.popup_aberto = False
            top.destroy()
        top.protocol("WM_DELETE_WINDOW", on_close)
        # Título com linha divisória
        title_font = tkfont.Font(family="Arial", size=22, weight="bold")
        title_label = tk.Label(top, text="Relação de Lojas + Inventário", font=title_font, bg="#b4d2ff", fg="#222", anchor="center", pady=8)
        title_label.pack(fill="x", pady=(10, 0))
        tk.Frame(top, height=2, bg="#d0d7e5").pack(fill="x", pady=(0, 8))
        # Frame principal horizontal
        main_frame = tk.Frame(top, bg="#f4f6fa")
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        # Frame lateral de botões
        btn_frame = tk.Frame(main_frame, bg="#f4f6fa")
        btn_frame.pack(side="left", fill="y", padx=(0, 0), pady=0)
        # Ícones (usando emojis para simplicidade)
        gmail_icon = "✉️ "
        outlook_icon = "📧 "
        # Estilo dos botões
        def style_btn(widget, color, hover_color):
            widget.configure(relief="flat", bd=0, highlightthickness=0, font=("Arial", 12, "bold"), fg="#fff", bg=color, activebackground=hover_color, activeforeground="#fff", cursor="hand2")
            widget.bind("<Enter>", lambda e: widget.config(bg=hover_color))
            widget.bind("<Leave>", lambda e: widget.config(bg=color))
            widget.configure(borderwidth=0, highlightbackground=color, highlightcolor=color)
            widget.configure(width=22, height=2)
        # Função para enviar por e-mail (Gmail/SMTP)
        def enviar_email_smtp():
            try:
                destinatario = 'operacionaldpsp@gmail.com'
                assunto = f"{values[1]} | {values[2]} - Link Inoperante"
                corpo_html = f"""
                <html><body>
                <h2 style='color:#1976d2;'>Carimbo de Loja</h2>
                <pre style='font-size:15px;font-family:Consolas,monospace;background:#f4f6fa;padding:10px;border-radius:8px;'>{carimbo_texto}</pre>
                <p style='color:#888;font-size:13px;'>Enviado automaticamente pelo sistema de consulta.</p>
                </body></html>
                """
                msg = MIMEMultipart()
                msg['From'] = 'OperacionalDPSP@gmail.com'
                msg['To'] = destinatario
                msg['Subject'] = assunto
                msg.attach(MIMEText(corpo_html, 'html'))
                # Anexar PNG
                png_path = f"carimbos/carimbo_loja_{values[1]}.png"
                if os.path.exists(png_path):
                    with open(png_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="carimbo_loja_{values[1]}.png"')
                    msg.attach(part)
                # Enviar
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login('OperacionalDPSP@gmail.com', 'mxqi oerj ndda edvx')
                server.send_message(msg)
                server.quit()
                messagebox.showinfo("E-mail enviado", "O carimbo foi enviado por e-mail com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro ao enviar e-mail", f"Erro: {e}")
        # Botão Gmail/SMTP
        btn_email_smtp = tk.Button(btn_frame, text=gmail_icon+"Enviar por E-mail (Gmail/SMTP)", command=enviar_email_smtp)
        style_btn(btn_email_smtp, "#1976d2", "#1565c0")
        btn_email_smtp.pack(pady=(30, 12), padx=18)
        add_tooltip(btn_email_smtp, "Envia o carimbo por e-mail usando Gmail/SMTP")
        # Função para enviar por e-mail (Outlook Desktop)
        def enviar_email_outlook():
            try:
                import win32com.client
                import os
                outlook = win32com.client.Dispatch('outlook.application')
                mail = outlook.CreateItem(0)
                mail.To = 'operacionaldpsp@gmail.com'
                mail.Subject = f"{values[1]} | {values[2]} - Link Inoperante"
                mail.Body = carimbo_texto
                png_path = f"carimbos/carimbo_loja_{values[1]}.png"
                if os.path.exists(png_path):
                    mail.Attachments.Add(os.path.abspath(png_path))
                mail.Display()  # Abre a janela do e-mail para revisão
            except Exception as e:
                messagebox.showerror("Erro ao enviar via Outlook", f"Erro: {e}\nVerifique se o Outlook Desktop está instalado e configurado.")
        # Botão Outlook
        btn_email_outlook = tk.Button(btn_frame, text=outlook_icon+"Enviar por E-mail (Outlook)", command=enviar_email_outlook)
        style_btn(btn_email_outlook, "#43a047", "#388e3c")
        btn_email_outlook.pack(pady=(0, 12), padx=18)
        add_tooltip(btn_email_outlook, "Envia o carimbo por e-mail usando Outlook Desktop")
        # Separador vertical
        tk.Frame(main_frame, width=2, bg="#d0d7e5").pack(side="left", fill="y", padx=(0, 0), pady=0)
        # Frame para imagem/texto do carimbo
        carimbo_frame = tk.Frame(main_frame, bg="#f4f6fa")
        carimbo_frame.pack(side="left", fill="both", expand=True)
        img_tk = None
        if not carimbo_texto.strip():
            tk.Label(carimbo_frame, text="[ERRO] carimbo_texto está vazio!", fg="red").pack(pady=10)
        else:
            try:
                img = self.gerar_png_carimbo(carimbo_texto, f"carimbo_loja_{values[1]}.png", return_image=True)
                max_width = 500
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height))
                # Reduzir fonte apenas para visualização (não afeta PNG salvo)
                # (Não é possível alterar fonte da imagem já gerada, mas a imagem ficará menor)
                img_tk = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"[ERRO ao gerar imagem do carimbo]: {e}")
                tk.Label(carimbo_frame, text=f"Erro ao carregar imagem: {e}", fg="red").pack()
        if img_tk:
            canvas = tk.Canvas(carimbo_frame, width=img_tk.width(), height=img_tk.height(), bd=0, highlightthickness=0)
            h_scroll = tk.Scrollbar(carimbo_frame, orient="horizontal", command=canvas.xview)
            canvas.configure(xscrollcommand=h_scroll.set)
            canvas.pack(padx=2, pady=5, fill="both", expand=True)
            h_scroll.pack(fill="x")
            canvas.create_image(0, 0, anchor="nw", image=img_tk)
            canvas.config(scrollregion=canvas.bbox("all"))
            canvas.image = img_tk
        elif carimbo_texto.strip():
            tk.Label(carimbo_frame, text="[Carimbo não gerado - veja o texto abaixo]", fg="red").pack(pady=10)
            text_box = tk.Text(carimbo_frame, height=20, width=60, font=("Consolas", 9))
            text_box.insert("1.0", carimbo_texto)
            text_box.config(state="disabled")
            text_box.pack(padx=2, pady=5)
        png_path = f"carimbos/carimbo_loja_{values[1]}.png"
        tk.Label(carimbo_frame, text=f"PNG salvo como carimbo_loja_{values[1]}.png", fg="#555").pack(pady=(0, 10))

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
        peop = values[0]
        # Buscar todos os links do inventário para esse People
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        cursor.execute("SELECT operadora, circuito_designacao, novo_circuito_designacao, id_vivo, novo_id_vivo FROM servicos_internet WHERE people=? OR people=? OR people=?", (peop, 'L'+peop, 'VD'+peop))
        rows_inv = cursor.fetchall()
        # Buscar dados da loja correspondente
        cursor.execute("SELECT nome, endereco, bairro, cidade, uf, cep, vd_novo, horario_semana, horario_sabado, horario_domingo, funcionamento FROM lojas WHERE peop=? OR peop=?", (peop, 'VD'+peop))
        row_loja = cursor.fetchone()
        conn.close()
        if row_loja:
            nome, endereco, bairro, cidade, uf, cep, vd_novo, horario_semana, horario_sabado, horario_domingo, funcionamento = row_loja
        else:
            nome = endereco = bairro = cidade = uf = cep = vd_novo = horario_semana = horario_sabado = horario_domingo = funcionamento = ''
        # Se houver múltiplos links, pedir seleção
        link_idx = 0
        incluir_todos = False
        if len(rows_inv) > 1:
            sel_popup = tk.Toplevel(self.root)
            sel_popup.title("Selecione o link/operadora")
            sel_popup.resizable(False, False)
            sel_popup.grab_set()
            sel_popup.focus_set()
            tk.Label(sel_popup, text="Selecione o link/operadora para o carimbo:", font=("Arial", 12, "bold")).pack(padx=10, pady=8)
            # Cabeçalho de colunas
            header = tk.Frame(sel_popup)
            header.pack(padx=10, pady=(0, 2))
            for col, w in zip(["Operadora", "Circuito", "Novo Circuito", "ID VIVO", "Novo ID"], [14, 18, 18, 14, 14]):
                tk.Label(header, text=col, font=("Arial", 10, "bold"), width=w, anchor="w").pack(side="left")
            var = tk.IntVar(value=0)
            for idx, row in enumerate(rows_inv):
                row_frame = tk.Frame(sel_popup)
                row_frame.pack(padx=10, pady=1, fill="x")
                tk.Radiobutton(row_frame, variable=var, value=idx).pack(side="left")
                for val, w in zip(row, [14, 18, 18, 14, 14]):
                    tk.Label(row_frame, text=val, font=("Arial", 10), width=w, anchor="w").pack(side="left")
            var_todos = tk.BooleanVar()
            def marcar_todos():
                var.set(-1)
                var_todos.set(True)
            todos_frame = tk.Frame(sel_popup)
            todos_frame.pack(padx=10, pady=8, fill="x")
            tk.Checkbutton(todos_frame, text="Incluir todos os links (tabela)", variable=var_todos, font=("Arial", 11, "bold"), fg="#1976d2", command=marcar_todos).pack(side="left")
            def confirmar():
                nonlocal link_idx, incluir_todos
                link_idx = var.get()
                incluir_todos = var_todos.get()
                sel_popup.destroy()
            btn_conf = tk.Button(sel_popup, text="Confirmar", bg="#1976d2", fg="#fff", font=("Arial", 11, "bold"), padx=10, pady=4, command=confirmar)
            btn_conf.pack(pady=(0, 10))
            self.root.wait_window(sel_popup)
        # Montar carimbo_texto e HTML
        if rows_inv and (incluir_todos or link_idx == -1):
            tabela_links = "\n".join([
                f"Operadora: {r[0]} | Circuito: {r[1]} | Novo Circuito: {r[2]} | ID VIVO: {r[3]} | Novo ID: {r[4]}" for r in rows_inv
            ])
            tabela_html = "".join([
                f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>" for r in rows_inv
            ])
            carimbo_texto = f"""
PEOP: {peop}
LOJAS: {nome}
ENDEREÇO: {endereco}
BAIRRO: {bairro}
CIDADE: {cidade}
UF: {uf}
CEP: {cep}
VD NOVO: {vd_novo}
{tabela_links}
2ª a 6ª: {horario_semana}
SAB / DOM: {horario_sabado} / {horario_domingo}
FUNC.: {funcionamento}

----------------------------------------
CONTATO COMMAND CENTER
Telefone: (11) 3274-7527
E-mail: central.comando@dpsp.com.br

MENSAGEM DE ABERTURA DE CHAMADO NOS PORTAIS
LOJA VD {peop} FAVOR LIGAR PARA CONFIRMAR A NORMALIZAÇÃO E LIBERAÇÃO DE ACESSO COM A CENTRAL DE COMANDO | HORÁRIO DE FUNCIONAMENTO: 24 HORAS | SÁB 24 HORAS | DOM 24 HORAS
"""
        else:
            if rows_inv:
                operadora, circuito, novo_circuito, id_vivo, novo_id_vivo = rows_inv[link_idx]
            else:
                operadora = circuito = novo_circuito = id_vivo = novo_id_vivo = ''
            carimbo_texto = f"""
PEOP: {peop}
LOJAS: {nome}
ENDEREÇO: {endereco}
BAIRRO: {bairro}
CIDADE: {cidade}
UF: {uf}
CEP: {cep}
VD NOVO: {vd_novo}
Operadora: {operadora}
Circuito/Designação: {circuito}
Novo Circuito/Designação: {novo_circuito}
ID VIVO: {id_vivo}
Novo ID Vivo: {novo_id_vivo}
2ª a 6ª: {horario_semana}
SAB / DOM: {horario_sabado} / {horario_domingo}
FUNC.: {funcionamento}

----------------------------------------
CONTATO COMMAND CENTER
Telefone: (11) 3274-7527
E-mail: central.comando@dpsp.com.br

MENSAGEM DE ABERTURA DE CHAMADO NOS PORTAIS
LOJA VD {peop} FAVOR LIGAR PARA CONFIRMAR A NORMALIZAÇÃO E LIBERAÇÃO DE ACESSO COM A CENTRAL DE COMANDO | HORÁRIO DE FUNCIONAMENTO: 24 HORAS | SÁB 24 HORAS | DOM 24 HORAS
"""
        print("[DEBUG] carimbo_texto:")
        print(carimbo_texto)
        # Proteção contra múltiplos popups
        if getattr(self, 'popup_aberto', False):
            return
        self.popup_aberto = True
        top = tk.Toplevel(self.root)
        top.title("Carimbo - Inventário + Loja")
        top.geometry("900x700")
        top.minsize(700, 500)
        top.resizable(True, True)
        def on_close():
            self.popup_aberto = False
            top.destroy()
        top.protocol("WM_DELETE_WINDOW", on_close)
        # Título com linha divisória
        title_font = tkfont.Font(family="Arial", size=22, weight="bold")
        title_label = tk.Label(top, text="Inventário + Relação de Lojas", font=title_font, bg="#b4d2ff", fg="#222", anchor="center", pady=8)
        title_label.pack(fill="x", pady=(10, 0))
        tk.Frame(top, height=2, bg="#d0d7e5").pack(fill="x", pady=(0, 8))
        # Frame principal horizontal
        main_frame = tk.Frame(top, bg="#f4f6fa")
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        # Frame lateral de botões
        btn_frame = tk.Frame(main_frame, bg="#f4f6fa")
        btn_frame.pack(side="left", fill="y", padx=(0, 0), pady=0)
        # Ícones (usando emojis para simplicidade)
        gmail_icon = "✉️ "
        outlook_icon = "📧 "
        # Estilo dos botões
        def style_btn(widget, color, hover_color):
            widget.configure(relief="flat", bd=0, highlightthickness=0, font=("Arial", 12, "bold"), fg="#fff", bg=color, activebackground=hover_color, activeforeground="#fff", cursor="hand2")
            widget.bind("<Enter>", lambda e: widget.config(bg=hover_color))
            widget.bind("<Leave>", lambda e: widget.config(bg=color))
            widget.configure(borderwidth=0, highlightbackground=color, highlightcolor=color)
            widget.configure(width=22, height=2)
        # Função para enviar por e-mail (Gmail/SMTP)
        def enviar_email_smtp():
            try:
                destinatario = 'operacionaldpsp@gmail.com'
                assunto = f"{peop} | {nome} - Link Inoperante"
                corpo_html = f"""
                <html><body>
                <h2 style='color:#1976d2;'>Carimbo de Loja</h2>
                <pre style='font-size:15px;font-family:Consolas,monospace;background:#f4f6fa;padding:10px;border-radius:8px;'>{carimbo_texto}</pre>
                <p style='color:#888;font-size:13px;'>Enviado automaticamente pelo sistema de consulta.</p>
                </body></html>
                """
                msg = MIMEMultipart()
                msg['From'] = 'OperacionalDPSP@gmail.com'
                msg['To'] = destinatario
                msg['Subject'] = assunto
                msg.attach(MIMEText(corpo_html, 'html'))
                # Anexar PNG
                png_path = f"carimbos/carimbo_inventario_{peop}.png"
                if os.path.exists(png_path):
                    with open(png_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="carimbo_inventario_{peop}.png"')
                    msg.attach(part)
                # Enviar
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login('OperacionalDPSP@gmail.com', 'mxqi oerj ndda edvx')
                server.send_message(msg)
                server.quit()
                messagebox.showinfo("E-mail enviado", "O carimbo foi enviado por e-mail com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro ao enviar e-mail", f"Erro: {e}")
        # Botão Gmail/SMTP
        btn_email_smtp = tk.Button(btn_frame, text=gmail_icon+"Enviar por E-mail (Gmail/SMTP)", command=enviar_email_smtp)
        style_btn(btn_email_smtp, "#1976d2", "#1565c0")
        btn_email_smtp.pack(pady=(30, 12), padx=18)
        add_tooltip(btn_email_smtp, "Envia o carimbo por e-mail usando Gmail/SMTP")
        # Função para enviar por e-mail (Outlook Desktop)
        def enviar_email_outlook():
            try:
                import win32com.client
                import os
                outlook = win32com.client.Dispatch('outlook.application')
                mail = outlook.CreateItem(0)
                mail.To = 'operacionaldpsp@gmail.com'
                mail.Subject = f"{peop} | {nome} - Link Inoperante"
                mail.Body = carimbo_texto
                png_path = f"carimbos/carimbo_inventario_{peop}.png"
                if os.path.exists(png_path):
                    mail.Attachments.Add(os.path.abspath(png_path))
                mail.Display()  # Abre a janela do e-mail para revisão
            except Exception as e:
                messagebox.showerror("Erro ao enviar via Outlook", f"Erro: {e}\nVerifique se o Outlook Desktop está instalado e configurado.")
        # Botão Outlook
        btn_email_outlook = tk.Button(btn_frame, text=outlook_icon+"Enviar por E-mail (Outlook)", command=enviar_email_outlook)
        style_btn(btn_email_outlook, "#43a047", "#388e3c")
        btn_email_outlook.pack(pady=(0, 12), padx=18)
        add_tooltip(btn_email_outlook, "Envia o carimbo por e-mail usando Outlook Desktop")
        # Separador vertical
        tk.Frame(main_frame, width=2, bg="#d0d7e5").pack(side="left", fill="y", padx=(0, 0), pady=0)
        # Frame para imagem/texto do carimbo
        carimbo_frame = tk.Frame(main_frame, bg="#f4f6fa")
        carimbo_frame.pack(side="left", fill="both", expand=True)
        img_tk = None
        if not carimbo_texto.strip():
            tk.Label(carimbo_frame, text="[ERRO] carimbo_texto está vazio!", fg="red").pack(pady=10)
        else:
            try:
                img = self.gerar_png_carimbo(carimbo_texto, f"carimbo_inventario_{peop}.png", return_image=True)
                max_width = 500
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height))
                # Reduzir fonte apenas para visualização (não afeta PNG salvo)
                # (Não é possível alterar fonte da imagem já gerada, mas a imagem ficará menor)
                img_tk = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"[ERRO ao gerar imagem do carimbo]: {e}")
                tk.Label(carimbo_frame, text=f"Erro ao carregar imagem: {e}", fg="red").pack()
        if img_tk:
            canvas = tk.Canvas(carimbo_frame, width=img_tk.width(), height=img_tk.height(), bd=0, highlightthickness=0)
            h_scroll = tk.Scrollbar(carimbo_frame, orient="horizontal", command=canvas.xview)
            canvas.configure(xscrollcommand=h_scroll.set)
            canvas.pack(padx=2, pady=5, fill="both", expand=True)
            h_scroll.pack(fill="x")
            canvas.create_image(0, 0, anchor="nw", image=img_tk)
            canvas.config(scrollregion=canvas.bbox("all"))
            canvas.image = img_tk
        elif carimbo_texto.strip():
            tk.Label(carimbo_frame, text="[Carimbo não gerado - veja o texto abaixo]", fg="red").pack(pady=10)
            text_box = tk.Text(carimbo_frame, height=20, width=60, font=("Consolas", 9))
            text_box.insert("1.0", carimbo_texto)
            text_box.config(state="disabled")
            text_box.pack(padx=2, pady=5)
        png_path = f"carimbos/carimbo_inventario_{peop}.png"
        tk.Label(carimbo_frame, text=f"PNG salvo como carimbo_inventario_{peop}.png", fg="#555").pack(pady=(0, 10))

    def export_lojas_csv(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not file:
            return
        search_term = self.search_lojas.get()
        uf = self.uf_var.get()
        operadora = self.operadora_var.get()
        conn = sqlite3.connect('inventario.db')
        query = """
            SELECT l.status, 
                   CASE 
                       WHEN l.peop LIKE 'L%' THEN substr(l.peop, 2)
                       WHEN l.peop LIKE 'VD%' THEN substr(l.peop, 3)
                       ELSE l.peop 
                   END as peop,
                   l.nome, l.endereco, l.bairro, l.cidade, l.uf, l.cep,
                   l.horario_semana, l.horario_sabado, l.horario_domingo, l.funcionamento, l.vd_novo
            FROM lojas l
            LEFT JOIN servicos_internet s ON l.peop = s.people OR l.peop = substr(s.people,2) OR l.peop = substr(s.people,3)
        """
        where = []
        params = []
        if search_term:
            where.append("(l.nome LIKE ? OR l.peop LIKE ? OR l.endereco LIKE ? OR l.cidade LIKE ? OR l.bairro LIKE ? OR s.operadora LIKE ? OR s.circuito_designacao LIKE ?)")
            for _ in range(7):
                params.append(f"%{search_term}%")
        if uf:
            where.append("l.uf = ?")
            params.append(uf)
        if operadora:
            where.append("s.operadora = ?")
            params.append(operadora)
        if where:
            query += " WHERE " + " AND ".join(where)
        query += " GROUP BY l.peop LIMIT 1000"
        df = pd.read_sql_query(query, conn, params=params)
        df.to_csv(file, index=False, encoding='utf-8-sig')
        conn.close()
        messagebox.showinfo("Exportação", f"Arquivo salvo em: {file}")

    def export_servicos_csv(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not file:
            return
        search_term = self.search_servicos.get()
        uf = self.uf_serv_var.get()
        operadora = self.operadora_serv_var.get()
        conn = sqlite3.connect('inventario.db')
        query = """
            SELECT s.people, s.operadora, s.circuito_designacao, s.novo_circuito_designacao, s.id_vivo, s.novo_id_vivo, l.uf
            FROM servicos_internet s
            LEFT JOIN lojas l ON s.people = l.peop OR s.people = 'L' || l.peop OR s.people = 'VD' || l.peop
        """
        where = []
        params = []
        if search_term:
            where.append("(s.people LIKE ? OR s.operadora LIKE ? OR s.circuito_designacao LIKE ? OR s.novo_circuito_designacao LIKE ? OR s.id_vivo LIKE ? OR l.nome LIKE ? OR l.cidade LIKE ?)")
            for _ in range(7):
                params.append(f"%{search_term}%")
        if uf:
            where.append("l.uf = ?")
            params.append(uf)
        if operadora:
            where.append("s.operadora = ?")
            params.append(operadora)
        if where:
            query += " WHERE " + " AND ".join(where)
        query += " GROUP BY s.people, s.operadora, s.circuito_designacao LIMIT 1000"
        df = pd.read_sql_query(query, conn, params=params)
        df.to_csv(file, index=False, encoding='utf-8-sig')
        conn.close()
        messagebox.showinfo("Exportação", f"Arquivo salvo em: {file}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop() 