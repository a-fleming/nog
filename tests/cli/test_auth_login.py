from datetime import datetime, timezone

from nog.auth.errors import (
    BrowserLoginError, 
    DevLoginError,
    LoginCancelled,
    SessionCookieNotFound,
)
from nog.auth.session import SessionRecord
from nog.cli.main import main, build_parser
from nog.cli.commands.auth import cmd_auth_login, run_browser_login, run_dev_login


# Parser tests

def test_auth_login_parser_accepts_dev_flag():
    parser = build_parser()
    args = parser.parse_args(["auth", "login", "--dev"])

    assert args.dev is True
    assert args.handler is cmd_auth_login

def test_auth_login_parser_sets_handler():
    parser = build_parser()
    args = parser.parse_args(["auth", "login"])

    assert args.dev is False
    assert args.handler is cmd_auth_login

# Routing tests

def test_auth_login_routes_browser_login(monkeypatch):
    called = []

    def fake_browser_login():
        called.append("fake_browser_login()")

    monkeypatch.setattr("nog.cli.commands.auth.run_browser_login", fake_browser_login)
    monkeypatch.setattr("nog.cli.commands.auth.run_dev_login", fail_if_run_dev_login_called)

    exit_code = main(["auth", "login"])

    assert exit_code == 0
    assert called == ["fake_browser_login()"]

def test_auth_login_routes_dev_login(monkeypatch):
    called = []

    def fake_dev_login():
        called.append("fake_dev_login()")

    monkeypatch.setattr("nog.cli.commands.auth.run_browser_login", fail_if_run_browser_login_called)
    monkeypatch.setattr("nog.cli.commands.auth.run_dev_login", fake_dev_login)

    exit_code = main(["auth", "login", "--dev"])

    assert exit_code == 0
    assert called == ["fake_dev_login()"]

# Browser login tests

def test_browser_login_handles_browser_error(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", fake_input)
    monkeypatch.setattr("nog.cli.commands.auth.github_login_automation", fail_if_github_login_automation_called)
    monkeypatch.setattr("nog.cli.commands.auth.playwright_assisted_login", raise_browser_login_error)
    monkeypatch.setattr("nog.cli.commands.auth.save_session_record", fail_if_save_called)

    run_browser_login()
    captured = capsys.readouterr()

    assert "Browser login failed" in captured.out

def test_browser_login_handles_cancel(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", fake_input)
    monkeypatch.setattr("nog.cli.commands.auth.github_login_automation", fail_if_github_login_automation_called)
    monkeypatch.setattr("nog.cli.commands.auth.playwright_assisted_login", raise_login_cancelled)
    monkeypatch.setattr("nog.cli.commands.auth.save_session_record", fail_if_save_called)

    run_browser_login()
    captured = capsys.readouterr()

    assert "Login cancelled. No session was saved." in captured.out

def test_browser_login_handles_missing_cookie(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", fake_input)
    monkeypatch.setattr("nog.cli.commands.auth.github_login_automation", fail_if_github_login_automation_called)
    monkeypatch.setattr("nog.cli.commands.auth.playwright_assisted_login", raise_session_cookie_not_found)
    monkeypatch.setattr("nog.cli.commands.auth.save_session_record", fail_if_save_called)

    run_browser_login()
    captured = capsys.readouterr()

    assert "returned to Advent of Code, but no session cookie" in captured.out

def test_browser_login_uses_playwright_assisted_login(capsys, monkeypatch):
    fake_record = make_session_record()
    saved = {}

    def fake_playwright_assisted_login():
        return fake_record
    
    def fake_save_session_record(record):
        saved["record"] = record
    
    monkeypatch.setattr("builtins.input", fake_input)
    monkeypatch.setattr("nog.cli.commands.auth.github_login_automation", fail_if_github_login_automation_called)
    monkeypatch.setattr("nog.cli.commands.auth.playwright_assisted_login", fake_playwright_assisted_login)
    monkeypatch.setattr("nog.cli.commands.auth.save_session_record", fake_save_session_record)

    run_browser_login()
    captured = capsys.readouterr()

    assert saved["record"] == fake_record
    assert "Successfully extracted Advent of Code session record" in captured.out

# Dev login tests

def test_dev_login_handles_dev_login_error(capsys, monkeypatch):
    monkeypatch.setattr("nog.cli.commands.auth.github_login_automation", raise_dev_login_error)
    monkeypatch.setattr("nog.cli.commands.auth.playwright_assisted_login", fail_if_playwright_assisted_login_called)
    monkeypatch.setattr("nog.cli.commands.auth.save_session_record", fail_if_save_called)

    run_dev_login()
    captured = capsys.readouterr()

    assert "GitHub automation failed" in captured.out

def test_dev_login_handles_missing_cookie(capsys, monkeypatch):
    monkeypatch.setattr("nog.cli.commands.auth.github_login_automation", raise_session_cookie_not_found)
    monkeypatch.setattr("nog.cli.commands.auth.playwright_assisted_login", fail_if_playwright_assisted_login_called)
    monkeypatch.setattr("nog.cli.commands.auth.save_session_record", fail_if_save_called)

    run_dev_login()
    captured = capsys.readouterr()

    assert "Dev login completed, but no session" in captured.out

def test_dev_login_uses_github_login_automation(capsys, monkeypatch):
    fake_record = make_session_record()
    saved = {}

    def fake_github_login_automation():
        return fake_record
    
    def fake_save_session_record(record):
        saved["record"] = record
    
    monkeypatch.setattr("nog.cli.commands.auth.github_login_automation", fake_github_login_automation)
    monkeypatch.setattr("nog.cli.commands.auth.playwright_assisted_login", fail_if_playwright_assisted_login_called)
    monkeypatch.setattr("nog.cli.commands.auth.save_session_record", fake_save_session_record)

    run_dev_login()
    captured = capsys.readouterr()

    assert saved["record"] == fake_record
    assert "Successfully extracted Advent of Code session record" in captured.out

# Test helpers

def fail_if_github_login_automation_called(*args, **kwargs):
    raise AssertionError("github_login_automation should not be called")

def fail_if_playwright_assisted_login_called(*args, **kwargs):
    raise AssertionError("playwright_assisted_login should not be called")

def fail_if_run_browser_login_called(*args, **kwargs):
    raise AssertionError("run_browser_login should not be called")

def fail_if_run_dev_login_called(*args, **kwargs):
    raise AssertionError("run_dev_login should not be called")

def fail_if_save_called(*args, **kwargs):
    raise AssertionError("save_session_record should not be called")

def fake_input(prompt: str = "") -> str:
    return ""

def make_session_record() -> SessionRecord:
    return SessionRecord(
        value="fake-session",
        created_at=datetime(2026, 6, 18, 12, 0, tzinfo=timezone.utc),
        expires=1900000000.0,
        source="test",
    )

def raise_browser_login_error():
    raise BrowserLoginError()

def raise_dev_login_error():
    raise DevLoginError()

def raise_login_cancelled():
    raise LoginCancelled()

def raise_session_cookie_not_found():
    raise SessionCookieNotFound()
