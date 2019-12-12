*** Settings ***
Documentation    Suite description

*** Variables ***
#headlesschrome
${BROWSER}       headlesschrome
${DELAY}          2
${URL}      https://demo.opencart.com/
${Good page}    https://demo.opencart.com/index.php?route=product/product&product_id=43&search=MacBook
${Login page}    https://demo.opencart.com/index.php?route=account/login


*** Keywords ***

Open Browser To Shop Page
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}

SubmitBtn
    [Arguments]  ${btn}
    Click Button    ${btn}

InputTextInSearch
    [Arguments]  ${text}
    ${field} =   Get WebElement    css:div[id="search"] input
    Input Text    ${field}    ${text}

user serch "${good}"
    InputTextInSearch    ${good}
    SubmitBtn  xpath://button[@class='btn btn-default btn-lg']

User added good to chart
    SubmitBtn  xpath://button[@id='button-cart']

Open Browser TO Good Page
    Open Browser    ${Good page}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}

Open Browser To Login Page
    Open Browser    ${Login page}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}

Input Username
    [Arguments]    ${username}
    Input Text    //input[@id='input-email']    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    id:input-password    ${password}

User login "${username}" and pwd "${password}"
    Input username    ${username}
    Input password    ${password}
    SubmitBtn   xpath://input[@class='btn btn-primary']