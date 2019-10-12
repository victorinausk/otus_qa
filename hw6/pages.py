""" pages """
# pylint: disable=missing-docstring, too-few-public-methods

from selenium.webdriver.common.action_chains import ActionChains
from .locators import CustomDrugAvatarLocators


class BasePage():

    def __init__(self, driver):
        self.driver = driver


class DartDragandDropPage(BasePage):

    def scroll_to_custom(self):
        self.driver.find_element(*CustomDrugAvatarLocators.Scroll).click()

    def move_to_trash(self):
        self.driver.switch_to.frame(0)
        documents = self.driver.find_elements(*CustomDrugAvatarLocators.Document)
        trash = self.driver.find_element(*CustomDrugAvatarLocators.Trash)
        for document in documents:
            ActionChains(self.driver).drag_and_drop(document, trash).perform()
