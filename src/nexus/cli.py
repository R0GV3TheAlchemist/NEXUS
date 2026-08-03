import argparse
import json
from pathlib import Path


def build_parser():
    parser = argparse.ArgumentParser(prog="nexus", description="NEXUS command-line interface")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a single ability through the pipeline")
    run_parser.add_argument("--principal", required=True, help="JSON principal object")
    run_parser.add_argument("--ability", required=True, help="JSON ability payload")
    run_parser.add_argument("--policy", default="{}", help="JSON policy object")

    bootstrap_parser = subparsers.add_parser("bootstrap", help="Create package skeleton files")
    bootstrap_parser.add_argument("--root", default=".", help="Project root")

    validate_parser = subparsers.add_parser("validate", help="Validate JSON inputs without running the pipeline")
    validate_parser.add_argument("--principal", required=True, help="JSON principal object")
    validate_parser.add_argument("--ability", required=True, help="JSON ability payload")
    validate_parser.add_argument("--policy", default="{}", help="JSON policy object")

    return parser


def handle_bootstrap(root: str):
    base = Path(root)
    files = [
        base / "src/nexus/__init__.py",
        base / "src/nexus/app/__init__.py",
        base / "src/nexus/core/__init__.py",
        base / "src/nexus/core/policy/__init__.py",
        base / "src/nexus/core/policy/aaa.py",
        base / "src/nexus/policy/__init__.py",
        base / "src/nexus/policy/aaa.py",
        base / "src/nexus/accounting/__init__.py",
        base / "src/nexus/sim/__init__.py",
        base / "src/nexus/domains/__init__.py",
    ]
    created = []
    for path in files:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.touch()
            created.append(str(path))
    return {"created": created, "checked": [str(p) for p in files]}


def run_command(principal_json: str, ability_json: str, policy_json: str):
    from nexus.app.runner import run_ability

    principal = json.loads(principal_json)
    ability = json.loads(ability_json)
    policy = json.loads(policy_json)
    return run_ability(principal, ability, policy)


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        result = run_command(args.principal, args.ability, args.policy)
        print(json.dumps(result, indent=2))
        return 0

    if args.command == "bootstrap":
        print(json.dumps(handle_bootstrap(args.root), indent=2))
        return 0

    if args.command == "validate":
        json.loads(args.principal)
        json.loads(args.ability)
        json.loads(args.policy)
        print(json.dumps({"valid": True}, indent=2))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
