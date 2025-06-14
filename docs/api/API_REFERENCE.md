# Referência da API

## Visão Geral

Este documento descreve as principais funções e classes disponíveis no sistema para desenvolvedores que desejam estender ou integrar com o projeto.

## Módulos Principais

### 1. Database (database.py)

#### Classes
```python
class Database:
    def __init__(self, db_path: str)
    def get_lojas(self, search_term: str = "", uf: str = "", operadora: str = "") -> pd.DataFrame
    def get_servicos(self, search_term: str = "", uf: str = "", operadora: str = "") -> pd.DataFrame
    def get_unique_values(self, table: str, column: str) -> list
```

#### Exemplo de Uso
```python
from database import Database

db = Database("inventario.db")
lojas = db.get_lojas(search_term="São Paulo", uf="SP")
```

### 2. Email (send_mail_smtp.py, send_mail_outlook.py)

#### Funções SMTP
```python
def send_email_smtp(
    to_email: str,
    subject: str,
    body: str,
    attachment_path: str = None,
    gmail_user: str = None,
    gmail_password: str = None
) -> bool
```

#### Funções Outlook
```python
def send_email_outlook(
    to_email: str,
    subject: str,
    body: str,
    attachment_path: str = None
) -> bool
```

#### Exemplo de Uso
```python
from send_mail_smtp import send_email_smtp

success = send_email_smtp(
    to_email="destinatario@email.com",
    subject="Teste",
    body="Corpo do e-mail",
    attachment_path="carimbo.png"
)
```

### 3. Carimbo (app.py)

#### Funções
```python
def gerar_png_carimbo(
    texto: str,
    filename: str,
    return_image: bool = False
) -> Union[None, Image.Image]

def gerar_carimbo_loja(self) -> None
def gerar_carimbo_inventario(self) -> None
```

#### Exemplo de Uso
```python
from app import DatabaseApp

app = DatabaseApp(root)
app.gerar_png_carimbo("Texto do carimbo", "carimbo.png")
```

## Estrutura de Dados

### 1. Tabela de Lojas
```sql
CREATE TABLE lojas (
    id INTEGER PRIMARY KEY,
    status TEXT,
    peop TEXT,
    nome TEXT,
    endereco TEXT,
    bairro TEXT,
    cidade TEXT,
    uf TEXT,
    cep TEXT,
    horario_semana TEXT,
    horario_sabado TEXT,
    horario_domingo TEXT,
    funcionamento TEXT,
    vd_novo TEXT
);
```

### 2. Tabela de Serviços
```sql
CREATE TABLE servicos_internet (
    id INTEGER PRIMARY KEY,
    operadora TEXT,
    status TEXT,
    peop TEXT,
    nome TEXT,
    endereco TEXT,
    bairro TEXT,
    cidade TEXT,
    uf TEXT,
    cep TEXT
);
```

## Eventos e Callbacks

### 1. Interface Principal
```python
def on_search(self, event=None)
def on_filter_change(self, event=None)
def on_theme_toggle(self)
```

### 2. Geração de Carimbos
```python
def on_carimbo_generate(self)
def on_carimbo_preview(self)
def on_carimbo_save(self)
```

## Extensibilidade

### 1. Adicionando Novos Tipos de Carimbos
1. Crie uma nova função de geração
2. Adicione o template correspondente
3. Integre com a interface

### 2. Adicionando Novos Métodos de Envio
1. Crie um novo módulo de e-mail
2. Implemente a função de envio
3. Adicione à interface

## Boas Práticas

### 1. Código
- Use type hints
- Documente funções e classes
- Siga o padrão PEP 8

### 2. Banco de Dados
- Use queries parametrizadas
- Implemente tratamento de erros
- Mantenha índices atualizados

### 3. Interface
- Mantenha consistência visual
- Implemente feedback de ações
- Trate erros graciosamente

## Exemplos de Integração

### 1. Adicionando Novo Filtro
```python
def add_custom_filter(self, filter_type: str, filter_value: str):
    if filter_type == "custom":
        self.custom_filter = filter_value
        self.refresh_data()
```

### 2. Personalizando Carimbo
```python
def customize_carimbo(self, template: str, data: dict):
    # Implementar lógica de personalização
    pass
```

## Troubleshooting

### 1. Problemas Comuns
- Erros de conexão com banco
- Falhas no envio de e-mail
- Problemas de geração de carimbos

### 2. Debug
- Use logging
- Implemente try/except
- Mantenha logs de erro 