"""Module with fixtures for log tests"""
import datetime
import logging
import os
import urllib.parse

import pytest
import testcontainers.compose
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as Chrome_options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as Firefox_options
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
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


COMPOSE_PATH = "./"


@pytest.fixture(scope='module', autouse=True)
def open_login_page(driver, request):
    url = 'admin/'
    login_page_url = ''.join((request.config.getoption('--opencart_url'), url))
    return driver.get(login_page_url)


@pytest.fixture(scope="module", autouse=True)
def module_fixture(request):
    """Запуск окружения"""
    print("\nЗапуск docker-compose")
    compose = testcontainers.compose.DockerCompose(COMPOSE_PATH)
    compose.start()
    compose.wait_for("http://localhost/")

    def fin():
        """Остановка окружения"""
        print("\nОстановка docker-compose")
        compose = testcontainers.compose.DockerCompose(COMPOSE_PATH)
        compose.stop()
        print("\n")
        print("\n================================== HW 20 ============================================================")
        print("\n")

    request.addfinalizer(fin)


def log():
    """Function for logging"""
    log_timestamp = str(datetime.datetime.now())[0:-4].replace('-', '.').replace(' ', '_').replace(':', '.')
    logger = logging.getLogger("WebTestApp")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_timestamp + "_logging.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info("-----------------------------")
    logger.info("Program started")


class MyListener(AbstractEventListener):
    """event_firing_webdriver listener"""
    __engine = create_engine('sqlite:///./log.db', echo=True)

    def __init__(self):
        self.log_timestamp = str(datetime.today().strftime("%Y%m%d"))
        self.log_filename = self.log_timestamp + '_file.log'
        self.logfile = open(self.log_filename, 'w')
        self.__engine.execute("CREATE TABLE IF NOT EXISTS log (timestamp a_string, message a_string)")
        log()
        self.logger = logging.getLogger("WebTestApp")

    def _write_log_(self, entry):
        """Function for write information in logfile"""
        self.logfile.write(entry + '\n')

    def _write_log_db_(self, entry):
        """Function for write information in logdb"""
        timestamp = str(datetime.today().strftime("%Y%m%d"))
        self.__engine.execute("INSERT INTO log VALUES ('{}', '{}')".format(timestamp, entry))

    def before_navigate_to(self, url, driver):
        print("Before navigate to {}".format(url))
        self._write_log_("Before navigate to {}".format(url))
        self._write_log_db_("Before navigate to {}".format(url))
        self.logger.info("Before navigate to {}".format(url))

    def after_navigate_to(self, url, driver):
        print("After navigate to {}".format(url))
        self._write_log_("After navigate to {}".format(url))
        self._write_log_db_("After navigate to {}".format(url))
        self.logger.info("After navigate to {}".format(url))

    def before_find(self, by, value, driver):
        print("Before find {} {}".format(by, value))
        self._write_log_("Before find {} {}".format(by, value))
        value = value.replace("'", '"')
        self._write_log_db_('Before find {} {}'.format(by, value))
        self.logger.info("Before find {} {}".format(by, value))

    def after_find(self, by, value, driver):
        print("After find {} {}".format(by, value))
        self._write_log_("After find {} {}".format(by, value))
        value = value.replace("'", '"')
        self._write_log_db_('After find {} {}'.format(by, value))
        self.logger.info("After find {} {}".format(by, value))

    def before_click(self, element, driver):
        print("Before click {}".format(element))
        self._write_log_("Before click {}".format(element.get_attribute("class")))
        self._write_log_db_("Before click {}".format(element.get_attribute("class")))
        self.logger.info("Before click {}".format(element.get_attribute("class")))

    def after_click(self, element, driver):
        print("After click")
        self._write_log_("After click")
        self._write_log_db_("After click")
        self.logger.info("After click")

    def before_execute_script(self, script, driver):
        print("Before execute script {}".format(script))
        self._write_log_("Before execute script {}".format(script))
        self._write_log_db_("Before execute script {}".format(script))
        self.logger.info("Before execute script {}".format(script))

    def after_execute_script(self, script, driver):
        print("After execute script {}".format(script))
        self._write_log_("After execute script {}".format(script))
        self._write_log_db_("After execute script {}".format(script))
        self.logger.info("After execute script {}".format(script))

    def before_close(self, driver):
        print("Before close")
        self._write_log_("Before close")
        self._write_log_db_("Before close")
        self.logger.info("Before close")

    def after_close(self, driver):
        print("After close")
        self._write_log_("After close")
        self._write_log_db_("After close")
        self.logger.info("After close")

    def before_quit(self, driver):
        print("Before quit")
        self._write_log_("Before quit")
        self._write_log_db_("Before quit")
        self.logger.info("Before quit")

    def after_quit(self, driver):
        print("After quit")
        self._write_log_("After quit")
        self._write_log_db_("After quit")
        self.logger.info("After quit")

    def on_exception(self, exception, driver):
        screenshot_timestamp = str(datetime.today().strftime("%Y%m%d"))
        screenshot_filename = screenshot_timestamp + 'exception_screenshot.png'
        print("On exception {}".format(exception))
        self._write_log_("On exception {}".format(exception))
        self._write_log_db_("On exception {}".format(exception))
        driver.save_screenshot('screenshots/' + screenshot_filename)


def pytest_addoption(parser):
    """Addoption fixture: browser type, url, headless option"""
    parser.addoption(
        "--browser", action="store", default="chrome", help="browser option"
    )
    parser.addoption(
        "--opencart_url", action="store", default="http://localhost/", help="url option"
    )
    parser.addoption(
        "--window_option", action="store", default="headless", help="window option"
    )
    parser.addoption(
        "--waits", action="store", default="no_wait", help="wait option"
    )
    parser.addoption(
        "--wait_time", action="store", default=10, help="wait time option"
    )


@pytest.fixture(scope='module', autouse=True)
def cmdopt_browser(request):
    """browser type option"""
    return request.config.getoption("--browser")


@pytest.fixture(scope='module', autouse=True)
def cmdopt_url(request):
    """url options"""
    return request.config.getoption("--opencart_url")


@pytest.fixture(scope='module', autouse=True)
def cmdopt_window(request):
    """window option"""
    return request.config.getoption("--window_option")


@pytest.fixture
def cmdopt_waits(request):
    """wait option"""
    return request.config.getoption("--waits")


@pytest.fixture
def cmdopt_wait_time(request):
    """wait time option"""
    return request.config.getoption("--wait_time")


@pytest.fixture(scope='module', autouse=True)
def driver(request, cmdopt_browser, cmdopt_window):
    """Fixture to create, return and close driver"""
    server = Server(find_file('browsermob-proxy'), {"port": 9090})
    server.start()
    proxy = server.create_proxy()
    url = urllib.parse.urlparse(proxy.proxy).path
    driver = None
    if cmdopt_browser == "ie":
        driver = webdriver.Ie()
    elif cmdopt_browser == "firefox":
        if cmdopt_window == "headless":
            options = Firefox_options()
            options.add_argument("--headless")
            options.add_argument('--proxy-server={}'.format(url))
            driver = webdriver.Firefox(firefox_options=options)
        else:
            options = Firefox_options()
            options.add_argument('--proxy-server={}'.format(url))
            driver = webdriver.Firefox()
        proxy.new_har()
        request.addfinalizer(driver.quit)
    elif cmdopt_browser == "chrome":
        if cmdopt_window == "headless":
            options = Chrome_options()
            options.headless = True
            options.add_argument('--proxy-server={}'.format(url))
            driver = webdriver.Chrome(options=options)
            proxy.new_har()
            request.addfinalizer(driver.quit)
        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server={}'.format(url))
            d = DesiredCapabilities.CHROME
            d['loggingPrefs'] = {'browser': 'ALL'}
            driver = webdriver.Chrome(desired_capabilities=d, options=chrome_options)
            proxy.new_har()
            ef_driver = EventFiringWebDriver(driver, MyListener())

            def fin():
                log_timestamp = str(datetime.today().strftime("%Y%m%d"))
                browserlog_filename = log_timestamp + '_browser_log_file.log'
                browserlogfile = open(browserlog_filename, 'w')
                print('-------------------------')
                for i in ef_driver.get_log('browser'):
                    print(i)
                    browserlogfile.write(str(i) + '\n')

                print(proxy.har)
                server.stop()
                ef_driver.quit

            request.addfinalizer(fin)
            return ef_driver
    else:
        return "unsupported browser"

    return driver


@pytest.fixture
def add_waits(get_driver, cmdopt_wait_time):
    """fixture for add waits"""
    driver = get_driver
    if cmdopt_waits == "waits":
        driver.implicitly_wait(cmdopt_wait_time)
    else:
        pass
    return driver
