*** Settings ***
Documentation    Suite description

Test Teardown     Close Browser
Resource          opencart.robot
Library           Selenium2Library





*** Test Cases ***
Search is working
    Given Open Browser To Shop Page
    When user serch "MacBook"
    Then Page Should Contain Link  MacBook
    [Teardown]    Close Browser

Mackbook added to chart
    Given Open Browser TO Good Page
    When User added good to chart
    Then Page Should Contain Element  //div[@class='alert alert-success alert-dismissible']
    [Teardown]    Close Browser


User Login Error
    Given Open Browser To Login Page
    When User login "demo" and pwd "demo"
    Then Page Should Contain Element  //div[@class='alert alert-danger alert-dismissible']
    [Teardown]    Close Browser
