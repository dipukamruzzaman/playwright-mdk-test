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
    page.wait_for_url(f"{BASE_URL}/inventory.html")


def add_item_to_cart(page: Page):
    """Add first item to cart"""
    page.locator('[data-test="inventory-item"]').first.get_by_role(
        "button", name="Add to cart"
    ).click()


def test_navigate_to_cart(page: Page):
    """User can navigate to cart after adding item"""
    login(page)
    add_item_to_cart(page)
    page.locator(".shopping_cart_link").click()
    page.wait_for_url(f"{BASE_URL}/cart.html")
    expect(page).to_have_url(f"{BASE_URL}/cart.html")
    expect(page.locator('[data-test="inventory-item"]')).to_have_count(1)


def test_cart_shows_correct_item(page: Page):
    """Cart should display the correct item name and price"""
    login(page)
    first_item = page.locator('[data-test="inventory-item"]').first
    item_name = first_item.locator(
        '[data-test="inventory-item-name"]'
    ).inner_text()
    add_item_to_cart(page)
    page.locator(".shopping_cart_link").click()
    page.wait_for_url(f"{BASE_URL}/cart.html")
    expect(page.locator('[data-test="inventory-item-name"]')).to_have_text(
        item_name
    )


def test_checkout_step_one(page: Page):
    """User can fill in checkout information"""
    login(page)
    add_item_to_cart(page)
    page.locator(".shopping_cart_link").click()
    page.wait_for_url(f"{BASE_URL}/cart.html")
    page.get_by_role("button", name="Checkout").click()
    page.wait_for_url(f"{BASE_URL}/checkout-step-one.html")
    page.fill('[data-test="firstName"]', "John")
    page.fill('[data-test="lastName"]', "Doe")
    page.fill('[data-test="postalCode"]', "12345")
    page.get_by_role("button", name="Continue").click()
    page.wait_for_url(f"{BASE_URL}/checkout-step-two.html")
    expect(page).to_have_url(f"{BASE_URL}/checkout-step-two.html")


def test_checkout_step_two_shows_summary(page: Page):
    """Order summary page should show item and price"""
    login(page)
    add_item_to_cart(page)
    page.locator(".shopping_cart_link").click()
    page.get_by_role("button", name="Checkout").click()
    page.fill('[data-test="firstName"]', "John")
    page.fill('[data-test="lastName"]', "Doe")
    page.fill('[data-test="postalCode"]', "12345")
    page.get_by_role("button", name="Continue").click()
    page.wait_for_url(f"{BASE_URL}/checkout-step-two.html")
    expect(page.locator('[data-test="inventory-item-name"]')).to_be_visible()
    expect(page.locator('[data-test="subtotal-label"]')).to_be_visible()
    expect(page.locator('[data-test="tax-label"]')).to_be_visible()


def test_complete_checkout_flow(page: Page):
    """Full end-to-end checkout — the money test"""
    login(page)
    add_item_to_cart(page)
    page.locator(".shopping_cart_link").click()
    page.wait_for_url(f"{BASE_URL}/cart.html")
    expect(page.locator('[data-test="inventory-item"]')).to_have_count(1)
    page.get_by_role("button", name="Checkout").click()
    page.wait_for_url(f"{BASE_URL}/checkout-step-one.html")
    page.fill('[data-test="firstName"]', "John")
    page.fill('[data-test="lastName"]', "Doe")
    page.fill('[data-test="postalCode"]', "12345")
    page.get_by_role("button", name="Continue").click()
    page.wait_for_url(f"{BASE_URL}/checkout-step-two.html")
    page.get_by_role("button", name="Finish").click()
    page.wait_for_url(f"{BASE_URL}/checkout-complete.html")
    expect(page.locator('[data-test="complete-header"]')).to_have_text(
        "Thank you for your order!"
    )
    expect(page.locator('[data-test="complete-text"]')).to_be_visible()


def test_checkout_requires_first_name(page: Page):
    """Checkout should fail if first name is missing"""
    login(page)
    add_item_to_cart(page)
    page.locator(".shopping_cart_link").click()
    page.get_by_role("button", name="Checkout").click()
    page.fill('[data-test="lastName"]', "Doe")
    page.fill('[data-test="postalCode"]', "12345")
    page.get_by_role("button", name="Continue").click()
    expect(page.locator('[data-test="error"]')).to_contain_text(
        "First Name is required"
    )