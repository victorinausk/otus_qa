""" API tests """
# -*- coding: UTF-8 -*-

import pytest
import requests


class ApiClient:

    def __init__(self, address):
        self.address = address

    def do_get(self, endpoint):
        url = ''.join([self.address, endpoint])
        return requests.get(url)

    def do_post(self, *args):
        pass


def pytest_collection_modifyitems(items, config):
    address = config.getoption('address')
    if address is not None:
        selected = []
        deselected = []

        for item in items:
            if address in getattr(item, 'fixturenames', ()):
                selected.append(item)
            else:
                deselected.append(item)

        config.hook.pytest_deselected(items=deselected)
        items[:] = selected
        if not items:  # check if items is empty
            raise ValueError('Invalid URL.')


def pytest_addoption(parser):
    parser.addoption('--address', help='Run tests only for certain URL. Enter fixture name.')


@pytest.fixture
def dogceo():
    client = ApiClient('https://dog.ceo/api')
    return client


@pytest.fixture
def openbrewery():
    client = ApiClient('https://api.openbrewerydb.org')
    return client


@pytest.fixture
def jph():
    client = ApiClient('https://jsonplaceholder.typicode.com')
    return client


@pytest.fixture(scope="module", autouse=True)
def module_fixture(request):
    """Тестирование базовых  Фикстур модуль"""
    print("\n")

    def fin():
        """Тестирование базовых  Фикстур модуль"""
        print("\n")

    request.addfinalizer(fin)
