from playwright.sync_api import Page
from pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://www.saucedemo.com/inventory.html"
        self.inventory_items = page.locator('[data-test="inventory-item"]')
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.sort_dropdown = page.locator('[data-test="product-sort-container"]')
        self.page_title = page.locator(".title")

    def add_first_item_to_cart(self):
        self.inventory_items.first.get_by_role(
            "button", name="Add to cart"
        ).click()

    def add_item_by_index(self, index: int):
        self.page.get_by_role("button", name="Add to cart").nth(index).click()

    def go_to_cart(self):
        self.cart_link.click()
        self.page.wait_for_url("**/cart.html")

    def sort_by(self, option: str):
        self.sort_dropdown.select_option(option)

    def get_item_count(self):
        return self.inventory_items.count()

    def get_all_prices(self):
        prices = self.page.locator(
            '[data-test="inventory-item-price"]'
        ).all_text_contents()
        return [float(p.replace("$", "")) for p in prices]