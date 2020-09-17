from abc import ABC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseElement(ABC):
    def __init__(self, locator: tuple, driver):
        """Initialize element with locator"""
        self.locator = locator
        self.driver = driver

    def get_text(self):
        return self.find_element().text

    def send_keys(self, keys):
        return self.find_element().send_keys(keys)

    def get_attribute(self, attr_name):
        return self.find_element().get_attribute(attr_name)

    def clear_field(self):
        return self.find_element().clear()

    def find_element(self, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(self.locator),
                                                      message=f"Can't find element by locator {self.locator}")

    def find_elements(self, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(self.locator),
                                                      message=f"Can't find elements by locator {self.locator}")

    def find_invisible_element(self, time=10):
        return WebDriverWait(self.driver, time).until(EC.invisibility_of_element_located(self.locator),
                                                      message=f"Can`t find element by locator {self.locator}")


class DriverElement:
    @staticmethod
    def get_element_attribute(element, attr_name):
        return element.get_attribute(attr_name)

    @staticmethod
    def get_element_text(element):
        return element.text


class Button(BaseElement):
    def __init__(self, locator, driver):
        super().__init__(locator, driver)

    def click(self):
        self.find_element().click()


class IFrame(BaseElement):
    def __init__(self, locator, driver):
        super().__init__(locator, driver)

    def switch_to_iframe(self):
        iframe = self.find_element()
        self.driver.switch_to.frame(iframe)

    def switch_to_mainpage(self):
        self.driver.switch_to.default_content()

