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

    def fin():
        """Остановка окружения"""
        print("\nОстановка docker-compose")
        compose = testcontainers.compose.DockerCompose(COMPOSE_PATH)
        compose.stop()
        print("\n")

    request.addfinalizer(fin)
