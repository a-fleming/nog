from nog.aoc.client import fetch_input
from nog.storage.input_cache import (
    input_exists,
    load_input,
    save_input,
)
from nog.auth.session import SessionRecord


def get_input(year: int, day: int, session_record: SessionRecord, force: bool = False) -> str:
    if not force and input_exists(year, day):
        return load_input(year, day)
    puzzle_input = fetch_input(year, day, session_record)
    save_input(year, day, puzzle_input)
    return puzzle_input
