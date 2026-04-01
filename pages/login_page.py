from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://www.saucedemo.com"
        self.username_input = page.locator('input[name="user-name"]')
        self.password_input = page.locator('input[name="password"]')
        self.login_button = page.locator('input[name="login-button"]')
        self.error_message = page.locator('[data-test="error"]')

    def navigate_to(self):
        self.navigate(self.url)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self):
        return self.error_message.inner_text()

    def is_error_visible(self):
        return self.error_message.is_visible()