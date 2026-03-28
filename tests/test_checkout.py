import pytest
from playwright.sync_api import Page, expect
from conftest import BASE_URL


def test_navigate_to_cart(cart_page: Page):
    expect(cart_page).to_have_url(f"{BASE_URL}/cart.html")
    expect(cart_page.locator('[data-test="inventory-item"]')).to_have_count(1)


def test_cart_shows_correct_item(logged_in_page: Page):
    first_item = logged_in_page.locator('[data-test="inventory-item"]').first
    item_name = first_item.locator(
        '[data-test="inventory-item-name"]'
    ).inner_text()
    first_item.get_by_role("button", name="Add to cart").click()
    logged_in_page.locator(".shopping_cart_link").click()
    logged_in_page.wait_for_url(f"{BASE_URL}/cart.html")
    expect(
        logged_in_page.locator('[data-test="inventory-item-name"]')
    ).to_have_text(item_name)


def test_checkout_step_one(checkout_page: Page):
    checkout_page.fill('[data-test="firstName"]', "John")
    checkout_page.fill('[data-test="lastName"]', "Doe")
    checkout_page.fill('[data-test="postalCode"]', "12345")
    checkout_page.get_by_role("button", name="Continue").click()
    checkout_page.wait_for_url(f"{BASE_URL}/checkout-step-two.html")
    expect(checkout_page).to_have_url(f"{BASE_URL}/checkout-step-two.html")


def test_checkout_step_two_shows_summary(checkout_page: Page):
    checkout_page.fill('[data-test="firstName"]', "John")
    checkout_page.fill('[data-test="lastName"]', "Doe")
    checkout_page.fill('[data-test="postalCode"]', "12345")
    checkout_page.get_by_role("button", name="Continue").click()
    checkout_page.wait_for_url(f"{BASE_URL}/checkout-step-two.html")
    expect(
        checkout_page.locator('[data-test="inventory-item-name"]')
    ).to_be_visible()
    expect(checkout_page.locator('[data-test="subtotal-label"]')).to_be_visible()
    expect(checkout_page.locator('[data-test="tax-label"]')).to_be_visible()


def test_complete_checkout_flow(checkout_page: Page):
    checkout_page.fill('[data-test="firstName"]', "John")
    checkout_page.fill('[data-test="lastName"]', "Doe")
    checkout_page.fill('[data-test="postalCode"]', "12345")
    checkout_page.get_by_role("button", name="Continue").click()
    checkout_page.wait_for_url(f"{BASE_URL}/checkout-step-two.html")
    checkout_page.get_by_role("button", name="Finish").click()
    checkout_page.wait_for_url(f"{BASE_URL}/checkout-complete.html")
    expect(checkout_page.locator('[data-test="complete-header"]')).to_have_text(
        "Thank you for your order!"
    )


def test_checkout_requires_first_name(checkout_page: Page):
    checkout_page.fill('[data-test="lastName"]', "Doe")
    checkout_page.fill('[data-test="postalCode"]', "12345")
    checkout_page.get_by_role("button", name="Continue").click()
    expect(checkout_page.locator('[data-test="error"]')).to_contain_text(
        "First Name is required"
    )