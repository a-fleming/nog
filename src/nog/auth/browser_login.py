from playwright.sync_api import Error, sync_playwright
from time import monotonic
from urllib.parse import urlparse

from nog.auth.session import extract_aoc_session_record, SessionRecord, save_session_record

AOC_HOST = "adventofcode.com"
COOKIE_GRACE_SECONDS = 2.0
LOGIN_URL = "https://adventofcode.com/2025/auth/login"
LOGIN_SOURCE = "browser-login"
REDIRECT_URL = "https://adventofcode.com/2025"


class BrowserLoginError(Exception):
    pass

class LoginCancelled(Exception):
    pass

class SessionCookieNotFound(Exception):
    pass

def is_aoc_url(url: str) -> bool:
    return urlparse(url).hostname == AOC_HOST

def playwright_assisted_login() -> SessionRecord | None:
    try:
        with sync_playwright() as playwright:
            with playwright.chromium.launch(headless=False, timeout=0) as browser:
                page = browser.new_page()
                page.goto(LOGIN_URL)

                has_left_aoc_site = False
                returned_to_aoc_at: float | None = None

                while True:
                    current_url = page.url
                    on_aoc_site = is_aoc_url(current_url)
                    cookies = page.context.cookies()
                    session_record = extract_aoc_session_record(cookies, LOGIN_SOURCE)

                    if session_record is not None:
                        return session_record
                    
                    if not on_aoc_site:
                        has_left_aoc_site = True
                        returned_to_aoc_at = None
                    
                    if has_left_aoc_site and on_aoc_site:
                        if returned_to_aoc_at is None:
                            returned_to_aoc_at = monotonic()
                        
                        if monotonic() - returned_to_aoc_at >= COOKIE_GRACE_SECONDS:
                            raise SessionCookieNotFound

                    page.wait_for_timeout(500)
    except SessionCookieNotFound:
        raise
    except Error as err:
        if "browser has been closed" in str(err).lower():
            raise LoginCancelled from err
        else:
            raise BrowserLoginError from err    

def main():
    print()
    print("nog will open a browser window for Advent of Code login.")
    print("Log in using your preferred Advent of Code login method.")
    print("After login succeeds, nog will extract your Advent of Code session and close the browser.")
    print("Closing the browser will cancel login.")
    print()

    input("Press Enter to open the browser...")
    print("Waiting for Advent of Code login to complete...")
    try:
        session_record = playwright_assisted_login()
        if session_record:
            print(f"Successfully extracted Advent of Code session record")
            save_session_record(session_record)
        else:
            print("Unable to extract Advent of Code session record")
    except BrowserLoginError:
        print("Browser login failed because Playwright reported an error. No session was saved.")
        print("Try running the login command again, or use manual session setup if the issue persists.")
    except LoginCancelled:
        print("Login cancelled. No session was saved.")
    except SessionCookieNotFound:
        print("Browser login returned to Advent of Code, but no session cookie was found.")
        print("Try running the login command again, or use manual session setup if the issue persists.")

if __name__ == "__main__":
    main()