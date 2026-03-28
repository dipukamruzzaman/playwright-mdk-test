import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://parabank.parasoft.com/parabank"

TEST_USERNAME = "testuser01"
TEST_PASSWORD = "Test1234!"

def test_login_page_loads(page: Page):
    """Check the login page is accessible"""
    page.goto(f"{BASE_URL}/index.htm")
    expect(page).to_have_title("ParaBank | Welcome | Online Banking")

def test_debug_login(page: Page):
    """Temporary debug test - see what happens after login click"""
    page.goto(f"{BASE_URL}/index.htm")
    page.fill('input[name="username"]', TEST_USERNAME)
    page.fill('input[name="password"]', TEST_PASSWORD)
    page.click('input[value="Log In"]')
    page.wait_for_timeout(3000)  # wait 3 seconds
    page.screenshot(path="debug_after_login.png")  # take a screenshot
    print(f"\nCurrent URL: {page.url}")
    print(f"Page title: {page.title()}")

def test_valid_login(page: Page):
    """Login with valid credentials"""
    page.goto(f"{BASE_URL}/index.htm")
    page.fill('input[name="username"]', TEST_USERNAME)
    page.fill('input[name="password"]', TEST_PASSWORD)
    page.click('input[value="Log In"]')
    # More resilient — checks URL contains overview, ignores session params
    expect(page).to_have_url(f"{BASE_URL}/overview.htm")
    expect(page.get_by_role("heading", name="Accounts Overview")).to_be_visible()

def test_invalid_login(page: Page):
    """Login with wrong credentials should show error"""
    page.goto(f"{BASE_URL}/index.htm")
    page.fill('input[name="username"]', "wronguser")
    page.fill('input[name="password"]', "wrongpass")
    page.click('input[value="Log In"]')
    expect(page.locator(".error")).to_be_visible()

def test_login_fields_are_empty_on_load(page: Page):
    """Username and password fields should be empty on fresh load"""
    page.goto(f"{BASE_URL}/index.htm")
    expect(page.locator('input[name="username"]')).to_have_value("")
    expect(page.locator('input[name="password"]')).to_have_value("")