# -*- coding: UTF-8 -*-

import pytest


@pytest.fixture(scope="session")
def session_fixture():
    print("\nСессия fixture")
    yield
    print("\nЗакрытие сессии fixture")


@pytest.fixture(scope="module")
def module_fixture(request):
    print("\nМодуль fixture")

    def fin():
        print("\nЗакрытие модуля fixture")

    request.addfinalizer(fin)


@pytest.fixture()
def function_fixture():
    print("\nФункция fixture")
