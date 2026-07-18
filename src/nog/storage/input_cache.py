from pathlib import Path
from platformdirs import user_data_dir

APP_NAME = "nog"
ENCODING = "utf-8"
INPUT_BASE_PATH = Path(user_data_dir(APP_NAME)) / "aoc" / "inputs"

def load_input(year: int, day: int, base_path: Path = INPUT_BASE_PATH) -> str:
    return input_path(year, day, base_path).read_text(encoding=ENCODING)

def input_exists(year: int, day: int, base_path: Path = INPUT_BASE_PATH) -> bool:
    return input_path(year, day, base_path).is_file()

def input_path(year: int, day: int, base_path: Path = INPUT_BASE_PATH) -> Path:
    return base_path / str(year) / f"day{day:02d}.txt"

def save_input(year: int, day: int, puzzle_input: str, base_path: Path = INPUT_BASE_PATH) -> None:
    save_path = input_path(year, day, base_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(puzzle_input, encoding=ENCODING)
