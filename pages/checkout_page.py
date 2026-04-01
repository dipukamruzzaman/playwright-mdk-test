from playwright.sync_api import Page
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_button = page.get_by_role("button", name="Continue")
        self.finish_button = page.get_by_role("button", name="Finish")
        self.complete_header = page.locator('[data-test="complete-header"]')
        self.error_message = page.locator('[data-test="error"]')
        self.subtotal = page.locator('[data-test="subtotal-label"]')
        self.tax = page.locator('[data-test="tax-label"]')

    def fill_information(self, first: str, last: str, postal: str):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)

    def continue_to_summary(self):
        self.continue_button.click()
        self.page.wait_for_url("**/checkout-step-two.html")

    def finish_checkout(self):
        self.finish_button.click()
        self.page.wait_for_url("**/checkout-complete.html")

    def get_confirmation_text(self):
        return self.complete_header.inner_text()