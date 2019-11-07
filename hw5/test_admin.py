""" Tests for opencart admin login page """
# pylint: disable=redefined-outer-name, unused-argument

import pytest

from .locators import LoginPageLocators, BaseLocators
from .pages import LoginPage


@pytest.fixture
def login_page(driver):
    """ Class init """
    return LoginPage(driver)


@pytest.fixture
def login_logout(request, driver, login_page):
    login_page.login(login='joe1', password='abc123')

    def logout():
        url = driver.current_url
        url = url.replace("dashboard", "logout")
        driver.get(url)
        driver.delete_all_cookies()

    request.addfinalizer(logout)


def test_login_success(login_logout, driver):
    """ Test login success """
    assert 'dashboard' in driver.current_url


@pytest.mark.xfail(reason='login failure, invalid username/password')
def test_login_fail(login_page, driver):
    """ Test login failure: invalid username and password """
    url = driver.current_url
    url = url.replace("dashboard", "logout")
    driver.get(url)
    login_page.login(login='admin', password='admin')
    assert 'dashboard' in driver.current_url


def test_login_empty(login_page, driver):
    """ Test login failure: empty username and password """

    login_page.clear_username_password()
    login_page.login(login='', password='')

    assert driver.find_element(*LoginPageLocators.ALERT_LOGIN_FAILURE)


def test_forgot_password(login_page, driver):
    """ Test press forgotten password button on login page """
    url = driver.current_url
    url = url.replace("dashboard", "logout")
    driver.get(url)
    driver.delete_all_cookies()
    login_page.open_forgot_password_link()
    assert driver.find_element(*BaseLocators.EMAIL_INPUT)
