import logging
import os
from datetime import date, datetime

import psutil
import pymysql
import pytest
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver import ChromeOptions, DesiredCapabilities
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver, AbstractEventListener


def find_file(file_name):
    """ Find file in sub dirs """

    rootdir = os.getcwd()

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filepath = subdir + os.sep + file

            if filepath.endswith(file_name):
                return filepath
    return "Error"


class BaseListener(AbstractEventListener):
    """event_firing_webdriver listener"""

    def __init__(self):
        self.log_timestamp = str(datetime.datetime.now())[0:-4].replace('-', '.').replace(' ', '_').replace(':', '.')
        self.log_filename = self.log_timestamp + '_file.log'
        self.logfile = open(self.log_filename, 'w')
        self.logdb_filename = (self.log_timestamp + '_log.myd')
        self.logdb = pymysql.connect(self.logdb_filename)
        self.cursor = self.logdb.cursor()
        self.cursor.execute("CREATE TABLE log (timestamp a_string, message a_string)")
        self.logdb.commit()
        self.logdb.close()
        self.logger = logging.getLogger("WebTestApp")

    def _write_log_(self, entry):
        """Function for write information in logfile"""
        self.logfile.write(entry + '\n')

    def _write_log_db_(self, entry):
        """Function for write information in logdb"""
        self.logdb = pymysql.connect(self.logdb_filename)
        self.cursor = self.logdb.cursor()
        timestamp = str(datetime.now())[0:-4].replace('-', '.').replace(' ', '_').replace(':', '.')
        self.cursor.execute("INSERT INTO log VALUES ('{}', '{}')".format(timestamp, entry))
        self.logdb.commit()
        self.logdb.close()

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
        screenshot_timestamp = str(datetime.now())[0:-4].replace('-', '.').replace(' ', '_').replace(':', '.')
        screenshot_filename = screenshot_timestamp + 'exception_screenshot.png'
        print("On exception {}".format(exception))
        self._write_log_("On exception {}".format(exception))
        self._write_log_db_("On exception {}".format(exception))
        driver.save_screenshot('screenshots/' + screenshot_filename)


@pytest.fixture(scope='session', autouse=True)
def proxy():
    """
    Setup and down for proxy.
    :return: browsermob proxy client
    """
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == "browsermob-proxy":
            proc.kill()

    d = {'port': 8090}
    print(find_file('browsermob-proxy'))
    server = Server(find_file('browsermob-proxy'), d)
    server.start()
    proxy = server.create_proxy()
    proxy.new_har(title='project_har')
    yield proxy
    server.stop()


@pytest.fixture(scope='session', autouse=True)
def driver(request, logger, proxy):
    browser = request.config.getoption('--browser')

    if browser == 'chrome':
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--start-fullscreen')
        options.add_argument(f'--proxy-server={proxy.proxy}')
        options.add_experimental_option('w3c', False)
        caps = DesiredCapabilities.CHROME.copy()
        caps['timeouts'] = {'implicit': 20000, 'pageLoad': 20000, 'script': 20000}
        caps['loggingPrefs'] = {'browser': 'ALL'}
        wd = EventFiringWebDriver(webdriver.Chrome(options=options, desired_capabilities=caps),
                                  ChromeListener(logger))
    else:
        raise ValueError('Unsupported browser.')

    yield wd

    wd.quit()


def pytest_addoption(parser):
    parser.addoption('--browser', help='Supported browsers: chrome', default='chrome')


@pytest.fixture(scope='session', autouse=True)
def logger():
    logger = MyLogger(name='session_logger').launch_logger()
    yield logger
    logging.shutdown()


class ChromeListener(BaseListener):

    def after_navigate_to(self, url, driver):
        self.logger.info(f'\nWebDriver log - Opened {url}')
        for s in driver.get_log('browser'):
            self.logger.debug(s)


class MyLogger:

    def __init__(self, name):
        self.name = name

    def launch_logger(self):
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        file_log = logging.FileHandler(f'logs_{date.today()}.log')
        file_log.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_log.setFormatter(file_format)
        logger.addHandler(file_log)
        console_log = logging.StreamHandler()
        console_log.setLevel(logging.DEBUG)
        console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_log.setFormatter(console_format)
        logger.addHandler(console_log)
        return logger
