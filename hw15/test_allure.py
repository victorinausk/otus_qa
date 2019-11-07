# -*- coding: UTF-8 -*-
"""Расширенный отчет Allure"""
import allure
import pytest


@allure.title("This test will be passed")
def test_pass():
    pass


@allure.title("This test will be failed")
@pytest.mark.xfail(reason='Так задумано')
def test_fail():
    assert False


@allure.title("This test will be broken")
@pytest.mark.xfail(reason='Так задумано')
def test_broken():
    raise ValueError("Some error")


@allure.title("This test contains steps.")
@pytest.mark.xfail(reason='Так задумано')
def test_with_steps():
    make_step1('Параметр 1', 'Параметр 2')
    make_step2()
    make_step3()


@allure.step('Параметр 1: "{0}", Параметр 2: "{1}"')
def make_step1(param1, param2):
    print('1-й Шаг')
    assert True


@allure.step('промежуточный шаг')
def make_step2():
    print('2-й Шаг')


@allure.step('Финальная проверка')
def make_step3():
    print('Завал')
    assert False
