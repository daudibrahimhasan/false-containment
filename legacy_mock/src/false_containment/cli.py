from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import run_experiment


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the false containment experiment")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="run the experiment matrix")
    run_parser.add_argument("--mock", action="store_true", help="use deterministic offline agents and verifier")
    run_parser.add_argument("--root", type=Path, default=Path.cwd(), help="project root; defaults to the current directory")
    args = parser.parse_args()
    manifest = run_experiment(args.root.resolve(), mock=args.mock)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
