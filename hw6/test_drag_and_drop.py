""" Test drag and drop element on page """
# pylint: disable=redefined-outer-name, unused-argument

import pytest
from selenium.webdriver.common.by import By

from .pages import DartDragandDropPage


@pytest.fixture
def init_page(driver):
    """ Class init """
    return DartDragandDropPage(driver)


@pytest.fixture
def drag(driver, init_page):
    """ base logic """
    init_page.scroll_to_custom()
    init_page.move_to_trash()


def test_drag_n_drop(driver, drag):
    """Добавление документов в корзину"""

    assert driver.find_elements(By.CSS_SELECTOR, '[class="trash full"]')
