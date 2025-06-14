# Arquitetura Técnica

## Visão Geral do Sistema

O sistema é construído em Python utilizando uma arquitetura modular com os seguintes componentes principais:

### 1. Interface Gráfica (GUI)
- Framework: Tkinter
- Componentes principais:
  - Notebook (abas) para separação de funcionalidades
  - Treeview para exibição de dados
  - Sistema de temas (claro/escuro)
  - Tooltips informativos

### 2. Banco de Dados
- Sistema: SQLite3
- Arquivo: `inventario.db`
- Tabelas principais:
  - lojas
  - servicos_internet
  - inventario

### 3. Geração de Carimbos
- Biblioteca: PIL (Python Imaging Library)
- Funcionalidades:
  - Geração de imagens PNG
  - Layout corporativo
  - Suporte a diferentes tipos de carimbos

### 4. Sistema de E-mail
- Múltiplos métodos de envio:
  - SMTP (Gmail)
  - Outlook (via win32com)
- Formatos suportados:
  - Anexo PNG
  - HTML colorido

## Fluxo de Dados

1. **Consulta de Dados**
   ```
   Interface -> Database.py -> SQLite -> Interface
   ```

2. **Geração de Carimbos**
   ```
   Interface -> Database.py -> Gerador de Carimbos -> PNG/Email
   ```

3. **Envio de E-mail**
   ```
   Interface -> Gerador de Carimbos -> Sistema de Email -> Destinatário
   ```

## Dependências Principais

- **GUI e Sistema Base**
  - tkinter
  - ttk
  - PIL (Pillow)
  - pandas

- **Banco de Dados**
  - sqlite3
  - pandas

- **E-mail**
  - smtplib
  - win32com.client
  - email.mime

## Estrutura de Arquivos

```
Projeto_02/
├── app.py              # Aplicação principal
├── database.py         # Gerenciamento do banco de dados
├── send_mail_smtp.py   # Configuração SMTP
├── send_mail_outlook.py # Configuração Outlook
├── carimbos/          # Diretório de carimbos gerados
└── Excel/             # Arquivos de dados
```

## Considerações de Performance

1. **Banco de Dados**
   - Índices otimizados para consultas frequentes
   - Queries parametrizadas para melhor performance
   - Cache de consultas frequentes

2. **Interface**
   - Carregamento lazy de dados
   - Paginação de resultados
   - Filtros otimizados

3. **Geração de Carimbos**
   - Processamento assíncrono
   - Cache de templates
   - Otimização de imagens

## Segurança

1. **Dados**
   - Validação de entrada
   - Sanitização de queries
   - Backup automático

2. **E-mail**
   - Autenticação segura
   - Criptografia de senhas
   - Validação de destinatários

## Logs e Monitoramento

1. **Sistema de Logs**
   - Logs de operações críticas
   - Rastreamento de erros
   - Monitoramento de performance

2. **Métricas**
   - Tempo de resposta
   - Uso de recursos
   - Taxa de erros 