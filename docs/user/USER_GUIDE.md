# Guia do Usuário

## Introdução

Este guia fornece instruções detalhadas sobre como usar o Sistema de Consulta de Lojas e Inventário.

## Primeiros Passos

### Instalação

1. Certifique-se de ter Python 3.10 ou superior instalado
2. Execute o arquivo `iniciar_app.bat` ou use o comando:
   ```bash
   python app.py
   ```

### Interface Principal

A interface é dividida em duas abas principais:

1. **Relação de Lojas**
   - Lista todas as lojas cadastradas
   - Filtros por UF e Operadora
   - Busca textual

2. **Inventário**
   - Lista todos os itens do inventário
   - Filtros similares à aba de Lojas
   - Busca textual

## Funcionalidades Principais

### 1. Consulta de Dados

#### Filtros Disponíveis
- **Busca Textual**: Pesquisa em todos os campos
- **UF**: Filtra por estado
- **Operadora**: Filtra por operadora de internet

#### Como Usar
1. Digite o termo de busca no campo "Buscar"
2. Selecione UF e/ou Operadora nos filtros
3. Clique em "Buscar" ou pressione Enter

### 2. Geração de Carimbos

#### Tipos de Carimbos
- Carimbo de Loja
- Carimbo de Inventário

#### Como Gerar
1. Selecione uma linha na tabela
2. Clique em "Gerar Carimbo"
3. Visualize o carimbo na janela de prévia
4. Escolha:
   - Salvar como PNG
   - Enviar por e-mail

### 3. Envio de E-mail

#### Métodos de Envio
1. **SMTP (Gmail)**
   - Requer senha de app do Gmail
   - Suporta anexo PNG e HTML

2. **Outlook**
   - Usa conta Outlook configurada
   - Suporta anexo PNG e HTML

#### Como Enviar
1. Gere o carimbo
2. Clique em "Enviar por E-mail"
3. Escolha o método de envio
4. Preencha os dados solicitados
5. Confirme o envio

## Dicas e Truques

### Atalhos de Teclado
- `Enter`: Executa busca
- `Ctrl+F`: Foca no campo de busca
- `Esc`: Limpa filtros

### Exportação de Dados
- Use o botão "Exportar CSV" para salvar dados
- Os arquivos são salvos no formato CSV
- Inclui todos os dados visíveis na tabela

### Personalização
- Alterne entre tema claro/escuro
- Ajuste o tamanho das colunas
- Reordene as colunas conforme necessário

## Solução de Problemas

### Problemas Comuns

1. **Carimbo não gera**
   - Verifique se uma linha está selecionada
   - Confirme se há dados válidos

2. **E-mail não envia**
   - Verifique conexão com internet
   - Confirme credenciais de e-mail
   - Verifique se o destinatário está correto

3. **Dados não aparecem**
   - Verifique filtros aplicados
   - Confirme conexão com banco de dados
   - Tente limpar os filtros

### Contato para Suporte

Em caso de problemas:
1. Verifique este guia
2. Consulte a documentação técnica
3. Entre em contato com o suporte

## Atualizações

O sistema é atualizado regularmente. Para verificar atualizações:
1. Consulte o repositório do projeto
2. Verifique o arquivo de changelog
3. Atualize quando novas versões estiverem disponíveis 