# -*- coding: UTF-8 -*-
"""HW 3 проверка ДЗ"""
import os.path

from .main_ddt import gen_file, find_file


def test_item_of_list(module_fixture):
    """Проверим что есть выходной файл"""

    gen_file()
    assert os.path.isfile(find_file("result_data.txt"))
