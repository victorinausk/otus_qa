# -*- coding: UTF-8 -*-
"""
Basic test for logging
"""

import os

import pymysql
from sqlalchemy import create_engine


def find_file(file_name):
    """ Find file in sub dirs """

    rootdir = os.getcwd()

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filepath = subdir + os.sep + file

            if filepath.endswith(file_name):
                return filepath
    raise Exception("Files not found " + file_name)


def get_insertion_sql():
    return """
    INSERT
    INTO
    opencart.oc_customer(customer_id, customer_group_id, store_id, firstname, lastname, email, telephone, fax, password,
                         salt, cart, wishlist, newsletter, address_id, custom_field, ip, status, approved, safe, token,
                         code, date_added)
    VALUES(1, 1, 0, 'test sql', 'test sql', 'noone@yandex.ru', '1111111', '',
           '6c135509838d44c012ac7748fda5c564f1ae2f67', '6ZZIlwIIR', null, null, 0, 0, '', '', 1, 1, 0, '', '',
           '2019-11-08 12:32:49');
    """


def get_truncate_sql():
    return "truncate table opencart.oc_customer"


def get_select_sql():
    return "select * from opencart.oc_customer"


def generate_customer():
    # engine = create_engine('mysql://root:my-secret-pw@localhost/opencart', echo=True) не работает с Python3
    try:
        conn = pymysql.connect(host='127.0.0.1', user='root', password='my-secret-pw', db='opencart', charset='utf8')
    except Exception:
        print("Error in MySQL connexion")
    else:
        cursor = conn.cursor()

        try:
            cursor.execute(get_truncate_sql())
            cursor.execute(get_insertion_sql())
            cursor.execute(get_select_sql())

        except Exception:
            print("Error with query")
        else:
            print('===================================================================')
            print(cursor.fetchmany(size=1))
            print(cursor.rowcount)
            cursor.close()
            conn.close()


def test_sql(driver):
    driver.get('https://localhost/admin')
    generate_customer()


def test_logging(driver):
    driver.get('https://ya.ru')
    print('sqlite:///' + find_file('log.db'))
    engine = create_engine('sqlite:///' + find_file('log.db'), echo=True)
    assert int(engine.execute("select count(*) from log").fetchall()[0][0]) != 0
