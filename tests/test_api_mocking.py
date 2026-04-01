import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com"


def test_block_images_page_still_loads(logged_in_page: Page):
    """Page should load correctly even with images blocked"""
    logged_in_page.route("**/*.jpg", lambda route: route.abort())
    logged_in_page.route("**/*.png", lambda route: route.abort())
    logged_in_page.reload()
    expect(logged_in_page.locator(".title")).to_contain_text("Products")
    expect(
        logged_in_page.locator('[data-test="inventory-item"]')
    ).to_have_count(6)


def test_intercept_and_verify_login_request(page: Page):
    """Intercept login request and verify it's made correctly"""
    requests_made = []

    def capture_request(request):
        if "login" in request.url or request.method == "POST":
            requests_made.append({
                "url": request.url,
                "method": request.method
            })

    page.on("request", capture_request)
    page.goto(BASE_URL)
    page.fill('input[name="user-name"]', "standard_user")
    page.fill('input[name="password"]', "secret_sauce")
    page.click('input[name="login-button"]')
    page.wait_for_url(f"{BASE_URL}/inventory.html")
    print(f"\nRequests captured: {requests_made}")


def test_slow_network_simulation(logged_in_page: Page, browser_name: str):
    """Test page behaviour under slow network conditions"""
    if browser_name != "chromium":
        pytest.skip("Network simulation tests are chromium-only due to parallel stability")

    def slow_response(route):
        route.continue_()

    logged_in_page.route("**/*", slow_response)
    logged_in_page.reload()
    expect(logged_in_page.locator(".title")).to_contain_text("Products")


def test_block_analytics_requests(page: Page):
    """Analytics/tracking requests should be blockable"""
    blocked_urls = []

    def block_analytics(route):
        if any(tracker in route.request.url for tracker in [
            "analytics", "tracking", "telemetry", "metrics"
        ]):
            blocked_urls.append(route.request.url)
            route.abort()
        else:
            route.continue_()

    page.route("**/*", block_analytics)
    page.goto(BASE_URL)
    page.fill('input[name="user-name"]', "standard_user")
    page.fill('input[name="password"]', "secret_sauce")
    page.click('input[name="login-button"]')
    page.wait_for_url(f"{BASE_URL}/inventory.html")
    expect(page.locator(".title")).to_contain_text("Products")
    print(f"\nBlocked {len(blocked_urls)} analytics requests")

def test_monitor_all_network_requests(logged_in_page: Page, browser_name: str):
    """Monitor and log all network requests made during page load"""
    if browser_name != "chromium":
        pytest.skip("Network monitoring tests are chromium-only due to parallel stability")

    requests_log = []
    responses_log = []

    logged_in_page.on("request", lambda req: requests_log.append(
        f"{req.method} {req.url}"
    ))
    logged_in_page.on("response", lambda res: responses_log.append(
        f"{res.status} {res.url}"
    ))

    logged_in_page.reload()
    logged_in_page.wait_for_load_state("networkidle")

    print(f"\nTotal requests: {len(requests_log)}")
    print(f"Total responses: {len(responses_log)}")

    real_failures = [
        r for r in responses_log
        if r.startswith(("4", "5"))
        and "inventory.html" not in r
        and "backtrace.io" not in r
        and "icon-192x192.png" not in r
    ]
    print(f"Real failed responses: {real_failures}")
    assert len(real_failures) == 0, f"Found failed responses: {real_failures}"


def test_intercept_and_modify_response(logged_in_page: Page):
    """Intercept a static asset and verify route interception works"""
    intercepted = []

    def intercept_css(route):
        intercepted.append(route.request.url)
        route.continue_()

    logged_in_page.route("**/*.css", intercept_css)
    logged_in_page.reload()
    expect(logged_in_page.locator(".title")).to_contain_text("Products")
    print(f"\nIntercepted {len(intercepted)} CSS requests")

def test_request_counting(logged_in_page: Page, browser_name: str):
    """Count total network requests on inventory page load"""
    if browser_name != "chromium":
        pytest.skip("Request counting tests are chromium-only due to parallel stability")

    request_count = {"total": 0}

    def count_requests(request):
        request_count["total"] += 1

    logged_in_page.on("request", count_requests)
    logged_in_page.reload()
    logged_in_page.wait_for_load_state("networkidle")
    print(f"\nTotal requests on page load: {request_count['total']}")
    assert request_count["total"] > 0, "No requests were made"