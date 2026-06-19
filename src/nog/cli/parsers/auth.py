import argparse

from typing import TypeAlias

SubparserGroup: TypeAlias = argparse._SubParsersAction


def add_auth_command(command_parsers: SubparserGroup) -> None:
    auth_parser = command_parsers.add_parser(
        "auth",
        help="Manage Advent of Code authentication",
        description="Manage Advent of Code authentication for nog."
    )

    auth_subcommands = auth_parser.add_subparsers(dest="subcommand", required=True)
    