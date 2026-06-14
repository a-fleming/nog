from argparse import Namespace

def cmd_template_test(args: Namespace) -> None:
    print("cmd_template_test()")
    print(f"args.value: {args.value}")
