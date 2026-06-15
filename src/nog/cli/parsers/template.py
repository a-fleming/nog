import argparse

from typing import TypeAlias

from nog.cli.commands.template import cmd_template_test

SubparserGroup: TypeAlias = argparse._SubParsersAction


def add_template_command(command_parsers: SubparserGroup) -> None:
    template_parser = command_parsers.add_parser(
        "template",
        help="This is a template for creating a subparser command",
    )

    template_subcommands = template_parser.add_subparsers(dest="subcommand", required=True)

    template_test = template_subcommands.add_parser(
        "test",
        help="A test subcommand",
    )
    template_test.add_argument(
        "value",
        type=int,
        help="A test value"
    )
    template_test.set_defaults(func=cmd_template_test, parser=template_test)
    