# Documentação do Projeto - Sistema de Consulta de Lojas e Inventário

## 1. Visão Geral do Projeto
O projeto é um sistema desktop desenvolvido em Python para consulta, geração de carimbos e comunicação de informações de lojas e inventário. O sistema permite exportação em PNG e envio por e-mail (HTML colorido ou anexo).

## 2. Funcionalidades Implementadas

### 2.1 Interface Gráfica
- Interface desenvolvida com Tkinter
- Sistema de temas claro/escuro
- Abas separadas para Lojas e Inventário
- Tooltips informativos
- Filtros e busca avançada
- Visualização em tabela com scroll horizontal e vertical

### 2.2 Consulta de Dados
- Consulta integrada ao banco SQLite
- Filtros por:
  - UF
  - Operadora
  - Busca textual
- Exportação para CSV
- Visualização em tabela organizada

### 2.3 Geração de Carimbos
- Geração de carimbos visuais em PNG
- Layout colorido seguindo padrão corporativo
- Pré-visualização no aplicativo
- Exportação automática para pasta `carimbos/`
- Suporte a diferentes tipos de carimbos (Lojas e Inventário)

### 2.4 Sistema de E-mail
- Duas opções de envio:
  - SMTP (Gmail)
  - Outlook
- Múltiplos formatos de envio:
  - Anexo PNG
  - Corpo do e-mail em HTML colorido
- Interface amigável para envio

## 3. Cronograma de Implementação

### Fase 1 - Estrutura Base (Concluído)
- [x] Configuração do ambiente
- [x] Estrutura do banco de dados
- [x] Interface básica
- [x] Conexão com banco de dados

### Fase 2 - Funcionalidades Principais (Concluído)
- [x] Sistema de consulta
- [x] Geração de carimbos
- [x] Exportação PNG
- [x] Sistema de e-mail básico

### Fase 3 - Melhorias de Interface (Concluído)
- [x] Sistema de temas
- [x] Tooltips
- [x] Filtros avançados
- [x] Exportação CSV

### Fase 4 - Otimizações (Concluído)
- [x] Melhorias de performance
- [x] Tratamento de erros
- [x] Documentação básica
- [x] Scripts de inicialização

## 4. Pendências e Melhorias Futuras

### 4.1 Melhorias de Interface
- [ ] Implementar sistema de atalhos de teclado
- [ ] Adicionar mais opções de personalização de tema
- [ ] Melhorar responsividade em diferentes resoluções
- [ ] Adicionar sistema de favoritos/marcadores

### 4.2 Funcionalidades
- [ ] Implementar sistema de backup automático
- [ ] Adicionar suporte a mais formatos de exportação
- [ ] Implementar sistema de relatórios personalizados
- [ ] Adicionar suporte a múltiplos idiomas

### 4.3 Segurança
- [ ] Implementar sistema de login
- [ ] Adicionar criptografia para dados sensíveis
- [ ] Melhorar segurança no envio de e-mails
- [ ] Implementar logs de atividades

### 4.4 Performance
- [ ] Otimizar consultas ao banco de dados
- [ ] Implementar cache de dados
- [ ] Melhorar tempo de carregamento inicial
- [ ] Otimizar geração de carimbos

## 5. Estrutura do Projeto

### 5.1 Arquivos Principais
- `app.py`: Aplicação principal
- `database.py`: Gerenciamento do banco de dados
- `send_mail_smtp.py`: Configuração de e-mail SMTP
- `send_mail_outlook.py`: Configuração de e-mail Outlook
- `requirements.txt`: Dependências do projeto

### 5.2 Diretórios
- `carimbos/`: Armazenamento de carimbos gerados
- `Excel/`: Arquivos de dados em Excel
- `.venv/`: Ambiente virtual Python

## 6. Requisitos Técnicos

### 6.1 Software
- Python 3.10+
- SQLite3
- Dependências listadas em `requirements.txt`

### 6.2 Hardware
- Processador: 1.6 GHz ou superior
- Memória RAM: 4GB ou superior
- Espaço em disco: 100MB livres

## 7. Instalação e Configuração

### 7.1 Requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Acesso à internet para instalação de dependências

### 7.2 Passos de Instalação
1. Clonar o repositório
2. Criar ambiente virtual: `python -m venv .venv`
3. Ativar ambiente virtual
4. Instalar dependências: `pip install -r requirements.txt`
5. Executar aplicação: `python app.py` ou `iniciar_app.bat`

## 8. Suporte e Manutenção

### 8.1 Contato
Para suporte técnico ou dúvidas, abra uma issue no repositório do projeto.

### 8.2 Manutenção
- Atualizações regulares de dependências
- Backup periódico do banco de dados
- Monitoramento de logs
- Verificação de segurança 