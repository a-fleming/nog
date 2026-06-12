import json
import os

from dotenv import load_dotenv
from pathlib import Path
from playwright.sync_api import Cookie, Page, Playwright, sync_playwright

SESSION_COOKIE_PATH = Path("session_cookie.json")
ENCODING = "utf-8"
LOGIN_URL = "https://adventofcode.com/2025/auth/login"
REDIRECT_URL = "https://adventofcode.com/2025"


def get_session_cookie(page: Page) -> Cookie | None:
    all_cookies = page.context.cookies()
    for cookie in all_cookies:
        if "adventofcode.com" in cookie.get("domain", "") and cookie.get("name") == "session":
            return cookie

def github_login_automation(playwright: Playwright) -> list[Cookie]:
    github_username, github_password = load_credentials()

    # Launch a hidden browser
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    # Go to the Advent of Code's login page
    print(f"Navigating to {LOGIN_URL}")
    page.goto(LOGIN_URL)

    # Click "[GitHub]"
    page.click("text=[GitHub]")
    page.wait_for_load_state("networkidle")

    # Fill in GitHub Credentials if prompted
    if "://github.com" in page.url:
        print("Filling GitHub credentials...")
        page.fill("input[name='login']", github_username)
        page.fill("input[name='password']", github_password)
        page.click("input[type='submit']")

        # Handle 2FA if it appears
        if "two-factor" in page.url:
            print("2FA detected! Please type the code")
            two_fa_code = input("> ")
            page.fill("input[id='app_totp']", two_fa_code)
        
        # Handle "Configure passwordless authentication" page if it appears
        page.wait_for_url(lambda url: "2fa" not in url and "login" not in url)
        if "trusted-device" in page.url:
            print("Detected trusted-device prompt. Dismissing it...")
            try:
                # Attempt button click
                page.click("""input[value="Don't ask again for this browser"]""")
            except Exception as e:
                print(f"Could not click dismiss button: {e}")

                print("Attempting JavaScript form submission to dismiss...")
                target_form = page.locator("form[action*='/sessions/trusted-device']").filter(has_text="Don't ask again for this browser")
                target_form.evaluate("form => form.submit()")
        else:
            print("No trusted-device prompt shown. Proceeding normally.")

    # Wait for redirect back to the target application
    page.wait_for_url(REDIRECT_URL)
    print("Successfully logged in!")

    session_cookie = get_session_cookie(page)
    browser.close()
    return session_cookie

def load_session_cookie() -> Cookie:
    if not SESSION_COOKIE_PATH.is_file():
        return []
    return Cookie(json.loads(SESSION_COOKIE_PATH.read_text(encoding=ENCODING)))

def load_credentials() -> tuple[str, str]:
    load_dotenv()
    github_username = os.environ.get("GITHUB_USERNAME")
    if not github_username:
        raise RuntimeError("GITHUB_USERNAME environment variable not set")
    github_password = os.environ.get("GITHUB_PASSWORD")
    if not github_password:
        raise RuntimeError("GITHUB_PASSWORD environment variable not set")
    return github_username, github_password

def save_session_cookie(cookie: Cookie) -> None:
    SESSION_COOKIE_PATH.write_text(json.dumps(cookie, indent=4), encoding=ENCODING)
    print(f"Saved new session cookie to '{str(SESSION_COOKIE_PATH)}'")

def main():
    with sync_playwright() as playwright:
        session_cookie = load_session_cookie()
        if session_cookie:
            print("Found session cookie")
        else:
            print("No session cookie found")
            session_cookie = github_login_automation(playwright)
            save_session_cookie(session_cookie)


if __name__ == "__main__":
    main()
