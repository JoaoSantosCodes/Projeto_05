# Projeto de Backup e Automação

## Índice
- [Visão Geral](#visão-geral)
- [Configuração](#configuração)
- [Backup Automático](#backup-automático)
- [Criptografia dos Backups](#criptografia-dos-backups)
- [Verificação de Integridade dos Backups](#verificação-de-integridade-dos-backups)
- [Notificações Automáticas](#notificações-automáticas)
- [Logs e Monitoramento](#logs-e-monitoramento)
- [Interface CLI e Comandos](#interface-cli-e-comandos)
- [Roadmap Revisado do Projeto](#roadmap-revisado-do-projeto)

# Documentação do Projeto - Sistema de Consulta de Lojas e Inventário

> **Repositório oficial:** [github.com/JoaoSantosCodes/Projeto_02](https://github.com/JoaoSantosCodes/Projeto_02)
> 
> Status CI/CD: [Verificar pipeline](https://github.com/JoaoSantosCodes/Projeto_02/actions)

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

## Como contribuir e atualizar

- Faça um fork ou clone do repositório oficial.
- Crie uma branch para cada nova funcionalidade ou correção.
- Siga o padrão de commits (conventional commits).
- Sempre atualize sua branch com a `main` antes de abrir um Pull Request.
- Assegure que todos os testes e pipelines estejam passando antes de solicitar merge.

## Histórico e versionamento

- Todo o histórico de alterações está disponível no [GitHub](https://github.com/JoaoSantosCodes/Projeto_02/commits/main).
- Consulte o arquivo `CHANGELOG.md` para detalhes de cada versão.

## Estrutura de Pastas (Atualizada)

```
Projeto_02/
│
├── app/                  # Código-fonte principal do sistema
│   ├── database.py
│   ├── send_mail_smtp.py
│   ├── send_mail_outlook.py
│   ├── check_database.py
│   ├── inspect_excel_columns.py
│   └── ...
│
├── tests/                # Testes automatizados
├── docs/                 # Documentação
├── carimbos/             # Saída de carimbos gerados
├── Excel/                # Planilhas de entrada/saída
├── .github/              # Workflows e configs do GitHub Actions
├── app.py                # Script principal (ponto de entrada)
├── build.spec            # Configuração do PyInstaller
├── requirements.txt
├── pyproject.toml
├── README.md
├── LICENSE
├── iniciar_app.bat
└── inventario.db
```

> Para importar módulos internos do código-fonte, utilize:
> 
> ```python
> from app import database
> from app.send_mail_smtp import ...
> ```

---

> Documentação mantida e atualizada em [github.com/JoaoSantosCodes/Projeto_02](https://github.com/JoaoSantosCodes/Projeto_02)

> **Nota de Segurança:**
> Testes automatizados que utilizavam segredos (como CLIENT_SECRET e senhas de e-mail) foram removidos do repositório e do histórico para garantir a segurança do projeto. Sempre utilize variáveis de ambiente para testes que dependam de credenciais.

## Teste seguro de envio de e-mail

- O teste `tests/integration/test_send_mail.py` realiza o envio de e-mail de forma segura, utilizando variáveis de ambiente.
- Para rodar o teste, defina as variáveis:
  - `EMAIL_USER`
  - `EMAIL_PASSWORD`
  - `EMAIL_TEST_RECEIVER`
- Exemplo de `.env.example`:
  ```
  EMAIL_USER=seu_email@gmail.com
  EMAIL_PASSWORD=sua_senha_de_app_gmail
  EMAIL_TEST_RECEIVER=destinatario@exemplo.com
  ```
- O teste será ignorado se as variáveis não estiverem definidas.

## Sistema de Atualização Automática

### Visão Geral
O sistema de atualização automática (`auto_update.py`) é uma ferramenta robusta que mantém o repositório sincronizado com o GitHub, realizando commits e pushes automáticos em intervalos configuráveis.

### Arquitetura

#### Componentes Principais
1. **Script Principal** (`auto_update.py`)
   - Monitoramento de mudanças
   - Sistema de commit e push
   - Gerenciamento de logs
   - Tratamento de erros

2. **Sistema de Configuração** (`config.yaml`)
   - Intervalos de atualização
   - Configurações de e-mail
   - Parâmetros de backup
   - Limites de tentativas

3. **Sistema de Backup**
   - Backup automático antes de commits
   - Rotação de backups antigos
   - Ignorar arquivos desnecessários

4. **Sistema de Notificações**
   - Alertas por e-mail
   - Notificações de sucesso/erro
   - Configuração flexível

### Configuração

#### 1. Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_app_gmail
```

#### 2. Arquivo de Configuração
Configure o `config.yaml`:
```yaml
update:
  interval: 300  # 5 minutos
  max_retries: 3

notifications:
  email:
    enabled: true
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    sender_email: "seu_email@gmail.com"
    recipient_email: "destinatario@exemplo.com"
    subject_prefix: "[Auto-Update]"

backup:
  enabled: true
  directory: "backups"
  max_backups: 5
```

### Funcionalidades Detalhadas

#### Sistema de Backup
- Cria backup antes de cada commit
- Mantém histórico limitado de backups
- Ignora diretórios e arquivos desnecessários
- Rotação automática de backups antigos

#### Notificações por E-mail
- Alertas de sucesso/erro
- Configuração flexível de remetente/destinatário
- Uso seguro de credenciais
- Mensagens detalhadas com timestamps

#### Tratamento de Erros
- Sistema de retry configurável
- Logs detalhados de erros
- Notificações de falhas
- Recuperação automática

### Boas Práticas

#### Segurança
1. Nunca exponha credenciais no código
2. Use variáveis de ambiente para senhas
3. Mantenha backups regulares
4. Monitore os logs de erro

#### Manutenção
1. Verifique regularmente os logs
2. Limpe backups antigos quando necessário
3. Atualize as configurações conforme necessário
4. Mantenha as dependências atualizadas

#### Uso
1. Execute apenas quando necessário
2. Configure intervalos adequados
3. Monitore o uso de recursos
4. Verifique as notificações regularmente

### Troubleshooting

#### Problemas Comuns
1. **Erro de Autenticação**
   - Verifique as credenciais no `.env`
   - Confirme as configurações SMTP
   - Verifique as permissões de e-mail

2. **Falhas no Backup**
   - Verifique o espaço em disco
   - Confirme as permissões do diretório
   - Ajuste o número máximo de backups

3. **Erros de Git**
   - Verifique a conexão com o GitHub
   - Confirme as credenciais do Git
   - Verifique conflitos no repositório

### Logs e Monitoramento

#### Arquivos de Log
- `auto_update.log`: Log principal
- Logs de backup no diretório `backups/`
- Logs de erro no console

#### Monitoramento
- Verifique os logs regularmente
- Monitore o uso de recursos
- Acompanhe as notificações
- Verifique o status dos backups 

## Estrutura de Logs

O sistema agora gera logs organizados para facilitar auditoria e troubleshooting:

- `logs/auto_update_YYYY-MM-DD.log`: Log diário de todas as operações do dia.
- `logs/auto_update_errors.log`: Log separado apenas para erros críticos.
- Logs antigos são rotacionados automaticamente.

**Vantagens:**
- Facilita a busca por eventos de um dia específico.
- Permite auditoria rápida de falhas e problemas recorrentes.
- Mantém o diretório principal limpo. 

## Verificação de Integridade dos Backups

- Cada backup criado agora possui um arquivo `integrity.json` dentro da respectiva pasta.
- Esse arquivo contém o hash SHA256 de todos os arquivos do backup, permitindo auditoria e verificação de integridade.
- Para verificar se um backup foi corrompido ou alterado, basta recalcular os hashes dos arquivos e comparar com o `integrity.json`.
- O processo é automático a cada novo backup.

**Exemplo de uso:**
- Se precisar restaurar um backup, valide antes a integridade usando o arquivo `integrity.json`.
- Em breve, será possível rodar um comando para checagem automática de integridade.

### Como checar a integridade dos backups

Para verificar automaticamente a integridade de todos os backups existentes, execute:

```
python auto_update.py --check-backups
```

O sistema irá:
- Ler todos os backups na pasta configurada
- Comparar os hashes dos arquivos com o `integrity.json`
- Informar se cada backup está íntegro ou se há arquivos corrompidos/ausentes 

## Criptografia dos Backups

- Se `encryption_enabled: true` no `config.yaml`, todos os arquivos dos backups (exceto `integrity.json`) serão criptografados usando Fernet (AES).
- A chave de criptografia pode ser definida por variável de ambiente `BACKUP_ENCRYPTION_KEY` ou pelo arquivo `backup.key` na raiz do projeto.
- Para gerar uma chave segura, execute no Python:
  ```python
  from cryptography.fernet import Fernet
  print(Fernet.generate_key().decode())
  ```
  Copie o resultado para a variável de ambiente ou salve em `backup.key`.
- **IMPORTANTE:** Guarde a chave em local seguro! Sem ela, não será possível descriptografar os backups.

**Exemplo de uso:**
- Para descriptografar um arquivo, use o mesmo método Fernet e a mesma chave. 

### Como visualizar o status do sistema

Para exibir um resumo rápido dos backups, últimos commits e erros recentes, execute:

```
python auto_update.py --status
```

O sistema irá mostrar:
- Lista dos últimos backups (data, integridade, criptografado ou não)
- Últimos commits automáticos
- Últimos erros críticos registrados 

### Notificações automáticas de integridade

Para receber um alerta por e-mail caso algum backup esteja corrompido ou ausente, execute:

```
python auto_update.py --check-backups --notify
```

Se houver qualquer problema de integridade, um e-mail será enviado com os detalhes dos arquivos/backup(s) afetados. 

# ROADMAP REVISADO DO PROJETO

## Estado Atual (2025-06)

### Funcionalidades já implementadas
- **Backup automático com versionamento e rotação**
- **Commit e push automáticos para o GitHub**
- **Backup seguro com criptografia opcional (Fernet/AES)**
- **Geração e verificação de integridade dos backups (hash SHA256)**
- **Notificações automáticas por e-mail (sucesso, erro, integridade)**
- **Logs diários, logs de erro separados e rotacionados**
- **Interface CLI para status, checagem de integridade e monitoramento**
- **Configuração centralizada via YAML e variáveis de ambiente**
- **Documentação detalhada e onboarding facilitado**

### Pontos fortes
- Segurança (criptografia, variáveis de ambiente, logs segregados)
- Facilidade de uso (CLI, documentação, exemplos)
- Auditoria e rastreabilidade (logs, integridade, notificações)
- Modularidade para expansão futura

## Próximos Passos Sugeridos

### Integrações externas
- [ ] Notificações via Slack, Telegram ou Microsoft Teams
- [ ] Webhook para integração com outros sistemas

### Interface e usabilidade
- [ ] Interface web simples para monitoramento e restauração assistida
- [ ] Dashboard de status dos backups e notificações
- [ ] Wizard de configuração inicial

### Automação e DevOps
- [ ] Pipeline CI/CD para testes automáticos do sistema de backup
- [ ] Deploy automatizado em servidores
- [ ] Testes de restauração automatizada

### Segurança avançada
- [ ] Rotação automática de chaves de criptografia
- [ ] Backup redundante em múltiplos destinos (cloud/local)
- [ ] Monitoramento de tentativas de acesso não autorizado

### Outras sugestões
- [ ] Suporte a múltiplos repositórios/projetos
- [ ] Permitir múltiplos destinatários de notificação
- [ ] Exportação de relatórios de auditoria

---

**O projeto está pronto para uso em produção, com base em boas práticas de segurança, automação e auditoria.**

Para evoluir, basta priorizar os próximos passos conforme a necessidade do time ou do negócio. 

# Checklist de Revisão Final

- [x] Todos os arquivos essenciais presentes e organizados
- [x] Nenhum arquivo sensível versionado (confira .gitignore)
- [x] Documentação cobre todos os pontos importantes
- [x] Scripts testados em ambiente limpo
- [x] Variáveis de ambiente e segredos protegidos
- [x] Logs e backups rotacionados corretamente
- [x] Configuração centralizada e fácil de entender
- [x] Pronto para onboarding de novos colaboradores

--- 