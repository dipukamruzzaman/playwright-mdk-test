# Playwright MDK Tests 🎭

![CI](https://github.com/dipukamruzzaman/playwright-mdk-test/actions/workflows/playwright.yml/badge.svg) 🎭

An end-to-end test automation framework built with **Python + Playwright**,
implementing industry best practices including Page Object Model,
cross-browser testing, API mocking, and Allure reporting.

## 🚀 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Core language |
| Playwright | Browser automation |
| pytest | Test runner |
| Allure | Test reporting |
| GitHub Actions | CI/CD pipeline |
| Page Object Model | Design pattern |

## 📊 Test Coverage

| Module | Tests | Description |
|--------|-------|-------------|
| Authentication | 5 | Login, logout, session handling |
| Products | 6 | Inventory, sorting, cart actions |
| Checkout | 6 | Full e2e checkout flow |
| Auth | 7 | Session state, multi-user scenarios |
| API Mocking | 7 | Network interception, request monitoring |
| POM | 7 | Page Object Model implementation |
| **Total** | **38** | **Cross-browser on Chrome, Firefox, WebKit** |

## 🏗️ Project Structure
```
playwright-banking-tests/
├── pages/                    # Page Object Model classes
│   ├── base_page.py          # Base class with common methods
│   ├── login_page.py         # Login page interactions
│   ├── inventory_page.py     # Products page interactions
│   ├── cart_page.py          # Cart page interactions
│   └── checkout_page.py      # Checkout page interactions
├── tests/                    # Test suites
│   ├── test_login.py         # Authentication tests
│   ├── test_products.py      # Product and cart tests
│   ├── test_checkout.py      # Checkout flow tests
│   ├── test_auth.py          # Session and auth state tests
│   ├── test_api_mocking.py   # Network interception tests
│   └── test_pom.py           # POM implementation tests
├── auth/                     # Auth state management
├── conftest.py               # pytest fixtures
├── pytest.ini                # pytest configuration
└── requirements.txt          # Dependencies
```

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation
```bash
# Clone the repository
git clone https://github.com/YourUsername/playwright-banking-tests.git
cd playwright-banking-tests

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Install browsers
python -m playwright install
```

### Running Tests
```bash
# Run full suite on Chromium
pytest tests/ -v

# Run cross-browser parallel suite
pytest tests/ --browser chromium --browser firefox --browser webkit -n auto -v

# Run specific test file
pytest tests/test_checkout.py -v

# Run with Allure report
pytest tests/ -v
allure serve allure-results

# Run headed (visible browser)
pytest tests/ -v --headed
```

## 🎯 Key Features

**Page Object Model** — All page interactions encapsulated in
dedicated page classes. Locator changes require updates in one place only.

**Smart Fixtures** — Chained pytest fixtures (`logged_in_page` →
`cart_page` → `checkout_page`) eliminate setup duplication across 38 tests.

**API Mocking** — Network request interception using `page.route()`
to test edge cases independent of backend state.

**Cross-browser** — Full test suite runs on Chrome, Firefox and
WebKit simultaneously using pytest-xdist parallel execution.

**Allure Reporting** — Tests tagged with feature, story and severity
metadata generating rich HTML reports.

**Trace Viewer** — Automatic trace capture on test failure for
post-mortem debugging.

## 📈 Test Results
```
38 tests | 3 browsers | ~70 seconds parallel execution
✅ Authentication flows
✅ Full checkout journey  
✅ API mocking & network monitoring
✅ Session & cookie handling
✅ Cross-browser compatibility
```

## 🔍 Design Decisions

**Why Playwright over Selenium?**
Auto-wait eliminates flaky tests. Built-in trace viewer accelerates
debugging. Native API mocking without additional tools.

**Why Page Object Model?**
Single source of truth for locators. Tests read like user stories.
Maintenance cost drops significantly when UI changes.

**Why pytest-xdist for parallel execution?**
Reduces 3-browser suite from 3× sequential time to near 1× by
utilizing all CPU cores simultaneously.

## 📝 Resume Bullet Points

- Built end-to-end test automation framework using Python + Playwright
covering authentication, checkout, and API mocking for a web application
- Implemented Page Object Model design pattern with 38 tests running
cross-browser (Chrome, Firefox, WebKit) via pytest with parallel execution
- Configured Allure reporting with feature/story categorisation and
severity levels for clear test result communication
- Reduced cross-browser test execution time by ~65% using pytest-xdist
parallel execution across 3 browser engines

## 👤 Author

Your Name — [LinkedIn](www.linkedin.com/in/md-kamruzzaman-54507149) |
[GitHub](https://github.com/dipukamruzzaman)