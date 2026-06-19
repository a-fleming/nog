from argparse import Namespace

from nog.auth.browser_login import (
    BrowserLoginError,
    LoginCancelled,
    playwright_assisted_login,
    SessionCookieNotFound,
)
from nog.auth.session import save_session_record


def cmd_auth_login(args: Namespace) -> None:
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
