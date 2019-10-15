import logging
import os
from datetime import date

import psutil
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


class BaseListener(AbstractEventListener):

    def __init__(self, logger):
        self.logger = logger

    def on_exception(self, exception, driver):
        driver.save_screenshot(f'{driver.current_url}-{driver.name}{date.today()}.png')
        self.logger.error(exception)

    def before_navigate_to(self, url, driver):
        self.logger.info(f'\nWebDriver log - Going to {url}')

    def after_navigate_to(self, url, driver):
        self.logger.info(f'\nWebDriver log - Opened {url}')


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
