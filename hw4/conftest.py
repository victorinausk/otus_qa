# -*- coding: UTF-8 -*-
"""Базовая настройка сервисов"""
import pytest
import testcontainers.compose
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions

COMPOSE_PATH = "./"


@pytest.fixture(scope="module")
def module_fixture(request):
    """Запуск окружения"""
    print("\nЗапуск docker-compose")
    compose = testcontainers.compose.DockerCompose(COMPOSE_PATH)
    compose.start()
    time.sleep(10)

    def fin():
        """Остановка окружения"""
        print("\nОстановка docker-compose")
        compose = testcontainers.compose.DockerCompose(COMPOSE_PATH)
        compose.stop()

    request.addfinalizer(fin)


@pytest.fixture
def chrome_browser():
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--start-fullscreen')
    wd = webdriver.Chrome(options=options)
    yield wd
    wd.quit()


@pytest.fixture
def firefox_browser():
    options = FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--start-fullscreen')
    wd = webdriver.Firefox(options=options)
    yield wd
    wd.quit()


def pytest_collection_modifyitems(items, config):
    browser = config.getoption('browser')
    if browser is not None:
        selected = []
        deselected = []

        for item in items:
            if browser in getattr(item, 'fixturenames'):
                selected.append(item)
            else:
                deselected.append(item)

        config.hook.pytest_deselected(items=deselected)
        items[:] = selected
        if not items:
            raise ValueError('Invalid browser name.')


def pytest_addoption(parser):
    parser.addoption('--browser', help='Run tests only for certain browser.')
    parser.addoption('--opencart_url', default='http://127.0.0.1/')
