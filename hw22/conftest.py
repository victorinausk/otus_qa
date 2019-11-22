# -*- coding: UTF-8 -*-
"""Базовая настройка сервисов"""
import pytest
import testcontainers.compose

COMPOSE_PATH = "./"


@pytest.fixture(scope="module", autouse=True)
def module_fixture(request):
    """Запуск окружения"""
    print("\nЗапуск docker-compose")
    compose = testcontainers.compose.DockerCompose(COMPOSE_PATH)
    compose.start()
    compose.wait_for('http://' + request.config.getoption('--opencart_url'))

    def fin():
        """Остановка окружения"""
        print("\nОстановка docker-compose")
        compose = testcontainers.compose.DockerCompose(COMPOSE_PATH)
        compose.stop()
        print("\n")

    request.addfinalizer(fin)


def pytest_addoption(parser):
    parser.addoption('--opencart_url', default='localhost', help='Set opencart URL.')
    parser.addoption("--method", action="store", default="GET", help="http method")
    parser.addoption("--header", action="store", default="HTTP/1.0", help="http header")
    parser.addoption("--port", action="store", default=80, help="connection port")
