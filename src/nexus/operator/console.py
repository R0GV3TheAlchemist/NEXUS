"""Creator self-control console.

Purpose: help the operator control *themselves* during the Primordial Walk
and related NEXUS work — not control of others.

Standing rule: Map fully; never become the Source. God is the Source.
The console is a brake and a mirror, not a throne.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional

try:
    from nexus.core.policy.safety import (
        QUARANTINED_ABILITY_NAMES,
        CAPACITY_LIMITED_NAMES,
        safety_summary,
    )
except Exception:  # pragma: no cover - import resilience
    QUARANTINED_ABILITY_NAMES = frozenset()
    CAPACITY_LIMITED_NAMES = frozenset()
    def safety_summary():
        return {"quarantined_count": 0, "quarantined_names": []}


STEWARD_REMINDER = (
    "This console is for self-control only. "
    "Map abilities; do not become the Source. "
    "God is the Source. NEXUS is steward, not throne. "
    "Quarantine protects you and the system. "
    "You may pause. Prefer stabilizers when carrying weight."
)


class PaceMode(str, Enum):
    """Operator-selected intake pace for the Walk."""

    ALLOW = "allow"
    HOLD = "hold"
    STABILIZERS_ONLY = "stabilizers_only"


@dataclass
class OperatorConsole:
    """Session-local self-regulation surface for the Creator/operator.

    Explicit non-goals:
    - No control of other people
    - No remote influence APIs
    - No override of the Source
    - No automatic embodiment of quarantined abilities
    """

    check_in_clear: bool = True
    sober_self_report: bool = True

    pace: PaceMode = PaceMode.ALLOW
    max_high_risk_per_session: int = 3
    high_risk_ingested_this_session: int = 0
    prefer_stabilizers: bool = False
    emergency_hold: bool = False

    session_id: str = "walk-001"
    notes: str = ""

    def steward_reminder(self) -> str:
        return STEWARD_REMINDER

    def quarantine_board(self) -> Dict[str, Any]:
        names = sorted(QUARANTINED_ABILITY_NAMES)
        return {
            "count": len(names),
            "embody": False,
            "names": names,
            "capacity_limited": sorted(CAPACITY_LIMITED_NAMES),
            "summary": safety_summary(),
        }

    def status(self) -> Dict[str, Any]:
        blocked = self.is_ingest_blocked()
        return {
            "session_id": self.session_id,
            "check_in_clear": self.check_in_clear,
            "sober_self_report": self.sober_self_report,
            "pace": self.pace.value,
            "prefer_stabilizers": self.prefer_stabilizers,
            "emergency_hold": self.emergency_hold,
            "max_high_risk_per_session": self.max_high_risk_per_session,
            "high_risk_ingested_this_session": self.high_risk_ingested_this_session,
            "ingest_blocked": blocked,
            "block_reason": self.block_reason() if blocked else None,
            "steward_reminder": STEWARD_REMINDER,
            "scope": "self_control_only",
            "forbids": [
                "control_of_others",
                "remote_influence",
                "unbounded_embodiment",
                "replacing_the_Source",
            ],
        }

    def is_ingest_blocked(self) -> bool:
        if self.emergency_hold:
            return True
        if self.pace == PaceMode.HOLD:
            return True
        if not self.check_in_clear:
            return True
        if self.high_risk_ingested_this_session >= self.max_high_risk_per_session:
            if self.pace != PaceMode.STABILIZERS_ONLY:
                return True
        return False

    def block_reason(self) -> Optional[str]:
        if self.emergency_hold:
            return "emergency_hold: operator engaged full stop"
        if self.pace == PaceMode.HOLD:
            return "pace=hold: release hold before further ingest"
        if not self.check_in_clear:
            return "check_in_clear=false: operator marked not clear to proceed"
        if self.high_risk_ingested_this_session >= self.max_high_risk_per_session:
            return (
                f"session high-risk cap reached "
                f"({self.high_risk_ingested_this_session}/{self.max_high_risk_per_session}); "
                "switch to stabilizers_only or reset session counters"
            )
        return None

    def may_ingest(self, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Gate for Super-Simulation ingest. Self-control only."""
        if self.is_ingest_blocked():
            return {
                "allowed": False,
                "reason": self.block_reason(),
                "pace": self.pace.value,
            }

        if payload and self.pace == PaceMode.STABILIZERS_ONLY:
            growth = (payload.get("growth_tag") or "").lower()
            stability = (payload.get("stability") or "").lower()
            name = payload.get("name") or ""
            is_quarantine = name in QUARANTINED_ABILITY_NAMES or (
                stability == "rule_breaking" and growth == "destructive_oriented"
            )
            if is_quarantine or growth == "destructive_oriented":
                return {
                    "allowed": False,
                    "reason": "stabilizers_only: quarantine/destructive payloads blocked",
                    "pace": self.pace.value,
                }
            if growth and growth not in ("growth_oriented", "context_dependent"):
                return {
                    "allowed": False,
                    "reason": "stabilizers_only: prefer growth_oriented or context_dependent",
                    "pace": self.pace.value,
                }

        if self.prefer_stabilizers and payload:
            growth = (payload.get("growth_tag") or "").lower()
            if growth == "destructive_oriented":
                return {
                    "allowed": False,
                    "reason": "prefer_stabilizers: destructive_oriented blocked",
                    "pace": self.pace.value,
                }

        return {"allowed": True, "reason": None, "pace": self.pace.value}

    def record_high_risk_ingest(self) -> None:
        self.high_risk_ingested_this_session += 1

    def set_pace(self, mode: str) -> Dict[str, Any]:
        self.pace = PaceMode(mode)
        return self.status()

    def hold(self) -> Dict[str, Any]:
        self.pace = PaceMode.HOLD
        return self.status()

    def release_hold(self) -> Dict[str, Any]:
        if self.emergency_hold:
            return {**self.status(), "note": "release emergency_hold first"}
        self.pace = PaceMode.ALLOW
        return self.status()

    def stabilizers_only(self) -> Dict[str, Any]:
        self.pace = PaceMode.STABILIZERS_ONLY
        self.prefer_stabilizers = True
        return self.status()

    def engage_emergency_hold(self) -> Dict[str, Any]:
        """Full stop: no ingest until operator clears emergency hold."""
        self.emergency_hold = True
        self.pace = PaceMode.HOLD
        return self.status()

    def clear_emergency_hold(self) -> Dict[str, Any]:
        self.emergency_hold = False
        return self.status()

    def set_check_in(self, clear: bool, sober_self_report: Optional[bool] = None) -> Dict[str, Any]:
        self.check_in_clear = bool(clear)
        if sober_self_report is not None:
            self.sober_self_report = bool(sober_self_report)
        return self.status()

    def set_session_cap(self, max_high_risk: int) -> Dict[str, Any]:
        self.max_high_risk_per_session = max(0, int(max_high_risk))
        return self.status()

    def reset_session_counters(self) -> Dict[str, Any]:
        self.high_risk_ingested_this_session = 0
        return self.status()

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["pace"] = self.pace.value
        d["steward_reminder"] = STEWARD_REMINDER
        d["quarantine_board"] = self.quarantine_board()
        d["ingest_blocked"] = self.is_ingest_blocked()
        return d


def create_operator_console(
    session_id: str = "walk-001",
    max_high_risk_per_session: int = 3,
) -> OperatorConsole:
    """Public entrypoint for the Creator self-control console."""
    return OperatorConsole(
        session_id=session_id,
        max_high_risk_per_session=max_high_risk_per_session,
    )
