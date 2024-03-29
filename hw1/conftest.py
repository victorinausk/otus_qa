# -*- coding: UTF-8 -*-
"""Тестирование базовых  Фикстур"""

import pytest


@pytest.fixture(scope="session")
def session_fixture():
    """Тестирование базовых  Фикстур ссесия"""
    print("\nСессия fixture")
    yield
    print("\nЗакрытие сессии fixture")


@pytest.fixture(scope="module")
def module_fixture(request):
    """Тестирование базовых  Фикстур модуль"""
    print("\n")

    def fin():
        """Тестирование базовых  Фикстур модуль"""
        print("\n")
    request.addfinalizer(fin)


@pytest.fixture()
def function_fixture():
    """Тестирование базовых  Фикстур"""
    print("\nФункция fixture")
