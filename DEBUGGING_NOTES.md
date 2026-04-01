# Debugging Notes

## Day 7 — Auth Tests & Session Handling

### Issue 1: `authenticated_page` fixture timeout
**Symptom:** Tests using `authenticated_page` fixture hung with asyncio timeout.
**Root cause:** Python 3.14 + Playwright 1.58 compatibility issue on Windows.
**Fix:** Used `logged_in_page` fixture instead — avoids creating a new context mid-session.

### Issue 2: Hamburger menu `intercepts pointer events`
**Symptom:** `test_logout_clears_session` timed out clicking `[data-test="open-menu"]`.
**Error log clue:**
```
<button type="button" id="react-burger-menu-btn">Open Menu</button>
intercepts pointer events
```
**Root cause:** The `data-test="open-menu"` targets an `<img>` element.
The actual clickable element is the button behind it.
**Fix:** Changed locator from:
```python
logged_in_page.locator('[data-test="open-menu"]').click()
```
To:
```python
logged_in_page.locator('#react-burger-menu-btn').click()
```
**Lesson:** Always read the full error log — `intercepts pointer events`
means another element is blocking the click. Use browser DevTools
or Playwright Inspector to find the correct clickable element.

### Issue 3: `pytest.ini` was empty
**Symptom:** POM fixtures not found by pytest on Day 6.
**Root cause:** `pytest.ini` existed but had no content — caused conftest
discovery issues.
**Fix:** Added proper content to `pytest.ini`:
```ini
[pytest]
addopts = --timeout=30
testpaths = tests
```
**Lesson:** Always verify config files actually have content after creating them.
Use `type filename` in terminal to confirm.



## Day 10 — Cross-Browser & Parallel Execution

### Issue 1: Firefox worker crashes on network monitoring tests
**Symptom:** `worker 'gw6' crashed` on `test_monitor_all_network_requests[firefox]`
and `test_request_counting[firefox]` when running with `-n auto`.
**Root cause:** `page.on("request/response")` event listeners are unstable
on Firefox under parallel execution with pytest-xdist.
**Fix:** Added `browser_name: str` fixture parameter and used `pytest.skip()`
inside the test to gracefully skip non-chromium browsers:
```python
def test_monitor_all_network_requests(logged_in_page: Page, browser_name: str):
    if browser_name != "chromium":
        pytest.skip("Chromium-only due to parallel stability")
```
**Lesson:** Not all Playwright features behave identically across browsers.
Always test cross-browser early — don't assume Chromium behaviour
applies to Firefox and WebKit.

### Issue 2: Firefox PWA icon 404
**Symptom:** `test_monitor_all_network_requests[firefox]` failed with
`404 https://www.saucedemo.com/icon/icon-192x192.png`
**Root cause:** Firefox requests PWA manifest icons that Chrome ignores.
SauceDemo doesn't provide these icons.
**Fix:** Added `icon-192x192.png` to the exclusion filter:
```python
real_failures = [
    r for r in responses_log
    if r.startswith(("4", "5"))
    and "inventory.html" not in r
    and "backtrace.io" not in r
    and "icon-192x192.png" not in r
]
```
**Lesson:** Cross-browser testing reveals browser-specific behaviours.
Firefox is stricter about PWA assets than Chromium.

### Issue 3: `@pytest.mark.skip_browser` didn't work
**Symptom:** Marker was added but Firefox tests still crashed.
**Root cause:** `skip_browser` marker doesn't prevent worker crashes
in parallel mode — the test still gets assigned to a worker and crashes
before the skip logic runs.
**Fix:** Use `pytest.skip()` inside the test body instead — this is
more reliable under xdist parallel execution.
**Lesson:** Markers run at collection time, `pytest.skip()` runs at
execution time. For parallel stability, always skip inside the test body.