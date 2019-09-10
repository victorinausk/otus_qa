# -*- coding: UTF-8 -*-
"""Тестирование базовых типов"""


def test_item_of_list(session_fixture,module_fixture,function_fixture):
    """Проверяем, что 8 элемент списка = 8"""
    mylist = [1, 2, 3, 4, 5, 6, 7, 8]
    print("\ntest N1: ")
    assert mylist[7] == 8, "test N1 is not passed"


def test_sum_of_two_strings(session_fixture,module_fixture,function_fixture):
    """Проверяем, что оператор + складывает 2 строки"""
    str1 = 'well'
    str2 = 'done'
    answ = str1 + str2
    print("\ntest N2: ")
    assert answ == 'welldone', "test N2 is not passed"


def test_multiply_number_to_string():
    """Проверяем. что оператор * умножает строку на заданное число"""
    str1 = '123'
    multiplied_str = 2 * str1
    print("\ntest N3 ")
    assert multiplied_str == '123123', "test N3 is not passed"


def test_clear_of_list():
    """Проверяем, что функция clear отчищает список"""
    mylist = ['aa', 'bb', 'cc']
    mylist.clear()
    print("\ntest N4")
    assert not mylist, "test N4 is not passed"


def test_amount_of_x_in_list():
    """Проверяем, что функция count находит число вхождений в список"""
    mylist = ['qq', 'x', 'aaz', 'x']
    amount = mylist.count('x')
    print("\ntest N5")
    assert amount == 2, print("test N5 is not passed")


def test_reversed_list():
    """Проверяем, что функция reverse переворачивает список"""
    mylist = ['first one', 'middle one', 'last one']
    mylist.reverse()
    first_of_reversed = mylist[0]
    print("\ntest N6")
    assert first_of_reversed == 'last one', print("not passed")


def test_set_consist_of_unique_elements():
    """Проверяем. что множество содержит только уникальные элементы"""
    s = set()
    s.add(1)
    s.add(2)
    s.add(1)
    length = len(s)
    print("\ntest N7")
    assert length == 2, print("not passed")


def test_getting_dictionary_value_by_key():
    """Проверяем, что по ключу можно получить значение из словаря"""
    d = dict(key1='value1', key2='value2', key3='value3')
    print("test N8")
    assert d['key1'] == 'value1', print("not passed")


def test_switch_values():
    """Проверяем, что значения переменных поменены"""
    a = 5
    b = 10
    a, b = b, a
    print("test N9")
    assert a == 10, print("not passed")


def test_insert_value():
    """Проверяем, что функция insert вставляет значение в список"""
    mylist = ['first one', 'middle one', 'last one']
    mylist.insert(0, 'new first one')
    print("test N10")
    assert mylist[0] == 'new first one', print("not passed")


def inc(x):
    """Инкремент"""
    return x + 1


def test_answer():
    """Проверяем, что функция инкримента увеличивает на 1 """
    print("test N11")
    assert inc(3) == 4, print("not passed")
