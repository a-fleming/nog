import os

from dotenv import load_dotenv

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
    github_username, github_password = load_credentials()
    print(f"Username: {github_username}")


if __name__ == "__main__":
    main()
