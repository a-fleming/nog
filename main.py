import json
import os

from dataclasses import dataclass
from datetime import datetime, timezone
from dotenv import load_dotenv
from pathlib import Path
from playwright.sync_api import Page, Playwright, sync_playwright
from typing import Self

SESSION_COOKIE_PATH = Path("session_cookie.json")
ENCODING = "utf-8"
LOGIN_URL = "https://adventofcode.com/2025/auth/login"
REDIRECT_URL = "https://adventofcode.com/2025"


@dataclass
class SessionRecord:
    value: str
    expires: float | None = None
    created_at: datetime | None = None
    source: str = "unknown"

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            value=data["value"],
            expires=data.get("expires"),
            created_at=datetime.fromisoformat(data.get("created_at")),
            source=data["source"],
        )
    
    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "expires": self.expires,
            "created_at": self.created_at.isoformat(),
            "source": self.source,
        }

def get_session_cookie(page: Page, source:str) -> SessionRecord | None:
    all_cookies = page.context.cookies()
    for cookie in all_cookies:
        if "adventofcode.com" in cookie.get("domain", "") and cookie.get("name") == "session":
            return SessionRecord(
                value=cookie.get("value"),
                expires=cookie.get("expires"),
                created_at=datetime.now(timezone.utc),
                source=source,
            )
    return None

def github_login_automation(playwright: Playwright) -> SessionRecord:
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

    session_cookie = get_session_cookie(page, "playwright-dev")
    browser.close()
    return session_cookie

def load_session_cookie() -> SessionRecord:
    if not SESSION_COOKIE_PATH.is_file():
        return []
    data = json.loads(SESSION_COOKIE_PATH.read_text(encoding=ENCODING))
    return SessionRecord.from_dict(data)

def load_credentials() -> tuple[str, str]:
    load_dotenv()
    github_username = os.environ.get("GITHUB_USERNAME")
    if not github_username:
        raise RuntimeError("GITHUB_USERNAME environment variable not set")
    github_password = os.environ.get("GITHUB_PASSWORD")
    if not github_password:
        raise RuntimeError("GITHUB_PASSWORD environment variable not set")
    return github_username, github_password

def save_session_cookie(cookie: SessionRecord) -> None:
    SESSION_COOKIE_PATH.write_text(json.dumps(cookie.to_dict(), indent=4), encoding=ENCODING)
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
