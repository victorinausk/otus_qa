"""
Basic test for logging
"""

import os

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


def test_logging(driver):
    driver.get('https://ya.ru')
    print('sqlite:///' + find_file('log.db'))
    engine = create_engine('sqlite:///' + find_file('log.db'), echo=True)
    assert int(engine.execute("select count(*) from log").fetchall()[0][0]) != 0
