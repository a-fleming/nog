from nog.aoc.inputs import get_input

# Routing tests

def test_get_input_loads_existing_input(monkeypatch):
    called = []
    expected = "PUZZLE INPUT"
    
    def fake_input_exists_returns_true(year, day):
        called.append("fake_input_exists()")
        return True
    
    def fake_load_input(year, day):
        called.append("fake_load_input()")
        return expected

    monkeypatch.setattr("nog.aoc.inputs.fetch_input", fail_if_fetch_input_called)
    monkeypatch.setattr("nog.aoc.inputs.input_exists", fake_input_exists_returns_true)
    monkeypatch.setattr("nog.aoc.inputs.load_input", fake_load_input)
    monkeypatch.setattr("nog.aoc.inputs.save_input", fail_if_save_input_called)

    actual = get_input(year=2015, day=1, session_record=None)

    assert called == ["fake_input_exists()", "fake_load_input()"]
    assert actual == expected

def test_get_input_fetches_and_saves_missing_input(monkeypatch):
    called = []
    expected = "PUZZLE INPUT"

    def fake_fetch_input(year, day, session_record, force=False):
        called.append("fake_fetch_input()")
        return expected
    
    def fake_input_exists_returns_false(year, day):
        called.append("fake_input_exists()")
        return False
    
    def fake_save_input(year, day, puzzle_input):
        called.append("fake_save_input()")

    monkeypatch.setattr("nog.aoc.inputs.fetch_input", fake_fetch_input)
    monkeypatch.setattr("nog.aoc.inputs.input_exists", fake_input_exists_returns_false)
    monkeypatch.setattr("nog.aoc.inputs.load_input", fail_if_load_input_called)
    monkeypatch.setattr("nog.aoc.inputs.save_input", fake_save_input)

    actual = get_input(year=2015, day=1, session_record=None)

    assert called == ["fake_input_exists()", "fake_fetch_input()", "fake_save_input()"]
    assert actual == expected

def test_get_input_force_fetches_and_saves_input(monkeypatch):
    called = []
    expected = "PUZZLE INPUT"

    def fake_fetch_input(year, day, session_record, force=False):
        called.append("fake_fetch_input()")
        return expected
    
    def fake_save_input(year, day, puzzle_input):
        called.append("fake_save_input()")

    monkeypatch.setattr("nog.aoc.inputs.fetch_input", fake_fetch_input)
    monkeypatch.setattr("nog.aoc.inputs.input_exists", fail_if_input_exists_called)
    monkeypatch.setattr("nog.aoc.inputs.load_input", fail_if_load_input_called)
    monkeypatch.setattr("nog.aoc.inputs.save_input", fake_save_input)

    actual = get_input(year=2015, day=1, session_record=None, force=True)

    assert called == ["fake_fetch_input()", "fake_save_input()"]
    assert actual == expected

# Test helpers

def fail_if_fetch_input_called(*args, **kwargs):
    raise AssertionError("fetch_input should not be called")

def fail_if_input_exists_called(*args, **kwargs):
    raise AssertionError("input_exists should not be called")

def fail_if_load_input_called(*args, **kwargs):
    raise AssertionError("load_input should not be called")

def fail_if_save_input_called(*args, **kwargs):
    raise AssertionError("save_input should not be called")
