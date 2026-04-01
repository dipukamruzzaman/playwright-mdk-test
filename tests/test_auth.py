import pytest
import json
import os
from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com"


def test_auth_state_file_exists():
    """Auth state file should exist after save_auth.py is run"""
    assert os.path.exists("auth/auth_state.json"), \
        "Run python auth/save_auth.py first"


def test_auth_state_contains_cookies():
    """Auth state file should contain valid cookies"""
    with open("auth/auth_state.json") as f:
        state = json.load(f)
    assert "cookies" in state
    assert len(state["cookies"]) > 0


def test_authenticated_landing_page(logged_in_page: Page):
    """After login should land on inventory page"""
    expect(logged_in_page).to_have_url(f"{BASE_URL}/inventory.html")
    expect(logged_in_page.locator(".title")).to_contain_text("Products")


def test_logout_clears_session(logged_in_page: Page):
    """Logging out should redirect to login page"""
    logged_in_page.locator('#react-burger-menu-btn').click()
    logged_in_page.wait_for_selector(
        '[data-test="logout-sidebar-link"]',
        state="visible"
    )
    logged_in_page.locator('[data-test="logout-sidebar-link"]').click()
    expect(logged_in_page).to_have_url(f"{BASE_URL}/")
    expect(logged_in_page.locator(
        'input[name="user-name"]'
    )).to_be_visible()


def test_direct_url_access_without_auth(page: Page):
    """Accessing inventory directly without auth should redirect to login"""
    page.goto(f"{BASE_URL}/inventory.html")
    expect(page).to_have_url(f"{BASE_URL}/")


def test_session_persists_across_navigation(logged_in_page: Page):
    """Auth session should persist when navigating between pages"""
    logged_in_page.locator(".shopping_cart_link").click()
    expect(logged_in_page).to_have_url(f"{BASE_URL}/cart.html")
    logged_in_page.go_back()
    expect(logged_in_page).to_have_url(f"{BASE_URL}/inventory.html")


def test_multiple_users_login(page: Page):
    """Different user types should have different behaviours"""
    users = [
        ("standard_user", "secret_sauce", True),
        ("locked_out_user", "secret_sauce", False),
        ("problem_user", "secret_sauce", True),
    ]
    for username, password, should_succeed in users:
        page.goto(BASE_URL)
        page.fill('input[name="user-name"]', username)
        page.fill('input[name="password"]', password)
        page.click('input[name="login-button"]')
        if should_succeed:
            expect(page).to_have_url(f"{BASE_URL}/inventory.html")
        else:
            expect(page.locator('[data-test="error"]')).to_be_visible()