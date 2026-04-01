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