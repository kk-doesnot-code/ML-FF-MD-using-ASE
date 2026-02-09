from __future__ import annotations

import argparse
import sys
import yaml

from mof_ase_md.config.loader import load_config
from mof_ase_md.config.defaults import apply_defaults
from mof_ase_md.config.validator import validate_config, ConfigError
from mof_ase_md.md.methods import list_methods
from mof_ase_md.run import run as run_md


def cmd_run(args: argparse.Namespace) -> int:
    run_md(args.config)
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    cfg = load_config(args.config)
    cfg = apply_defaults(cfg)
    validate_config(cfg)
    print("CONFIG VALID")
    return 0


def cmd_list_methods(args: argparse.Namespace) -> int:
    methods = list_methods()
    print("\n".join(methods))
    return 0


def cmd_print_config(args: argparse.Namespace) -> int:
    cfg = load_config(args.config)
    cfg = apply_defaults(cfg)
    cfg = validate_config(cfg)
    yaml.safe_dump(cfg, stream=sys.stdout, sort_keys=False)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mof_ase_md",
        description="MOF MD runner using ASE + ML force fields",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser("run", help="Run MD from a config file")
    p_run.add_argument("config", help="Path to YAML config file")
    p_run.set_defaults(func=cmd_run)

    p_val = sub.add_parser("validate", help="Validate config (after applying defaults)")
    p_val.add_argument("config", help="Path to YAML config file")
    p_val.set_defaults(func=cmd_validate)

    p_list = sub.add_parser("list-methods", help="List available md.method names")
    p_list.set_defaults(func=cmd_list_methods)

    p_print = sub.add_parser("print-config", help="Print resolved config    (defaults applied)")
    p_print.add_argument("config", help="Path to YAML config file")
    p_print.set_defaults(func=cmd_print_config)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        rc = args.func(args)
        raise SystemExit(rc)
    except ConfigError as e:
        print(f"CONFIG ERROR: {e}", file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
