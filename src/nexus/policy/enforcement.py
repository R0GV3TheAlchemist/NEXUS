from typing import Any, Dict, List

from .schema import PolicySchema, normalize_policy


def evaluate_guards(policy: PolicySchema, context: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    for guard in policy.guards:
        if guard == "source_verified" and not context.get("source_verified", False):
            failures.append(guard)
        elif guard == "schema_valid" and not context.get("schema_valid", False):
            failures.append(guard)
        elif guard == "state_ready" and not context.get("state_ready", False):
            failures.append(guard)
    return failures


def enforce_policy(raw_policy: Dict[str, Any], principal: Dict[str, Any], action: str, context: Dict[str, Any]) -> Dict[str, Any]:
    policy = normalize_policy(raw_policy)
    allowed = action in policy.allow and action not in policy.deny
    role_ok = policy.role is None or principal.get("role") == policy.role
    guard_failures = evaluate_guards(policy, context)
    decision = allowed and role_ok and not guard_failures
    return {
        "decision": decision,
        "policy": policy.to_dict(),
        "guard_failures": guard_failures,
        "allowed": allowed,
        "role_ok": role_ok,
    }
