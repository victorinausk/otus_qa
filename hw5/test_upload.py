"""
Test for file upload function
"""
import pytest
from .pages import LoginPage, UploadPage


@pytest.fixture
def login_page(driver):
    """ Class init """
    return LoginPage(driver)


@pytest.fixture
def login_logout(request, driver, login_page):
    """ base login logout """

    login_page.login(login='joe1', password='abc123')

    def logout():
        url = driver.current_url
        url = url.replace("dashboard", "logout")
        driver.get(url)
        driver.delete_all_cookies()

    request.addfinalizer(logout)


def test_file_upload(login_logout, driver):
    """
    Check if upload and save have no error
    """
    file_path = './test_img.jpg'
    upload_page = UploadPage(driver)
    upload_page.open_upload()
    upload_page.input_file_title('test img')
    assert upload_page.upload_file(file_path)
    upload_page.save()
    print(driver.current_url)
    assert 'catalog/download&token=' in driver.current_url
