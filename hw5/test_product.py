""" Tests for opencart products page """
# pylint: disable=redefined-outer-name, unused-argument

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .pages import LoginPage, ProductsPage, EditProductPage, AdminDashboardPage


@pytest.fixture(scope='module', autouse=True)
def login_opencart(driver, request, open_login_page, module_fixture):
    login_page = LoginPage(driver)
    login_page.login(login='joe1', password='abc123')
    WebDriverWait(driver=driver, timeout=10).until(EC.url_contains('dashboard'))


@pytest.fixture
def dashboard_page(driver):
    return AdminDashboardPage(driver)


@pytest.fixture
def edit_product_page(driver):
    return EditProductPage(driver)


@pytest.fixture
def products_page(driver):
    return ProductsPage(driver)


@pytest.fixture
def open_products_page(request, dashboard_page):
    dashboard_page.open_products_page()


@pytest.fixture
def add_new_product(request, products_page, edit_product_page, open_products_page):
    product_name = 'Test product'
    products_page.create_product(product_name=product_name,
                                 product_tag='Test product meta tag',
                                 product_model='Test product model')
    yield product_name

    def cleanup():
        products_page.delete_product(product_name)

    request.addfinalizer(cleanup)


@pytest.fixture
def create_product_to_edit(open_products_page, products_page, edit_product_page):
    product_name = 'Test product to be edited'
    products_page.create_product(product_name=product_name,
                                 product_tag='Test product meta tag',
                                 product_model='Test product model')
    products_page.close_success_alert()
    yield product_name


@pytest.fixture
def create_product_to_delete(open_products_page, products_page, edit_product_page):
    product_name = 'Test product to be deleted'
    products_page.create_product(product_name=product_name,
                                 product_tag='Test product meta tag',
                                 product_model='Test product model')
    products_page.close_success_alert()
    yield product_name


@pytest.fixture
def delete_product(request, create_product_to_delete, products_page):
    products_page.delete_product(product_name=create_product_to_delete)


@pytest.fixture
def edit_product(request, create_product_to_edit, products_page, edit_product_page):
    new_product_name = 'Test product edited'
    print(create_product_to_edit)
    products_page.edit_created_product(name=create_product_to_edit, name_edited=new_product_name)
    yield new_product_name

    def cleanup():
        print(" Cleanup")
        products_page.delete_product(new_product_name)
        #        products_page.delete_product(product_name=f'"{new_product_name}"')

    request.addfinalizer(cleanup)


def test_add_product(driver, module_fixture, add_new_product, products_page):
    """ Test add product item """

    assert products_page.get_success_alert()
    assert products_page.is_products_on_page(add_new_product)


def test_edit_product(driver, module_fixture, edit_product, products_page):
    """ Test edit product item info """
    assert products_page.get_success_alert()
    assert products_page.is_products_on_page(product_name=edit_product)


def test_delete_product(driver, module_fixture, create_product_to_delete, delete_product, products_page):
    """ Test delete product item """
    assert products_page.get_success_alert()
