from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://www.saucedemo.com/cart.html"
        self.cart_items = page.locator('[data-test="inventory-item"]')
        self.checkout_button = page.get_by_role("button", name="Checkout")
        self.continue_shopping = page.get_by_role(
            "button", name="Continue Shopping"
        )

    def get_item_count(self):
        return self.cart_items.count()

    def proceed_to_checkout(self):
        self.checkout_button.click()
        self.page.wait_for_url("**/checkout-step-one.html")