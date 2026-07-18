from nog.storage.input_cache import input_exists, load_input, save_input


def test_input_exists_existent_returns_true(tmp_path):
    input_path = tmp_path / "2015" / "day01.txt"
    input_path.parent.mkdir(parents=True, exist_ok=True)
    input_path.write_text("EXISTS")

    exists = input_exists(2015, 1, tmp_path)

    assert exists is True

def test_input_exists_returns_true_after_save(tmp_path):
    year = 2015
    day = 1
    expected = "TEST"

    exists_before_save = input_exists(year, day, tmp_path)
    save_input(year, day, expected, tmp_path)
    exists_after_save = input_exists(year, day, tmp_path)

    assert exists_before_save is False
    assert exists_after_save is True

def test_save_and_load_input_round_trip(tmp_path):
    year = 2015
    day = 1
    expected = "TEST"

    save_input(year, day, expected, tmp_path)
    actual = load_input(year, day, tmp_path)

    assert expected == actual
    assert expected is not actual
    