""" Opencart pages """

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from .locators import LoginPageLocators, AdminPageLocators, ProductsPageLocators, UploadPageLocators
from .locators import EditProductPageLocators, BaseLocators


def clear_input(element):
    """ Clear input data """
    element.send_keys(Keys.CONTROL + 'a')
    element.send_keys(Keys.DELETE)


def click_via_script(driver, element: WebElement):
    """
    Метод осуществляет клик по элементу через JS скрипт
    :driver: webdriver
    :param element: экземпляр класса WebElement
    """
    return driver.execute_script("arguments[0].click();", element)


class BasePage:

    def __init__(self, driver):
        self.driver = driver


class LoginPage(BasePage):

    def login(self, login, password):
        self.driver.find_element(*LoginPageLocators.LOGIN_INPUT).send_keys(login)
        self.driver.find_element(*LoginPageLocators.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()

    def clear_username_password(self):
        clear_input(self.driver.find_element(*LoginPageLocators.LOGIN_INPUT))
        clear_input(self.driver.find_element(*LoginPageLocators.PASSWORD_INPUT))

    def open_forgot_password_link(self):
        self.driver.find_element(*LoginPageLocators.FORGOT_PASSWORD_BUTTON).click()


class AdminDashboardPage(BasePage):

    def open_products_page(self):
        return click_via_script(self.driver, self.driver.find_element(*AdminPageLocators.PRODUCTS))


class ProductsPage(BasePage):

    def __open_add_product_page(self):
        click_via_script(self.driver, self.driver.find_element(*ProductsPageLocators.ADD_PRODUCT))

    def __open_edit_product_page(self, product_name):
        self.__filter_product(product_name)
        text_product = self.driver.find_element(By.XPATH,
                                                f'//*[@id="form-product"]/div/table/tbody/tr[1]/td[3][contains(.,"{product_name}")]')
        tr_product = text_product.find_element(By.XPATH, '..')
        click_via_script(self.driver, tr_product.find_element(By.XPATH, './td//i[@class="fa fa-pencil"]'))

    def __filter_product(self, product_name):
        filter_name = self.driver.find_element(By.ID, 'input-name')
        clear_input(filter_name)
        filter_name.send_keys(product_name)
        click_via_script(self.driver, self.driver.find_element(By.ID, 'button-filter'))

    def __select_product(self, product_name):
        click_via_script(self.driver, self.driver.find_element(By.XPATH, '//thead/tr/td[1]/input'))

    def get_success_alert(self):
        try:
            WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located(BaseLocators.ALERT_SUCCESS))
            return self.driver.find_element(*BaseLocators.ALERT_SUCCESS)
        except NoSuchElementException:
            return False

    def close_success_alert(self):
        try:
            success = self.driver.find_element(*BaseLocators.ALERT_SUCCESS)
            WebDriverWait(driver=self.driver, timeout=10).until(EC.visibility_of(success))
            return click_via_script(self.driver, self.driver.find_element(*BaseLocators.CLOSE_BUTTON))
        except (ElementNotVisibleException, ElementNotInteractableException):
            return None

    def __get_edit_product_page(self):
        return EditProductPage(self.driver)

    def create_product(self, *args, **kwargs):
        self.__open_add_product_page()
        edit_product_page = self.__get_edit_product_page()
        edit_product_page.add_product(*args, **kwargs)

    def edit_created_product(self, name, name_edited):
        self.__open_edit_product_page(name)
        edit_product_page = self.__get_edit_product_page()
        edit_product_page.edit_product(name_edited)

    def delete_product(self, product_name):
        self.__filter_product(product_name)
        self.__select_product(product_name)
        click_via_script(self.driver, self.driver.find_element(*ProductsPageLocators.DELETE_PRODUCT))
        Alert(self.driver).accept()

    def is_products_on_page(self, product_name):
        try:
            self.__filter_product(product_name)
            return self.driver.find_element(By.XPATH,
                                            f'//*[@id="form-product"]/div/table/tbody/tr[1]/td[3][contains(.,"{product_name}")]')
        except NoSuchElementException:
            return False


class EditProductPage(BasePage):

    def __clear_product_name(self):
        clear_input(self.driver.find_element(*EditProductPageLocators.PRODUCT_NAME_INPUT))

    def __add_product_name(self, product_name):
        self.driver.find_element(*EditProductPageLocators.PRODUCT_NAME_INPUT).send_keys(product_name)

    def __add_product_tag(self, product_tag):
        self.driver.find_element(*EditProductPageLocators.PRODUCT_TAGNAME_INPUT).send_keys(product_tag)

    def __add_product_model(self, product_model):
        self.driver.find_element(*EditProductPageLocators.PRODUCT_MODEL_INPUT).send_keys(product_model)

    def __save_product_info(self):
        click_via_script(self.driver, self.driver.find_element(*EditProductPageLocators.SAVE))

    def __add_main_product_info(self, product_name, product_tag, product_model):
        self.__add_product_name(product_name)
        self.__add_product_tag(product_tag)
        click_via_script(self.driver, self.driver.find_element(*EditProductPageLocators.DATA_DESCRIPTION))
        self.__add_product_model(product_model)

    def add_product(self, product_name, product_tag, product_model):
        self.__add_main_product_info(product_name, product_tag, product_model)
        self.__save_product_info()

    def edit_product(self, product_name):
        self.__clear_product_name()
        self.__add_product_name(product_name)
        self.__save_product_info()


class UploadPage(BasePage):

    def open_upload(self):
        click_via_script(self.driver, self.driver.find_element(*BaseLocators.PLUS_ADD_BUTTON))

    def input_file_title(self, name):
        self.driver.find_element(*UploadPageLocators.UPLOAD_TITLE).send_keys(name)

    def save(self):
        click_via_script(self.driver, self.driver.find_element(*BaseLocators.SAVE_BUTTON))
