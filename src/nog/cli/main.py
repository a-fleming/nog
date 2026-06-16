import argparse

from nog.cli.parsers.template import add_template_command

def build_parser() -> argparse.ArgumentParser:
    """Build the top-level parser for the nog CLI."""
    parser = argparse.ArgumentParser(
        prog="nog",
        description="nog: a small Advent of Code helper CLI for managing puzzle workflows from the terminal",
    )

    # Top-level command groups will map to workflows like auth, new, run, and submit.
    command_parsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    add_template_command(command_parsers)

    return parser

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.handler(args)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())