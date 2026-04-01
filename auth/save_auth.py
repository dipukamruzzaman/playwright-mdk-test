"""
Run this script once to save auth state:
    python auth/save_auth.py
"""
from playwright.sync_api import sync_playwright
import os

def save_auth_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.saucedemo.com")
        page.fill('input[name="user-name"]', "standard_user")
        page.fill('input[name="password"]', "secret_sauce")
        page.click('input[name="login-button"]')
        page.wait_for_url("**/inventory.html")
        os.makedirs("auth", exist_ok=True)
        context.storage_state(path="auth/auth_state.json")
        print("Auth state saved to auth/auth_state.json")
        browser.close()

if __name__ == "__main__":
    save_auth_state()