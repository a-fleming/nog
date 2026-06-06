import json
import os

from dotenv import load_dotenv
from pathlib import Path

COOKIE_PATH = Path("cookies.json")
ENCODING = "utf-8"

def load_cookies() -> list[dict]:
    if not COOKIE_PATH.is_file():
        return []
    return json.loads(COOKIE_PATH.read_text(encoding=ENCODING))


def load_credentials() -> tuple[str, str]:
    load_dotenv()
    github_username = os.environ.get("GITHUB_USERNAME")
    if not github_username:
        raise RuntimeError("GITHUB_USERNAME environment variable not set")
    github_password = os.environ.get("GITHUB_PASSWORD")
    if not github_password:
        raise RuntimeError("GITHUB_PASSWORD environment variable not set")
    return github_username, github_password

def main():
    cookies = load_cookies()
    if cookies:
        print("Found cookies:")
        print(cookies)
    else:
        print("No cookies found")

if __name__ == "__main__":
    main()
