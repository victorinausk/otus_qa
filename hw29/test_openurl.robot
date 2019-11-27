*** Settings ***
Documentation           This is a simple test with Robot Framework
Library                 Selenium2Library


*** Variables ***
${SERVER}               http://google.com
${BROWSER}              Chrome
${DELAY}                1


*** Keywords ***
Open Browser To Login Page
    Open Browser        ${SERVER}   ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed  ${DELAY}


*** Test Cases ***
Valid Login
    Open Browser To Login Page
    [Teardown]    Close Browser