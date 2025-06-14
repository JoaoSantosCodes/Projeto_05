*** Settings ***
Documentation     Testes de interface do Sistema de Consulta de Lojas
Library          OperatingSystem
Library          Process
Library          String
Library          Collections
Library          DateTime
Library          Screenshot
Library          Dialogs

*** Variables ***
${APP_PATH}      ${CURDIR}/../../dist/Sistema_Consulta_Lojas.exe
${SCREENSHOTS}   ${CURDIR}/screenshots
${TIMEOUT}       30s
${RETRY_COUNT}   3

*** Keywords ***
Iniciar Aplicativo
    [Documentation]    Inicia o aplicativo e verifica se está rodando
    Start Process    ${APP_PATH}    alias=app
    Sleep    5s
    Process Should Be Running    app

Finalizar Aplicativo
    [Documentation]    Finaliza o aplicativo
    Terminate Process    app
    Sleep    2s

Tirar Screenshot
    [Documentation]    Tira um screenshot com timestamp
    ${timestamp}=    Get Time    epoch
    ${screenshot_path}=    Set Variable    ${SCREENSHOTS}/screenshot_${timestamp}.png
    Take Screenshot    ${screenshot_path}
    [Return]    ${screenshot_path}

Verificar Elemento
    [Documentation]    Verifica se um elemento está visível
    [Arguments]    ${element_id}    ${timeout}=${TIMEOUT}
    FOR    ${i}    IN RANGE    ${RETRY_COUNT}
        ${status}=    Run Keyword And Return Status
        ...    Wait Until Element Is Visible    ${element_id}    ${timeout}
        Return From Keyword If    ${status}    ${True}
        Sleep    1s
    END
    Fail    Elemento ${element_id} não encontrado após ${RETRY_COUNT} tentativas

*** Test Cases ***
Iniciar Aplicativo
    [Documentation]    Verifica se o aplicativo inicia corretamente
    Iniciar Aplicativo
    Verificar Elemento    main_window
    Finalizar Aplicativo

Consultar Loja
    [Documentation]    Testa a funcionalidade de consulta de loja
    Iniciar Aplicativo
    Verificar Elemento    search_input
    Input Text    search_input    Loja Teste
    Click Button    search_button
    Verificar Elemento    results_table
    Finalizar Aplicativo

Gerar Carimbo
    [Documentation]    Testa a geração de carimbo
    Iniciar Aplicativo
    Verificar Elemento    search_input
    Input Text    search_input    Loja Teste
    Click Button    search_button
    Verificar Elemento    results_table
    Click Button    generate_stamp
    Verificar Elemento    stamp_preview
    Finalizar Aplicativo

Enviar Email
    [Documentation]    Testa o envio de email
    Iniciar Aplicativo
    Verificar Elemento    search_input
    Input Text    search_input    Loja Teste
    Click Button    search_button
    Verificar Elemento    results_table
    Click Button    send_email
    Verificar Elemento    email_dialog
    Input Text    email_input    teste@exemplo.com
    Click Button    send_button
    Verificar Elemento    success_message
    Finalizar Aplicativo 