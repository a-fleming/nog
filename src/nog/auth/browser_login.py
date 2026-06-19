from playwright.sync_api import Error, sync_playwright
from time import monotonic
from urllib.parse import urlparse

from nog.auth.session import extract_aoc_session_record, SessionRecord

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
