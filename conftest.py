import pytest
from playwright.sync_api import Page

BASE_URL = "https://www.saucedemo.com"
TEST_USERNAME = "standard_user"
TEST_PASSWORD = "secret_sauce"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }

@pytest.fixture
def logged_in_page(page: Page):
    """Fixture that returns a page already logged in to SauceDemo"""
    page.goto(BASE_URL)
    page.fill('input[name="user-name"]', TEST_USERNAME)
    page.fill('input[name="password"]', TEST_PASSWORD)
    page.click('input[name="login-button"]')
    page.wait_for_url(f"{BASE_URL}/inventory.html")
    yield page


@pytest.fixture
def cart_page(logged_in_page: Page):
    """Fixture that returns a page with one item already in cart"""
    logged_in_page.locator(
        '[data-test="inventory-item"]'
    ).first.get_by_role("button", name="Add to cart").click()
    logged_in_page.locator(".shopping_cart_link").click()
    logged_in_page.wait_for_url(f"{BASE_URL}/cart.html")
    yield logged_in_page


@pytest.fixture
def checkout_page(cart_page: Page):
    """Fixture that returns a page at checkout step one"""
    cart_page.get_by_role("button", name="Checkout").click()
    cart_page.wait_for_url(f"{BASE_URL}/checkout-step-one.html")
    yield cart_page

@pytest.fixture(scope="function", autouse=True)
def trace_on_failure(page: Page, request):
    """Automatically capture trace on test failure"""
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    trace_path = f"traces/{request.node.name}.zip"
    page.context.tracing.stop(path=trace_path)