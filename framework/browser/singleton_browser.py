from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


drivers = {}


def get_chrome():
    """
    :return: <class 'selenium.webdriver.chrome.webdriver.WebDriver'>
    """

    instance = drivers.get('chrome')
    if instance is None:
        instance = webdriver.Chrome(ChromeDriverManager().install())
        drivers['chrome'] = instance
    return instance


def get_firefox():
    """
    :return: <class 'selenium.webdriver.chrome.webdriver.WebDriver'>
    """

    instance = drivers.get('firefox')
    if instance is None:
        instance = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        drivers['firefox'] = instance
    return instance
