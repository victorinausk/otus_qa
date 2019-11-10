# -*- coding: UTF-8 -*-

import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions
from selenium.webdriver import DesiredCapabilities


@pytest.fixture(scope='module', autouse=True)
def open_login_page(driver, request):
    login_page_url = request.config.getoption('--url')
    print(login_page_url)
    return driver.get(login_page_url)


@pytest.fixture(scope="module", autouse=True)
def module_fixture(request):
    """Запуск окружения"""

    def fin():
        """Остановка окружения"""
        print("\n")

    request.addfinalizer(fin)


@pytest.fixture(scope='session', autouse=True)
def driver(request):
    browser = request.config.getoption('--browser')
    if browser == 'chrome':
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--start-fullscreen')
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['timeouts'] = {'implicit': 5000, 'pageLoad': 15000, 'script': 15000}
        wd = webdriver.Chrome(options=options, desired_capabilities=capabilities)
    elif browser == 'firefox':
        options = FirefoxOptions()
        options.add_argument('--headless')
        capabilities = DesiredCapabilities.FIREFOX.copy()
        capabilities['timeouts'] = {'implicit': 5000, 'pageLoad': 15000, 'script': 15000}
        wd = webdriver.Firefox(options=options, desired_capabilities=capabilities)
    else:
        raise ValueError('Unsupported browser.')
    yield wd
    wd.quit()


def pytest_addoption(parser):
    parser.addoption('--browser', help='Set browser name.', default='chrome')
    parser.addoption('--url', default='https://code.makery.ch/library/dart-drag-and-drop/', help='Set URL.')
    parser.addoption('--implicit_wait', default='10', help='Set the amount (in seconds) for implicit wait.')
