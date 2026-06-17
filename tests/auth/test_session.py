import pytest

from datetime import datetime, timezone

from nog.auth.session import (
    extract_aoc_session_record,
    load_session_record,
    save_session_record,
    SessionRecord,
)

AOC_DOMAIN = ".adventofcode.com"
FAKE_DOMAIN = "fake-website.com"
FAKE_EXPIRES = 1900000000.0
FAKE_EXTRA_COOKIE_DATA = "important cookie stuff"
FAKE_SESSION_VALUE = "fake-session"
FAKE_SOURCE = "test"


def test_extract_aoc_session_record():
    fake_aoc_cookie = make_cookie()
    fake_website_cookie = make_cookie(domain=FAKE_DOMAIN)
    cookies = [fake_aoc_cookie, fake_website_cookie]

    record = extract_aoc_session_record(cookies, FAKE_SOURCE)

    assert isinstance(record, SessionRecord)
    assert record.value == FAKE_SESSION_VALUE
    assert record.expires == FAKE_EXPIRES
    assert record.source == FAKE_SOURCE
    assert isinstance(record.created_at, datetime)
    assert record.created_at.tzinfo is not None
    assert not hasattr(record, "extra_data")

def test_extract_aoc_session_record_returns_none_when_cookie_missing(): 
    cookies = []

    record = extract_aoc_session_record(cookies, FAKE_SOURCE)

    assert record is None

def test_extract_aoc_session_record_returns_none_when_name_not_session():
    fake_aoc_non_session_cookie =make_cookie(name="not session") 
    cookies = [fake_aoc_non_session_cookie]

    record = extract_aoc_session_record(cookies, FAKE_SOURCE)

    assert record is None

def test_extract_aoc_session_record_returns_none_when_value_empty():
    fake_aoc_cookie = make_cookie(value="")
    cookies = [fake_aoc_cookie]

    record = extract_aoc_session_record(cookies, FAKE_SOURCE)

    assert record is None

def test_extract_aoc_session_record_returns_none_when_value_missing():
    fake_aoc_cookie = make_cookie()
    fake_aoc_cookie.pop("value")
    cookies = [fake_aoc_cookie]

    record = extract_aoc_session_record(cookies, FAKE_SOURCE)

    assert record is None

def test_load_session_record_returns_none_when_file_missing(tmp_path):
    record_path = tmp_path / "session_record.json"

    loaded_record = load_session_record(record_path)

    assert loaded_record is None

def test_save_and_load_session_record_round_trip(tmp_path):
    record_path = tmp_path / "session_record.json"
    record = SessionRecord(
        value="fake-session",
        created_at=datetime(2026, 6, 16, 12, 0, tzinfo=timezone.utc),
        expires=1900000000.0,
        source="manual",
    )

    save_session_record(record, record_path)
    loaded_record = load_session_record(record_path)

    assert loaded_record == record

def make_cookie(
        *,
        value: str = FAKE_SESSION_VALUE,
        domain: str = AOC_DOMAIN,
        name: str = "session",
        expires: float = FAKE_EXPIRES,
        extra_data: str = FAKE_EXTRA_COOKIE_DATA,
) -> dict[str, object]:
    """Create a fresh fake cookie mapping for session extraction tests."""
    return {
        "value": value,
        "domain": domain,
        "name": name,
        "expires": expires,
        "extra_data": extra_data,
    }
