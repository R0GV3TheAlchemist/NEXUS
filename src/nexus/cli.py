"""NEXUS CLI.

Copyright (c) 2026 Kyle Alexander Steen.
"""

from __future__ import annotations

import argparse
from typing import Sequence

from .version import __author__, __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nexus")
    parser.add_argument("--version", action="version", version=f"NEXUS {__version__} by {__author__}")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="Run the NEXUS application")
    run_parser.add_argument("inputs", nargs="+", help="Inputs required to run NEXUS")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    return 0
