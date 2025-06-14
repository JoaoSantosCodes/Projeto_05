# Testes do Projeto

## Ferramentas de Teste

### 1. Testes Unitários
- **Framework**: pytest
- **Cobertura**: pytest-cov
- **Linting**: flake8, black
- **Type Checking**: mypy

### 2. Testes de Interface
- **Framework**: Robot Framework
- **Navegador**: Chrome/Firefox
- **Automação**: Selenium WebDriver
- **Relatórios**: Robot Framework Reports

### 3. Testes de Integração
- **Framework**: pytest
- **Mocking**: pytest-mock
- **Fixtures**: pytest-fixtures
- **Asserções**: pytest-assume

## Critérios de Aceitação

### 1. Testes Unitários
- Cobertura mínima de 80%
- Zero falhas em testes críticos
- Validação de tipos (mypy)
- Conformidade com PEP 8

### 2. Testes de E-mail
- Validação SMTP
  - Conexão segura
  - Autenticação
  - Envio de anexos
  - Formatação HTML
- Validação Outlook
  - Conexão COM
  - Envio de anexos
  - Formatação HTML
  - Tratamento de erros

### 3. Testes de Interface
- Responsividade
- Acessibilidade (WCAG 2.1)
- Compatibilidade cross-browser
- Performance (tempo de resposta < 2s)

### 4. Testes de Banco de Dados
- Integridade dos dados
- Performance das queries
- Tratamento de concorrência
- Backup e recuperação

## Estrutura de Testes

```
tests/
├── unit/                 # Testes unitários
│   ├── test_database.py
│   ├── test_carimbo.py
│   └── test_email.py
├── integration/         # Testes de integração
│   ├── test_workflow.py
│   └── test_security.py
└── ui/                  # Testes de interface
    ├── test_interface.py
    └── test_usability.py
```

## Como Executar os Testes

### Requisitos
- Python 3.10+
- pytest e plugins
- Robot Framework
- Selenium WebDriver
- Chrome/Firefox

### Instalação
```bash
# Dependências principais
pip install -r requirements.txt

# Dependências de teste
pip install robotframework
pip install robotframework-seleniumlibrary
pip install webdriver-manager
```

### Execução
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

## Exemplos de Testes

### Teste Unitário (pytest)
```python
def test_gerar_carimbo():
    carimbo = gerar_png_carimbo("Teste", "test.png")
    assert carimbo is not None
    assert os.path.exists("test.png")
```

### Teste de Interface (Robot Framework)
```robot
*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem

*** Test Cases ***
Login Válido
    Open Browser    http://localhost:5000    chrome
    Input Text    id=username    admin
    Input Text    id=password    senha123
    Click Button    id=login
    Page Should Contain    Bem-vindo
```

### Teste de Integração
```python
def test_fluxo_completo():
    # Setup
    db = Database("test.db")
    # Test
    result = db.get_lojas()
    # Assert
    assert len(result) > 0
```

## Relatórios

### Cobertura de Código
- Relatórios HTML em `coverage/`
- Relatórios XML para CI/CD
- Badges no README

### Testes de Interface
- Relatórios HTML do Robot Framework
- Screenshots de falhas
- Logs detalhados

### Performance
- Tempo de execução
- Uso de memória
- Tempo de resposta

## CI/CD

### GitHub Actions
- Execução automática de testes
- Geração de relatórios
- Build do executável
- Deploy automático

### Workflow
1. Push para main/develop
2. Execução de testes
3. Geração de relatórios
4. Build do executável
5. Deploy (se main)

## Boas Práticas

### 1. Nomenclatura
- Use prefixo `test_` para arquivos
- Nomes descritivos para testes
- Documente casos de teste

### 2. Organização
- Mantenha testes isolados
- Use fixtures quando necessário
- Evite dependências entre testes

### 3. Manutenção
- Atualize testes com mudanças no código
- Remova testes obsoletos
- Mantenha documentação atualizada

## Troubleshooting

### Problemas Comuns
1. **Testes falhando**
   - Verificar ambiente
   - Verificar dependências
   - Verificar dados de teste

2. **Cobertura baixa**
   - Identificar código não testado
   - Adicionar casos de teste
   - Verificar configuração

3. **Performance**
   - Otimizar testes lentos
   - Usar fixtures eficientemente
   - Paralarizar quando possível 