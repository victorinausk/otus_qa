# -*- coding: UTF-8 -*-
"""HW 3 разметка для Travis"""

import pytest


@pytest.fixture(scope="module")
def module_fixture(request):
    """Расскраска трависа"""
    print("\n================================== HW 3 ===============================================================")
    print("\n")

    def fin():
        """Расскраска трависа"""
        print("\n")

    request.addfinalizer(fin)
