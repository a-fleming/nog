from datetime import datetime, timezone
from unittest.mock import Mock

import pytest
import requests

from nog.aoc.client import fetch_input, input_url
from nog.aoc.errors import (
    AoCClientResponseError,
    AoCError,
    AoCServerResponseError,
    NetworkError,
    NotLoggedInError,
    UnexpectedResponseError,
)
from nog.auth.session import SessionRecord


def test_input_url():
    year = 2015
    day = 1
    expected = f"https://adventofcode.com/{year}/day/{day}/input"

    actual = input_url(year, day)

    assert expected == actual

def test_fetch_input_returns_response(monkeypatch):
    year = 2015
    day = 1
    session_record = make_session_record()

    fake_response = FakeResponse(status_code=200, text="TEXT")
    mock_get = Mock(return_value=fake_response)
    fake_user_agent = "TEST USER AGENT"
    fake_timeout = 15

    monkeypatch.setattr("nog.aoc.client.requests.get", mock_get)
    monkeypatch.setattr("nog.aoc.client.USER_AGENT", fake_user_agent)
    monkeypatch.setattr("nog.aoc.client.TIMEOUT", fake_timeout)

    actual = fetch_input(year, day, session_record)

    assert actual == "TEXT"
    mock_get.assert_called_once_with(
        "https://adventofcode.com/2015/day/1/input",
        headers={"User-Agent": fake_user_agent},
        cookies={"session": session_record.value},
        timeout=fake_timeout,
    )

@pytest.mark.parametrize("status_code", [200, 403, 404])
def test_fetch_input_raises_not_logged_in_error(monkeypatch, status_code):
    year = 2015
    day = 1
    session_record = make_session_record()
    not_logged_in_text = "Puzzle inputs differ by user.  Please log in to get your puzzle input."

    fake_response = FakeResponse(status_code=status_code, text=not_logged_in_text)
    mock_get = Mock(return_value=fake_response)

    monkeypatch.setattr("nog.aoc.client.requests.get", mock_get)

    with pytest.raises(NotLoggedInError):
        fetch_input(year, day, session_record)

@pytest.mark.parametrize(
        "raised_error",
        [
            requests.ConnectionError("connection failed"),
            requests.Timeout("request timed out"),
        ]
    )
def test_fetch_input_raises_network_error(monkeypatch, raised_error):
    mock_get = Mock(side_effect=raised_error)
    
    monkeypatch.setattr("nog.aoc.client.requests.get", mock_get)

    with pytest.raises(NetworkError) as exc_info:
        fetch_input(2015, 1, make_session_record())
    
    assert exc_info.value.__cause__ is raised_error

def test_fetch_input_raises_aoc_error_on_request_failure(monkeypatch):
    mock_get = Mock(side_effect=requests.RequestException)
    
    monkeypatch.setattr("nog.aoc.client.requests.get", mock_get)

    with pytest.raises(AoCError) as exc_info:
        fetch_input(2015, 1, make_session_record())

    assert type(exc_info.value) is AoCError

@pytest.mark.parametrize("status_code", [400, 404, 429, 499])
def test_fetch_input_raises_aoc_client_response_error(monkeypatch, status_code):
    fake_response = FakeResponse(status_code=status_code, text="TEXT")
    mock_get = Mock(return_value=fake_response)

    monkeypatch.setattr("nog.aoc.client.requests.get", mock_get)

    with pytest.raises(AoCClientResponseError):
        fetch_input(2015, 1, make_session_record())

@pytest.mark.parametrize("status_code", [500, 503, 599])
def test_fetch_input_raises_aoc_server_response_error(monkeypatch, status_code):
    fake_response = FakeResponse(status_code=status_code, text="TEXT")
    mock_get = Mock(return_value=fake_response)

    monkeypatch.setattr("nog.aoc.client.requests.get", mock_get)

    with pytest.raises(AoCServerResponseError):
        fetch_input(2015, 1, make_session_record())

@pytest.mark.parametrize("status_code", [199, 201, 399])
def test_fetch_input_raises_unexpected_response_error(monkeypatch, status_code):
    year = 2015
    day = 1
    session_record = make_session_record()

    fake_response = FakeResponse(status_code=status_code, text="TEXT")
    mock_get = Mock(return_value=fake_response)

    monkeypatch.setattr("nog.aoc.client.requests.get", mock_get)

    with pytest.raises(UnexpectedResponseError):
        fetch_input(year, day, session_record)

class FakeResponse:
    def __init__(self, status_code, text) -> None:
        self.status_code = status_code
        self.text = text

def make_session_record() -> SessionRecord:
    return SessionRecord(
        value="fake-session",
        created_at=datetime(2026, 6, 18, 12, 0, tzinfo=timezone.utc),
        expires=1900000000.0,
        source="test",
    )
