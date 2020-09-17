from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .default_browser import BaseEntity


class BasePage(BaseEntity):
    def find_invisible_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.invisibility_of_element_located(locator),
                                                      message=f"Can`t find element by locator {locator}")

    def find_elements(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                      message=f"Can't find elements by locator {locator}")

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    def switch_to_mainpage(self):
        return self.driver.switch_to.default_content()

    def switch_to_alert(self):
        return self.driver.switch_to.alert

    def accept_alert(self):
        return self.driver.switch_to.alert.accept()

    def get_alert_msg(self):
        return self.driver.switch_to.alert.text

    def switch_to_active(self):
        return self.driver.switch_to_active_element()

    def switch_frame(self, frame_name):
        return self.driver.switch_to.frame(frame_name)

