*** Settings ***

Documentation     Test examples for admin console
Test Teardown     Close Browser

Library           Selenium2Library


*** Variables ***
${BROWSER}        Firefox
${DELAY}          0
${LOGIN URL}      https://demo.opencart.com/admin/

*** Keywords ***

Open Browser To Login Page
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Login Page Should Be Open

Login Page Should Be Open
    Title Should Be    Administration

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open

Input Username
    [Arguments]    ${username}
    Input Text    input-username    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    id:input-password    ${password}

Input email
    [Arguments]    ${email}
    Input Text    id:input-email    ${email}

Submit
    Click Button    css:button[type='submit']

Welcome Page Should Be Open
    Title Should Be    Dashboard

Browser is opened to login page
    Open browser to login page

Browser is opened to admin page by user "${username}" and password "${password}"
    Open browser to login page
    User "${username}" logs in with password "${password}"
    Menu-Catigories


User "${username}" logs in with password "${password}"
    Input username    ${username}
    Input password    ${password}
    Submit

User clicked forgotten link
    Click Link  link:Forgotten Password
    Input email  demo@opencart.com
    Submit

Link has been sent to user e-mail
    Element Should Contain  css:div.alert:nth-child(1)     An email with a confirmation link has been sent your admin email address.

Category Permissiond denied
    Element Should Contain  //div[@class='alert alert-danger alert-dismissible']    Warning: You do not have permission to modify categories!


Menu-Catigories
    sleep  2s
    ${field} =   Get WebElement    css:a[href="#collapse1"]
    Click Element    ${field}
    sleep  2s
    Click Element    css:ul.in li a[href*=catalog]

User added new category "${name_category}" with tag "${name_tag}"
    Click Element    css:div.pull-right a.btn-primary
    Input Text    css:input[id="input-name1"]    ${name_category}
    Input Text    css:input[id="input-meta-title1"]    ${name_tag}
    Click Button    css:button[type="submit"]


*** Test Cases ***
Valid Login
    Given browser is opened to login page
    When user "demo" logs in with password "demo"
    Then welcome page should be open
    [Teardown]    Close Browser

Forgotten PWD
    Given browser is opened to login page
    When user clicked forgotten link
    Then Link has been sent to user e-mail
    [Teardown]    Close Browser

New Category Error
        Given browser is opened to admin page by user "demo" and password "demo"
        When User added new category "new category" with tag "new tag"
        Then Category Permissiond denied
        [Teardown]    Close Browser




