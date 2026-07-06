import argparse

from typing import TypeAlias

from nog.cli.commands.auth import cmd_auth_login

SubparserGroup: TypeAlias = argparse._SubParsersAction


def add_auth_command(command_parsers: SubparserGroup) -> None:
    auth_parser = command_parsers.add_parser(
        "auth",
        help="Manage Advent of Code authentication",
        description="Manage Advent of Code authentication for nog.",
    )

    auth_subcommands = auth_parser.add_subparsers(dest="subcommand", required=True)

    auth_login = auth_subcommands.add_parser(
        "login",
        help="Log in to Advent of Code using a browser.",
        description=(
            "Open a browser for Advent of Code login, extract the session cookie, "
            "and save it locally for future nog commands."
        )
    )
    auth_login.add_argument(
        "--dev",
        action="store_true",
        help=(
            "Use the development-only automated GitHub login flow. "
            "Requires configured dev credentials."
        ),
    )
    auth_login.set_defaults(handler=cmd_auth_login, parser=auth_login)
    