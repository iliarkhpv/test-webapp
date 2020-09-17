from .singleton_browser import get_chrome, get_firefox
from framework.logger import appLogger

BROWSER_CHROME = 'Chrome'
BROWSER_FIREFOX = 'Firefox'


class Browser:
    def factory(browser_name: str):
        if browser_name.lower() == BROWSER_CHROME.lower():
            return Chrome().browser()
        if browser_name.lower() == BROWSER_FIREFOX.lower():
            return Firefox().browser()

    factory = staticmethod(factory)


class Chrome(Browser):
    def browser(self):
        appLogger.debug('Get Chrome driver')
        driver = get_chrome()
        return driver


class Firefox(Browser):
    def browser(self):
        appLogger.debug('Get Firefox driver')
        driver = get_firefox()
        return driver
