import pytest

from nog.cli.main import main, build_parser
from nog.cli.commands.template import cmd_template_test


def test_template_test_calls_handler(capsys):
    exit_code = main(["template", "test", "123"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "cmd_template_test()\nargs.value: 123\n"

def test_template_test_errors_when_missing_args():
    parser = build_parser()

    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["template"])

    assert exc_info.value.code == 2

def test_template_test_parses():
    parser = build_parser()
    args = parser.parse_args(["template", "test", "123"])

    assert args.value == 123
    assert args.handler is cmd_template_test
