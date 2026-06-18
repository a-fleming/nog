from playwright.sync_api import sync_playwright

from nog.auth.session import extract_aoc_session_record, SessionRecord, save_session_record

LOGIN_URL = "https://adventofcode.com/2025/auth/login"
REDIRECT_URL = "https://adventofcode.com/2025"


def playwright_assisted_login() -> SessionRecord | None:
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
        

def main():
    input("Press Enter to open the browser...")
    session_record = playwright_assisted_login()
    if session_record:
        print(f"Successfully extracted Advent of Code session record")
        save_session_record(session_record)
    else:
        print("Unable to extract Advent of Code session record")

if __name__ == "__main__":
    main()