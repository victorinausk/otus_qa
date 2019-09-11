# -*- coding: UTF-8 -*-
"""HW 3 разметка для Travis"""

import pytest
@pytest.fixture(scope="module")
def module_fixture(request):
    """Тестирование базовых  Фикстур модуль"""
    print("\n================================== HW 3 ===============================================================")
    print("\nМодуль fixture")

    def fin():
        """Тестирование базовых  Фикстур модуль"""
        print("\nЗакрытие модуля fixture")

    request.addfinalizer(fin)