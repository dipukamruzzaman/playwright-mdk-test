import pytest
from playwright.sync_api import Page, expect
from conftest import BASE_URL


def test_login_with_pom(login_page, page: Page):
    """Login using Page Object Model"""
    login_page.navigate_to()
    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url(f"{BASE_URL}/inventory.html")


def test_invalid_login_with_pom(login_page):
    """Invalid login shows error via POM"""
    login_page.navigate_to()
    login_page.login("wrong_user", "wrong_pass")
    assert login_page.is_error_visible()
    assert "do not match" in login_page.get_error_message()


def test_inventory_item_count(inventory_page):
    """Products page has 6 items via POM"""
    assert inventory_page.get_item_count() == 6


def test_add_item_updates_cart(inventory_page):
    """Adding item updates cart badge via POM"""
    inventory_page.add_first_item_to_cart()
    expect(inventory_page.cart_badge).to_have_text("1")


def test_cart_has_one_item(cart_page_obj):
    """Cart has one item via POM"""
    assert cart_page_obj.get_item_count() == 1


def test_full_checkout_with_pom(checkout_page_obj):
    """Full checkout flow via POM"""
    checkout_page_obj.fill_information("John", "Doe", "12345")
    checkout_page_obj.continue_to_summary()
    expect(checkout_page_obj.subtotal).to_be_visible()
    checkout_page_obj.finish_checkout()
    assert checkout_page_obj.get_confirmation_text() == "Thank you for your order!"


def test_price_sort_with_pom(inventory_page):
    """Prices sort correctly via POM"""
    inventory_page.sort_by("lohi")
    prices = inventory_page.get_all_prices()
    assert prices == sorted(prices)