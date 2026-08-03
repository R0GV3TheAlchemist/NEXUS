from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class AAAResult:
    authenticated: bool
    authorized: bool
    accounted: bool
    reason: str = ""


def authenticate(principal: Dict[str, Any]) -> bool:
    return bool(principal.get("id")) and bool(principal.get("secret"))


def authorize(principal: Dict[str, Any], action: str, resource: Dict[str, Any], policy: Dict[str, Any] | None = None) -> bool:
    policy = policy or {}
    allowed_actions = policy.get("allow", [])
    if action not in allowed_actions:
        return False
    required_role = policy.get("role")
    if required_role and principal.get("role") != required_role:
        return False
    return True


def account(actor: Dict[str, Any], action: str, outcome: str, reason: str = "") -> Dict[str, Any]:
    return {
        "actor": actor.get("id"),
        "action": action,
        "outcome": outcome,
        "reason": reason,
        "signature": f"{actor.get('id')}::{action}::{outcome}",
    }


def decide(principal: Dict[str, Any], action: str, resource: Dict[str, Any], policy: Dict[str, Any] | None = None) -> AAAResult:
    authed = authenticate(principal)
    if not authed:
        return AAAResult(False, False, False, "authentication_failed")
    allowed = authorize(principal, action, resource, policy)
    if not allowed:
        return AAAResult(True, False, False, "authorization_failed")
    return AAAResult(True, True, True, "allowed")
