import argparse
import json

from nexus.app.runner import run_ability


def parse_args():
    parser = argparse.ArgumentParser(description="Run a single NEXUS ability through the pipeline")
    parser.add_argument("--principal", required=True, help="JSON principal object")
    parser.add_argument("--ability", required=True, help="JSON ability payload")
    parser.add_argument("--policy", required=False, default="{}", help="JSON policy object")
    return parser.parse_args()


def main():
    args = parse_args()
    principal = json.loads(args.principal)
    ability = json.loads(args.ability)
    policy = json.loads(args.policy)
    result = run_ability(principal, ability, policy)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
