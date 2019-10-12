""" locators """
# pylint: disable=missing-docstring, too-few-public-methods

from selenium.webdriver.common.by import By


class CustomDrugAvatarLocators():
    Scroll = (By.ID, 'custom-drag-avatar')
    Document = (By.CSS_SELECTOR, 'img[class="document"]')
    Trash = (By.CSS_SELECTOR, '[class="trash"]')
