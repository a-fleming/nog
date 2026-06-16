from argparse import Namespace

def cmd_template_test(args: Namespace) -> None:
    """Temporary command handler used to verify CLI wiring."""
    print("cmd_template_test()")
    print(f"args.value: {args.value}")
