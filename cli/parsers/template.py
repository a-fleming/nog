import argparse

from typing import TypeAlias

from cli.commands.template import cmd_template_test

SubparserGroup: TypeAlias = argparse._SubParsersAction


def add_template_area(area_parsers: SubparserGroup) -> None:
    template_parser = area_parsers.add_parser(
        "template",
        help="This is a template for creating a subparser area",
    )

    template_actions = template_parser.add_subparsers(dest="action", required=True)

    template_test = template_actions.add_parser(
        "test",
        help="A test action",
    )
    template_test.add_argument(
        "value",
        type=int,
        help="A test value"
    )
    template_test.set_defaults(func=cmd_template_test, parser=template_test)
    