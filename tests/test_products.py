import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com"
TEST_USERNAME = "standard_user"
TEST_PASSWORD = "secret_sauce"


def login(page: Page):
    """Reusable login helper"""
    page.goto(BASE_URL)
    page.fill('input[name="user-name"]', TEST_USERNAME)
    page.fill('input[name="password"]', TEST_PASSWORD)
    page.click('input[name="login-button"]')


def test_products_page_has_items(page: Page):
    """Products page should display inventory items"""
    login(page)
    items = page.locator('[data-test="inventory-item"]')
    expect(items).to_have_count(6)


def test_product_has_name_price_and_button(page: Page):
    """Each product should show name, price and add to cart button"""
    login(page)
    first_item = page.locator('[data-test="inventory-item"]').first
    expect(first_item.locator('[data-test="inventory-item-name"]')).to_be_visible()
    expect(first_item.locator('[data-test="inventory-item-price"]')).to_be_visible()
    expect(first_item.get_by_role("button", name="Add to cart")).to_be_visible()


def test_add_single_item_to_cart(page: Page):
    """Adding an item should update cart badge to 1"""
    login(page)
    page.locator('[data-test="inventory-item"]').first.get_by_role(
        "button", name="Add to cart"
    ).click()
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")


def test_add_multiple_items_to_cart(page: Page):
    """Adding 3 items should update cart badge to 3"""
    login(page)
    buttons = page.get_by_role("button", name="Add to cart")
    buttons.nth(0).click()
    buttons.nth(1).click()
    buttons.nth(2).click()
    expect(page.locator(".shopping_cart_badge")).to_have_text("3")


def test_remove_item_from_cart(page: Page):
    """Removing an item should update cart badge"""
    login(page)
    page.locator('[data-test="inventory-item"]').first.get_by_role(
        "button", name="Add to cart"
    ).click()
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")
    page.locator('[data-test="inventory-item"]').first.get_by_role(
        "button", name="Remove"
    ).click()
    expect(page.locator(".shopping_cart_badge")).to_have_count(0)


def test_sort_products_by_price_low_to_high(page: Page):
    """Sorting by price low-high should reorder products"""
    login(page)
    page.locator('[data-test="product-sort-container"]').select_option("lohi")
    prices = page.locator('[data-test="inventory-item-price"]').all_text_contents()
    price_values = [float(p.replace("$", "")) for p in prices]
    assert price_values == sorted(price_values), "Prices are not sorted low to high"