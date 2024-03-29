# -*- coding: UTF-8 -*-
"""Расширенный отчет pytest"""

import os
import pkgutil

import pytest


@pytest.fixture(scope="module", autouse=True)
def module_fixture(request):
    """Запуск окружения"""

    def fin():
        """Остановка окружения"""
        print("\n")

    request.addfinalizer(fin)


@pytest.mark.usefixtures("environment_info")
@pytest.fixture(scope='session', autouse=True)
def configure_html_report_env(request, get_module_info):
    request.config._metadata.update(
        {"Env": os.environ, "Modules": get_module_info}
    )
    yield


@pytest.fixture(scope='session')
def get_module_info():
    lst = []
    for pkg in pkgutil.iter_modules():
        lst.append(pkg.name)
    return lst
