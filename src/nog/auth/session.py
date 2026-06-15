import json

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from platformdirs import user_data_dir
from playwright.sync_api import Page
from typing import Self

APP_NAME = "nog"
ENCODING = "utf-8"

SESSION_RECORD_PATH = Path(user_data_dir(APP_NAME)) / "auth" / "session_record.json"


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

def extract_aoc_session_record(page: Page, source:str) -> SessionRecord | None:
    """Extract the Advent of Code session cookie from the browser page and convert to a SessionRecord."""
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

def load_session_record() -> SessionRecord | None:
    if not SESSION_RECORD_PATH.is_file():
        return None
    data = json.loads(SESSION_RECORD_PATH.read_text(encoding=ENCODING))
    return SessionRecord.from_dict(data)

def save_session_record(record: SessionRecord) -> None:
    SESSION_RECORD_PATH.parent.mkdir(parents=True, exist_ok=True)
    SESSION_RECORD_PATH.write_text(json.dumps(record.to_dict(), indent=4), encoding=ENCODING)
    print(f"Saved new session record to '{str(SESSION_RECORD_PATH)}'")
