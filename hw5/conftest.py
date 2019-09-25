# -*- coding: UTF-8 -*-
"""Базовая настройка сервисов"""
import pytest
import testcontainers.compose
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions
from selenium.webdriver import DesiredCapabilities

COMPOSE_PATH = "./"


@pytest.fixture(scope='module', autouse=True)
def open_login_page(driver, request):
    url = 'admin/'
    login_page_url = ''.join((request.config.getoption('--opencart_url'), url))
    return driver.get(login_page_url)


@pytest.fixture(scope="module", autouse=True)
def module_fixture(request):
    """Запуск окружения"""
    print("\nЗапуск docker-compose")
    compose = testcontainers.compose.DockerCompose(COMPOSE_PATH)

    compose.start()
    compose.wait_for("http://localhost/")

    def fin():
        """Остановка окружения"""
        print("\nОстановка docker-compose")
        compose = testcontainers.compose.DockerCompose(COMPOSE_PATH)
        compose.stop()
        print("\n")
        print("\n================================== HW 6 ============================================================")
        print("\n")

    request.addfinalizer(fin)


@pytest.fixture(scope='session')
def driver(request):
    browser = request.config.getoption('--browser')
    if browser == 'chrome':
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--start-fullscreen')
        options.accept_insecure_certs = True
        options.accept_untrusted_certs = True
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')

        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['timeouts'] = {'implicit': int(request.config.getoption('--implicit_wait')) * 1000,
                                    'pageLoad': 5000, 'script': 10000}
        wd = webdriver.Chrome(options=options, desired_capabilities=capabilities)
        wd.maximize_window()
    elif browser == 'firefox':
        options = FirefoxOptions()
        options.accept_insecure_certs = True
        options.accept_untrusted_certs = True
        options.add_argument('--headless')
        options.add_argument('start-maximized')

        capabilities = DesiredCapabilities.FIREFOX.copy()
        capabilities['timeouts'] = {'implicit': int(request.config.getoption('--implicit_wait')) * 1000,
                                    'pageLoad': 5000, 'script': 10000}
        wd = webdriver.Firefox(options=options, desired_capabilities=capabilities)
        wd.maximize_window()
    else:
        raise ValueError('Unsupported browser.')
    yield wd
    wd.quit()


def pytest_addoption(parser):
    parser.addoption('--browser', help='Set browser name.', default='chrome')
    parser.addoption('--opencart_url', default='http://localhost/', help='Set opencart URL.')
    parser.addoption('--implicit_wait', default='0', help='Set the amount (in seconds) for implicit wait.')
