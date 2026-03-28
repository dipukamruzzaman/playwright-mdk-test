import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com"
TEST_USERNAME = "standard_user"
TEST_PASSWORD = "secret_sauce"

def test_login_page_loads(page: Page):
    """Check the login page is accessible"""
    page.goto(BASE_URL)
    expect(page).to_have_title("Swag Labs")

def test_valid_login(page: Page):
    """Login with valid credentials"""
    page.goto(BASE_URL)
    page.fill('input[name="user-name"]', TEST_USERNAME)
    page.fill('input[name="password"]', TEST_PASSWORD)
    page.click('input[name="login-button"]')
    expect(page).to_have_url(f"{BASE_URL}/inventory.html")
    expect(page.locator(".title")).to_contain_text("Products")

def test_invalid_login(page: Page):
    """Login with wrong credentials should show error"""
    page.goto(BASE_URL)
    page.fill('input[name="user-name"]', "wrong_user")
    page.fill('input[name="password"]', "wrong_pass")
    page.click('input[name="login-button"]')
    expect(page.locator('[data-test="error"]')).to_be_visible()
    expect(page.locator('[data-test="error"]')).to_contain_text("Username and password do not match")

def test_login_fields_are_empty_on_load(page: Page):
    """Username and password fields should be empty on fresh load"""
    page.goto(BASE_URL)
    expect(page.locator('input[name="user-name"]')).to_have_value("")
    expect(page.locator('input[name="password"]')).to_have_value("")

def test_locked_out_user(page: Page):
    """Locked out user should see specific error message"""
    page.goto(BASE_URL)
    page.fill('input[name="user-name"]', "locked_out_user")
    page.fill('input[name="password"]', "secret_sauce")
    page.click('input[name="login-button"]')
    expect(page.locator('[data-test="error"]')).to_contain_text("Sorry, this user has been locked out")