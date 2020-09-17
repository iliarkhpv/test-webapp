class BaseEntity:
    def __init__(self, driver):
        self.driver = driver

    def go_to_site(self, base_url):
        return self.driver.get(base_url)

    def refresh_page(self):
        return self.driver.refresh()

    def complete_basic_auth_with_token(self, url, login, password):
        self.go_to_site(
            url.replace('http://', f'http://{login}:{password}@'))

    def add_cookie(self, name, value):
        cookie = {'name': name,
                  'value': value}
        self.driver.add_cookie(cookie)

    def execute_script(self, script):
        self.driver.execute_script(script)

    def wait(self, time=0.3):
        self.driver.implicitly_wait(time)

    def take_screenshot(self, name):
        scr_name = f"{name}_screenshot.png"
        self.driver.save_screenshot(scr_name)
        return scr_name

