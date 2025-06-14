# Sistema de Consulta de Lojas e Inventário

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/JoaoSantosCodes/Projeto_02/actions/workflows/main.yml/badge.svg)](https://github.com/JoaoSantosCodes/Projeto_02/actions)
[![Coverage](https://codecov.io/gh/JoaoSantosCodes/Projeto_02/branch/main/graph/badge.svg)](https://codecov.io/gh/JoaoSantosCodes/Projeto_02)

> **Repositório oficial:** [github.com/JoaoSantosCodes/Projeto_02](https://github.com/JoaoSantosCodes/Projeto_02)

Sistema desktop para consulta, geração de carimbos e comunicação de informações de lojas e inventário, com exportação em PNG e envio por e-mail.

## 📁 Estrutura de Pastas

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

> O código-fonte principal agora está em `app/`. Para importar módulos internos, utilize:
> 
> ```python
> from app import database
> from app.send_mail_smtp import ...
> ```

## 🚀 Funcionalidades

- 📊 Consulta de lojas e inventário
- 🖼️ Geração de carimbos em PNG
- 📧 Envio por e-mail (HTML/PNG)
- 🔍 Busca e filtros avançados
- 🎨 Interface moderna e responsiva
- 🌓 Temas claro/escuro

## 📋 Pré-requisitos

- Python 3.10 ou superior
- Dependências listadas em `requirements.txt`
- Acesso à internet para envio de e-mails
- Permissões de administrador para algumas funcionalidades

## 🔧 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/JoaoSantosCodes/Projeto_02.git
   cd Projeto_02
   ```

2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o aplicativo:
   ```bash
   # Windows
   iniciar_app.bat
   # Linux/Mac
   python app.py
   ```

## 📖 Documentação

A documentação completa está disponível na pasta `docs/`:

- [Documentação Técnica](docs/technical/ARCHITECTURE.md)
- [Guia do Usuário](docs/user/USER_GUIDE.md)
- [Referência da API](docs/api/API_REFERENCE.md)
- [Monitoramento](docs/MONITORING.md)
- [Changelog](docs/CHANGELOG.md)

## 🧪 Testes

Execute os testes com:
```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/unit/
pytest tests/integration/
robot tests/ui/

# Com cobertura
pytest --cov=app tests/
```

## 🧪 Teste seguro de envio de e-mail

Para rodar o teste de integração de envio de e-mail:
1. Crie um arquivo `.env` ou defina as variáveis de ambiente:
   - `EMAIL_USER` (e-mail do remetente)
   - `EMAIL_PASSWORD` (senha de app do Gmail)
   - `EMAIL_TEST_RECEIVER` (e-mail de destino para o teste)
2. Execute:
   ```bash
   pytest tests/integration/test_send_mail.py
   ```

Exemplo de `.env.example`:
```
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_app_gmail
EMAIL_TEST_RECEIVER=destinatario@exemplo.com
```

O teste será ignorado automaticamente se as variáveis não estiverem definidas.

## 📦 Distribuição

Para criar o executável:
```bash
pyinstaller build.spec
```

O executável será gerado em `dist/Sistema_Consulta_Lojas.exe`

## 🤝 Contribuindo

1. Faça um Fork do projeto ou clone diretamente:
   ```bash
   git clone https://github.com/JoaoSantosCodes/Projeto_02.git
   cd Projeto_02
   ```
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'feat: sua mensagem'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

> **Dica:** Sempre mantenha seu fork/branch atualizado com a branch `main` do repositório oficial.

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## ✨ Roadmap

Veja nosso [Roadmap](docs/ROADMAP.md) para as próximas melhorias planejadas.

## 📫 Suporte

Para suporte, abra uma issue no GitHub ou envie um e-mail para seu-email@dominio.com

> **Atenção:**
> Testes sensíveis que utilizavam segredos foram removidos do repositório por segurança. Para testar envio de e-mail, utilize variáveis de ambiente e nunca exponha senhas ou tokens no código.

## 🔄 Sistema de Atualização Automática

O projeto inclui um sistema de atualização automática que mantém o repositório sincronizado com o GitHub:

### Configuração

1. Crie um arquivo `.env` com suas credenciais de e-mail:
   ```
   EMAIL_USER=seu_email@gmail.com
   EMAIL_PASSWORD=sua_senha_de_app_gmail
   ```

2. Configure o arquivo `config.yaml`:
   ```yaml
   update:
     interval: 300  # Intervalo em segundos
     max_retries: 3  # Tentativas em caso de erro

   notifications:
     email:
       enabled: true
       sender_email: "seu_email@gmail.com"
       recipient_email: "destinatario@exemplo.com"

   backup:
     enabled: true
     directory: "backups"
     max_backups: 5
   ```

### Funcionalidades

- **Atualização Automática**: Commit e push a cada 5 minutos (configurável)
- **Sistema de Backup**: Cria backups antes de cada commit
- **Notificações por E-mail**: Envia alertas de sucesso e erro
- **Tratamento de Erros**: Sistema de retry e notificações
- **Logs Detalhados**: Registro completo de todas as operações

### Como Usar

1. Configure o arquivo `config.yaml` com suas preferências
2. Configure as variáveis de ambiente no arquivo `.env`
3. Execute `auto_update.bat`
4. O script iniciará o monitoramento automático

### Arquivos Importantes

- `auto_update.py`: Script principal
- `auto_update.bat`: Inicializador para Windows
- `config.yaml`: Configurações do sistema
- `auto_update.log`: Arquivo de logs
- `backups/`: Diretório de backups (ignorado pelo git)

### Boas Práticas

- Mantenha o script rodando apenas quando necessário
- Monitore os logs para identificar problemas
- Configure corretamente as credenciais de e-mail
- Mantenha backups regulares
- Não modifique arquivos sensíveis durante a execução

---

> Documentação e código mantidos em [github.com/JoaoSantosCodes/Projeto_02](https://github.com/JoaoSantosCodes/Projeto_02) 