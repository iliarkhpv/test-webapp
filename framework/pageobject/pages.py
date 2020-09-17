from framework.base.default_page import BasePage
from selenium.webdriver.common.by import By
from .element import Button, BaseElement
from string import Template


DAY_FOR_SELECT = (Template('//div[@aria-label="$date"]'))


class WebAppMainPageLocators:
    PROJECT = (Template(f'//a[contains(text(), "$project")]'))
    VARIANT = (By.XPATH, '/html/body/footer/div/p/span')
    PLUS_ADD = (By.XPATH, '//button[contains(text(), "+Add")]')
    NAME_FIELD = (By.XPATH, '//*[@id="projectName"]')
    SUBMIT = (By.XPATH, '//*[@id="addProjectForm"]/button[@type="submit"]')
    IFRAME = 'addProjectFrame'
    CLOSE_POPUP = (By.XPATH, '/html/body/script[10]')
    SAVE_ALERT = (By.CLASS_NAME, 'alert-success')


class WebAppMainPage(BasePage):
    def find_alert_success_field(self):
        return self.find_element(WebAppMainPageLocators.SAVE_ALERT)

    def check_frame_visible(self):
        return self.find_invisible_element(WebAppMainPageLocators.NAME_FIELD)

    def find_project(self, project_name):
        locator = (By.XPATH, WebAppMainPageLocators.PROJECT.substitute(project=project_name))
        return BaseElement(locator, self.driver)

    def open_project(self, project_name):
        locator = (By.XPATH, WebAppMainPageLocators.PROJECT.substitute(project=project_name))
        Button(locator, self.driver).click()

    def get_variant(self):
        return BaseElement(WebAppMainPageLocators.VARIANT, self.driver).get_text()

    def add_project(self):
        Button(WebAppMainPageLocators.PLUS_ADD, self.driver).click()

    def put_project_name(self, name):
        BaseElement(WebAppMainPageLocators.NAME_FIELD, self.driver).send_keys(name)

    def submit_creation(self):
        Button(WebAppMainPageLocators.SUBMIT, self.driver).click()

    def switch_to_iframe(self):
        self.switch_frame(WebAppMainPageLocators.IFRAME)

    def find_script(self):
        return BaseElement(WebAppMainPageLocators.CLOSE_POPUP, self.driver).get_attribute('src')


class ProjectPageLocators:
    HOME_BTN = (By.XPATH, '//a[contains(text(), "Home")]')
    TEST = Template('//a[contains(text(), "$name")]')
    START_TIME = (By.XPATH, '//td[4]')


class ProjectPage(BasePage):
    def get_tests_start_time(self):
        times = []
        for test in self.find_elements(ProjectPageLocators.START_TIME):
            times.append(test.text)
        return times

    def get_test(self, name):
        locator = (By.XPATH, ProjectPageLocators.TEST.substitute(name=name))
        Button(locator, self.driver).click()

    def wait_test_upload(self, name):
        locator = (By.XPATH, ProjectPageLocators.TEST.substitute(name=name))
        return self.find_element(locator)

    def click_home_button(self):
        Button(ProjectPageLocators.HOME_BTN, self.driver).click()


class RunPageLocators:
    FIELD = Template('//p[contains(text(), "$name")]')


class RunPage(BasePage):
    def find_test_field(self, name):
        locator = (By.XPATH, RunPageLocators.FIELD.substitute(name=name))
        return self.find_element(locator)
