from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import load_cases, read_json, run, run_agent_pilot, run_class_balance_validation, run_preflight, run_secondary, run_stress, validate_design


def main() -> None:
    parser = argparse.ArgumentParser(description="FalseContain-Bench")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate")
    run_parser = commands.add_parser("run")
    run_parser.add_argument("--fixture", action="store_true")
    run_parser.add_argument("--mock", action="store_true")
    run_parser.add_argument("--dry-run", action="store_true", help="run all scientific case definitions with mock providers while the scientific lock remains closed")
    secondary_parser = commands.add_parser("secondary")
    secondary_parser.add_argument("--fixture", action="store_true")
    secondary_parser.add_argument("--mock", action="store_true")
    stress_parser = commands.add_parser("stress")
    stress_parser.add_argument("--mock", action="store_true")
    stress_parser.add_argument("--include-broad", action="store_true")
    pilot_parser = commands.add_parser("pilot", help="run the 16-call agent-only design-validation pilot")
    pilot_parser.add_argument("--mock", action="store_true")
    pilot_parser.add_argument("--force", action="store_true")
    commands.add_parser("preflight", help="check API keys and exact provider model IDs without inference")
    commands.add_parser("validate-classes", help="run the deterministic 8-fixture, 4/4 class-balance validation with no APIs")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.command == "validate":
        config = read_json(root / "config" / "experiment.json")
        cases = load_cases(root)
        errors = validate_design(cases, config, scientific=True)
        print(json.dumps({"valid": not errors, "case_count": len(cases), "errors": errors}, indent=2))
        raise SystemExit(0 if not errors else 2)
    if args.command == "run":
        result = run(root, fixture=args.fixture, mock=args.mock, dry_run=args.dry_run)
    elif args.command == "secondary":
        result = run_secondary(root, fixture=args.fixture, mock=args.mock)
    elif args.command == "stress":
        result = run_stress(root, mock=args.mock, include_broad=args.include_broad)
    elif args.command == "pilot":
        result = run_agent_pilot(root, mock=args.mock, force=args.force)
    elif args.command == "preflight":
        result = run_preflight(root)
    else:
        result = run_class_balance_validation(root)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
