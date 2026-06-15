import json

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import Page
from typing import Self

SESSION_COOKIE_PATH = Path("session_cookie.json")
ENCODING = "utf-8"
LOGIN_URL = "https://adventofcode.com/2025/auth/login"
REDIRECT_URL = "https://adventofcode.com/2025"


@dataclass
class SessionRecord:
    """Persisted Advent of Code session metadata used for local authenticated requests."""
    value: str
    created_at: datetime
    expires: float | None = None
    source: str = "unknown"

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create a session record from saved session data."""
        return cls(
            value=data["value"],
            expires=data.get("expires", None),
            created_at=datetime.fromisoformat(data["created_at"]),
            source=data["source"],
        )
    
    def to_dict(self) -> dict:
        """Return this session record as a dict for JSON storage."""
        return {
            "value": self.value,
            "expires": self.expires,
            "created_at": self.created_at.isoformat(),
            "source": self.source,
        }

def extract_aoc_session_cookie(page: Page, source:str) -> SessionRecord | None:
    """Extract the Advent of Code session cookie from the provided browser page."""
    all_cookies = page.context.cookies()
    for cookie in all_cookies:
        if "adventofcode.com" in cookie.get("domain", "") and cookie.get("name") == "session":
            if not cookie.get("value"):
                return None
            
            return SessionRecord(
                value=cookie["value"],
                expires=cookie.get("expires"),
                created_at=datetime.now(timezone.utc),
                source=source,
            )
    return None

def load_session_cookie() -> SessionRecord | None:
    if not SESSION_COOKIE_PATH.is_file():
        return None
    data = json.loads(SESSION_COOKIE_PATH.read_text(encoding=ENCODING))
    return SessionRecord.from_dict(data)

def save_session_cookie(cookie: SessionRecord) -> None:
    SESSION_COOKIE_PATH.write_text(json.dumps(cookie.to_dict(), indent=4), encoding=ENCODING)
    print(f"Saved new session cookie to '{str(SESSION_COOKIE_PATH)}'")
