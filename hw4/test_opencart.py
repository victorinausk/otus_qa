""" Tests for opencart main page """

def test_chrome(chrome_browser, request, module_fixture):
    """ Test open opencart main page in Chrome """
    chrome_browser.get(request.config.getoption('--opencart_url'))
    assert chrome_browser.current_url == request.config.getoption('--opencart_url')

def test_firefox(firefox_browser, request, module_fixture):
    """ Test open opencart main page in Firefox """
    firefox_browser.get(request.config.getoption('--opencart_url'))
    assert firefox_browser.current_url == request.config.getoption('--opencart_url')