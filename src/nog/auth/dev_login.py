import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from nog.auth.errors import DevLoginError, SessionCookieNotFound
from nog.auth.session import extract_aoc_session_record, SessionRecord

LOGIN_URL = "https://adventofcode.com/2025/auth/login"
REDIRECT_URL = "https://adventofcode.com/2025"


def github_login_automation() -> SessionRecord:
    """Development-only helper for temporary GitHub login automation."""
    github_username, github_password = load_credentials()

    try:
        # Launch a hidden browser
        with sync_playwright() as playwright:
            with playwright.chromium.launch(headless=True) as browser:
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
                    
                    # Wait until GitHub has left the login/2FA pages so the trusted-device URL can be checked reliably.
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

                cookies = page.context.cookies()
                session_record = extract_aoc_session_record(cookies, "playwright-dev")
                if session_record is None:
                    raise SessionCookieNotFound
                return session_record
    except DevLoginError:
        raise
    except Exception as err:
        raise DevLoginError from err

def load_credentials() -> tuple[str, str]:
    """Development-only helper to load GitHub credentials from .env."""
    load_dotenv()
    github_username = os.environ.get("GITHUB_USERNAME")
    if not github_username:
        raise DevLoginError("GITHUB_USERNAME environment variable not set")
    github_password = os.environ.get("GITHUB_PASSWORD")
    if not github_password:
        raise DevLoginError("GITHUB_PASSWORD environment variable not set")
    return github_username, github_password
