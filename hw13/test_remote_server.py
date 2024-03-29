"""
Basic test for remote server
"""
import json
import time
import urllib

import pytest
import testcontainers.compose
from selenium import webdriver

COMPOSE_PATH = "./"


@pytest.fixture(scope="module", autouse=True)
def module_fixture(request):
    """Запуск окружения"""
    print("\nЗапуск docker-compose")
    compose = testcontainers.compose.DockerCompose(COMPOSE_PATH)
    compose.start()
    compose.wait_for("http://localhost:4444/wd/hub/status")
    with urllib.request.urlopen("http://localhost:4444/wd/hub/status") as url:
        data = json.loads(url.read().decode())
        if (data['status']) != '0':
            time.sleep(5)
    time.sleep(5)

    def fin():
        """Остановка окружения"""
        print("\nОстановка docker-compose")
        compose = testcontainers.compose.DockerCompose(COMPOSE_PATH)
        compose.stop()
        print("\n")

    request.addfinalizer(fin)


@pytest.fixture
def browser(request):
    wd = webdriver.Remote("http://localhost:4444/wd/hub",
                          desired_capabilities={'browserName': 'chrome', 'version': '', 'platform': 'ANY',
                                                'javascriptEnabled': True})

    request.addfinalizer(wd.quit)
    return wd


def test_grid(browser):
    """Тестирование грида в докере"""

    browser.get("http://www.google.com")
    if 'Google' not in browser.title:
        raise Exception("Unable to load google page!")
    elem = browser.find_element_by_name("q")
    elem.click()


def test_browserstack():
    """Тестирование в browserstack"""

    desired_cap = {
        'browser': 'Chrome',
        'browser_version': '62.0',
        'os': 'Windows',
        'os_version': '10',
        'resolution': '1024x768',
        'name': 'Bstack-[Python] Sample Test'
    }

    driver = webdriver.Remote(
        command_executor='https://victoriauskova1:GxkfyzdSQUnTpp3pcDUM@hub-cloud.browserstack.com/wd/hub',
        desired_capabilities=desired_cap)

    driver.get("http://www.google.com")
    if 'Google' not in driver.title:
        raise Exception("Unable to load google page!")
    elem = driver.find_element_by_name("q")
    elem.send_keys("BrowserStack")
    elem.submit()
    print(driver.title)
    driver.quit()
