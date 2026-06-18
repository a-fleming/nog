from playwright.sync_api import Error, sync_playwright

from nog.auth.session import extract_aoc_session_record, SessionRecord, save_session_record

LOGIN_URL = "https://adventofcode.com/2025/auth/login"
REDIRECT_URL = "https://adventofcode.com/2025"


class BrowserLoginError(Exception):
    pass

class LoginCancelled(Exception):
    pass

def playwright_assisted_login() -> SessionRecord | None:
    try:
        with sync_playwright() as playwright:
            with playwright.chromium.launch(headless=False, timeout=0) as browser:
                page = browser.new_page()
                page.goto(LOGIN_URL)

                # Wait for redirect back to the Advent of Code site
                page.wait_for_url(REDIRECT_URL, timeout=0)
                if "adventofcode.com" in page.url:
                    cookies = page.context.cookies()
                    session_record = extract_aoc_session_record(cookies, source="browser-login")
                    return session_record
        return None
    except Error as err:
        if "browser has been closed" in str(err).lower():
            raise LoginCancelled from err
        else:
            raise BrowserLoginError from err    

def main():
    input("Press Enter to open the browser...")
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

if __name__ == "__main__":
    main()