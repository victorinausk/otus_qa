# -*- coding: UTF-8 -*-
"""Пример проверки парсинга логов"""


def test_log_parcer(log_parcer):
    """log test"""
    current_result = log_parcer
    assert current_result != "Error"
