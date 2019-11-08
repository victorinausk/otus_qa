# -*- coding: UTF-8 -*-
"""Расширенный отчет pytest Allure"""
import pytest


@pytest.fixture(scope="module", autouse=True)
def module_fixture(request):
    """Запуск окружения"""

    def fin():
        """Остановка окружения"""
        print("\n")

    request.addfinalizer(fin)
