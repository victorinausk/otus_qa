# -*- coding: UTF-8 -*-

import pytest


"""Проверяем, что 8 элемент списка = 8"""

def test_item_of_list(session_fixture, module_fixture, function_fixture):
    list = [1, 2, 3, 4, 5, 6, 7, 8]

    print("\ntest N1: ")
    assert list[7] == 8, "test N1 is not passed"


"""Проверяем, что оператор + складывает 2 строки"""

def test_summ_of_two_strings(session_fixture, module_fixture, function_fixture):
    str1 = 'well'
    str2 = 'done'
    str = str1+str2
    print("\ntest N2: ")
    assert str == 'welldone', "test N2 is not passed"


"""Проверяем. что оператор * умножает строку на заданное число"""

def test_multiply_number_to_string(session_fixture, module_fixture, function_fixture):
    str = '123'
    multiplied_str = 2*str
    print("\ntest N3 ")
    assert multiplied_str == '123123', "test N3 is not passed"



"""Проверяем, что функция clear отчищает список"""

def test_clear_of_list(session_fixture, module_fixture, function_fixture):
    list = ['aa', 'bb', 'cc']
    list.clear()
    print("\ntest N4")
    assert len(list) == 0, "test N4 is not passed"




"""Проверяем, что функция count находит число вхождений в список"""

def test_ammount_of_x_in_list(session_fixture, module_fixture, function_fixture):
    list = ['qq', 'x', 'aaz', 'x']
    ammount = list.count('x')
    print("\ntest N5")
    assert ammount == 2, print("test N5 is not passed")


"""Проверяем, что функция reverse переворачивает список"""

def test_reversed_list(session_fixture, module_fixture, function_fixture):
    list = ['first one', 'middle one', 'last one']
    list.reverse()
    first_of_reversed = list[0]
    print("\ntest N6")
    assert first_of_reversed == 'last one', print("not passed")



"""Проверяем. что множество содержит только уникальные элементы"""

def test_set_consist_of_unique_elements(session_fixture, module_fixture, function_fixture):
    s = set()
    s.add(1)
    s.add(2)
    s.add(1)
    lenth = len(s)
    print("\ntest N7")

    assert lenth == 2 , print("not passed")


"""Проверяем, что по ключу можно получить значение из словаря"""

def test_getting_dictionary_value_by_key(session_fixture, module_fixture, function_fixture):
    d = dict(key1='value1', key2='value2', key3='value3')
    print("test N8")
    assert d['key1'] == 'value1', print("not passed")


"""Проверяем, что значения переменных поменены"""

def test_switch_values(session_fixture, module_fixture, function_fixture):
    a = 5
    b = 10
    a, b = b, a
    print("test N9")
    assert a == 10, print("not passed")




"""Проверяем, что функция insert вставляет значение в список"""

def test_insert_value(session_fixture, module_fixture, function_fixture):
    l = ['first one', 'middle one', 'last one']
    l.insert(0, 'new first one')
    print("test N10")
    assert l[0] == 'new first one', print("not passed")


def inc(x):
    return x + 1
"""Проверяем, что функция инкримента увеличивает на 1 """
def test_answer():
    print("test N11")
    assert inc(3) == 4, print ("not passed")



