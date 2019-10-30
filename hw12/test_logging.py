"""
Basic test for logging
"""
import logging
# pylint: disable=redefined-outer-name, unused-argument
import os
from datetime import date

import pytest


def find_file(file_name):
    """ Find file in sub dirs """

    rootdir = os.getcwd()

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filepath = subdir + os.sep + file

            if filepath.endswith(file_name):
                return True
    return False


@pytest.fixture
def function_logger(logger, driver):
    return logging.getLogger(name=f'session_logger.{__name__}.{driver.name}')


@pytest.fixture
def logs_setup_teardown(logger):
    logger.debug('---- Beginning of test. ----')
    yield
    logger.debug('---- End of test. ----')


def test_logging(driver, function_logger, logs_setup_teardown, proxy):
    driver.get('https://ya.ru')
    function_logger.info('Yandex')
    function_logger.debug(proxy.har)
    assert find_file(f'logs_{date.today()}.log')
