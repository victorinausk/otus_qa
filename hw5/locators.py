""" Locators """

from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN_INPUT = (By.ID, 'input-username')
    PASSWORD_INPUT = (By.ID, 'input-password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'button[class="btn btn-primary"][type="submit"]')
    FORGOT_PASSWORD_BUTTON = (By.LINK_TEXT, 'Forgotten Password')
    ALERT_LOGIN_FAILURE = (By.CSS_SELECTOR, 'div[class="alert alert-danger"]')


class BaseLocators:
    CLOSE_BUTTON = (By.CSS_SELECTOR, 'button.close')
    LOGOUT = (By.CSS_SELECTOR, 'fa fa-sign-out fa-lg')
    EMAIL_INPUT = (By.ID, 'input-email')
    ALERT_SUCCESS = (By.CSS_SELECTOR, 'div[class="alert alert-success"]')
    PLUS_ADD_BUTTON = (By.CSS_SELECTOR, '.fa-plus')
    SAVE_BUTTON = (By.CSS_SELECTOR, '.fa-save')


class AdminPageLocators:
    CATALOG = (By.XPATH, '//a[contains(text(), "Catalog")]')
    PRODUCTS = (By.XPATH, '//*[@id="catalog"]/ul/li/a[contains(@href, "product")]')
    # driver.FindElementByXPath("//*[@id='navMenu']/ul/li/a[contains(@href, 'mysite.com/item/')]").Click()


class ProductsPageLocators:
    ADD_PRODUCT = (By.CSS_SELECTOR, 'i[class="fa fa-plus"]')
    DELETE_PRODUCT = (By.CSS_SELECTOR, 'i[class="fa fa-trash-o"]')


class EditProductPageLocators:
    SAVE = (By.CSS_SELECTOR, 'i[class="fa fa-save"]')
    CANCEL = (By.XPATH, '//a[@data-original-title="Cancel"]')
    GENERAL_DESCRIPTION = (By.LINK_TEXT, 'General')
    DATA_DESCRIPTION = (By.LINK_TEXT, 'Data')
    PRODUCT_NAME_INPUT = (By.ID, 'input-name1')
    PRODUCT_TAGNAME_INPUT = (By.ID, 'input-meta-title1')
    PRODUCT_MODEL_INPUT = (By.ID, 'input-model')
    PRODUCT_PRICE_INPUT = (By.ID, 'input-price')
    IMAGE_DESCRIPTION = (By.LINK_TEXT, 'Image')
    PLUS_BUTTON = (By.CLASS_NAME, 'fa fa-plus-circle')
    BASE_IMAGE = (By.ID, 'thumb-image')
    ADDITIONAL_IMAGE = (By.ID, 'thumb-image0')
    EDIT_IMAGE_BUTTON = (By.ID, 'button-image')
    UPLOAD_BUTTON = (By.ID, 'button-upload')


class UploadPageLocators:
    UPLOAD_TITLE = (By.CSS_SELECTOR, 'input[name="download_description[1][name]"]')
    REAL_INPUT = (By.CSS_SELECTOR, 'input[type="file"]')
    UPLOAD_PATH = (By.CSS_SELECTOR, 'input[name="filename"]')
    UPLOAD_MASK = (By.CSS_SELECTOR, 'input[name="mask"]')
