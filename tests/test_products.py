import pytest
from playwright.sync_api import Page, expect
from conftest import BASE_URL


def test_products_page_has_items(logged_in_page: Page):
    items = logged_in_page.locator('[data-test="inventory-item"]')
    expect(items).to_have_count(6)


def test_product_has_name_price_and_button(logged_in_page: Page):
    first_item = logged_in_page.locator('[data-test="inventory-item"]').first
    expect(first_item.locator('[data-test="inventory-item-name"]')).to_be_visible()
    expect(first_item.locator('[data-test="inventory-item-price"]')).to_be_visible()
    expect(first_item.get_by_role("button", name="Add to cart")).to_be_visible()


def test_add_single_item_to_cart(logged_in_page: Page):
    logged_in_page.locator(
        '[data-test="inventory-item"]'
    ).first.get_by_role("button", name="Add to cart").click()
    expect(logged_in_page.locator(".shopping_cart_badge")).to_have_text("1")


def test_add_multiple_items_to_cart(logged_in_page: Page):
    buttons = logged_in_page.get_by_role("button", name="Add to cart")
    buttons.nth(0).click()
    buttons.nth(1).click()
    buttons.nth(2).click()
    expect(logged_in_page.locator(".shopping_cart_badge")).to_have_text("3")


def test_remove_item_from_cart(logged_in_page: Page):
    logged_in_page.locator(
        '[data-test="inventory-item"]'
    ).first.get_by_role("button", name="Add to cart").click()
    expect(logged_in_page.locator(".shopping_cart_badge")).to_have_text("1")
    logged_in_page.locator(
        '[data-test="inventory-item"]'
    ).first.get_by_role("button", name="Remove").click()
    expect(logged_in_page.locator(".shopping_cart_badge")).to_have_count(0)


def test_sort_products_by_price_low_to_high(logged_in_page: Page):
    logged_in_page.locator(
        '[data-test="product-sort-container"]'
    ).select_option("lohi")
    prices = logged_in_page.locator(
        '[data-test="inventory-item-price"]'
    ).all_text_contents()
    price_values = [float(p.replace("$", "")) for p in prices]
    assert price_values == sorted(price_values)