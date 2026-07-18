import requests

from nog.aoc.errors import (
    AoCError,
    AoCClientResponseError,
    AoCServerResponseError,
    NetworkError,
    NotLoggedInError,
    UnexpectedResponseError,
)
from nog.auth.session import SessionRecord
from nog._version import __version__

BASE_URL = "https://adventofcode.com"
DOMAIN = ".adventofcode.com"
TIMEOUT = 10  # seconds
USER_AGENT = f"nog/{__version__}  (+https://github.com/a-fleming/nog)"


def fetch_input(year: int, day: int, session_record: SessionRecord) -> str:
    url = input_url(year, day) 
    headers = {
        "User-Agent": USER_AGENT,
    }
    cookies = {
        "session": session_record.value
    }
    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=TIMEOUT)
    except requests.ConnectionError as err:
        raise NetworkError("Could not connect to Advent of Code.") from err
    except requests.Timeout as err:
        raise NetworkError("The request to Advent of Code timed out.") from err
    except requests.RequestException as err:
        raise AoCError("The Advent of Code request failed.") from err

    if "Please log in" in response.text:
        raise NotLoggedInError
    
    if response.status_code == 200:
        return response.text

    if response.status_code >= 400 and response.status_code < 500:
        raise AoCClientResponseError(f"Advent of Code returned HTTP {response.status_code}.")
    
    if response.status_code >= 500:
        raise AoCServerResponseError(f"Advent of Code returned HTTP {response.status_code}.")
    
    raise UnexpectedResponseError(
        "Unexpected response from Advent of Code: "
        f"HTTP {response.status_code}."
    )

def input_url(year: int, day: int) -> str:
    return f"{BASE_URL}/{year}/day/{day}/input"
