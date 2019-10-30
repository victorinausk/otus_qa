# -*- coding: UTF-8 -*-
"""Заглушка для проверки расширенного отчета pytest"""
import pytest


def test_pass():
    pass


@pytest.mark.xfail(reason='1!=2')
def test_fail():
    assert 1 == 2
