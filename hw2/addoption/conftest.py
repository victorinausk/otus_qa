# -*- coding: UTF-8 -*-
"""Пример с addoption"""
import pytest


def pytest_addoption(parser):
    """Установка базовых значений"""
    parser.addoption(
        "--url",
        action="store",
        default="https://ya.ru",
        help="This is request url",
        required=False
    )


@pytest.fixture
def url_param(request):
    """Возврат значения ключа url"""

    return request.config.getoption("--url")
