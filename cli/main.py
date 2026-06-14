import argparse

from cli.parsers.template import add_template_area

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nog",
        description="nog: a small Advent of Code helper CLI for managing puzzle workflows from the terminal",
    )

    area_parsers = parser.add_subparsers(
        dest="area",
        required=True,
    )

    add_template_area(area_parsers)

    return parser

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())