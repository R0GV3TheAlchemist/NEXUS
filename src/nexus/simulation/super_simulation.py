"""Minimal Super-Simulation entrypoint.

The Super-Simulation is the developmental model that feeds NEXUS (Universal OS)
and GAIA (Worldwide OS). Ability inputs — typically normalized from Superpower
Wiki — are treated as labeled mechanisms with physics analogs, subject-domain
impacts, stability class, and growth tags. Runs produce structured evidence
(state deltas, acceptance decisions, subject coverage) that informs what the
operating-system layers may need to support next.

This module is intentionally minimal: initialize, ingest one ability or a
batch, snapshot state, and emit a short recommendation surface. Batch-of-10
Primordial Walk documentation and richer fitness metrics remain later work.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from nexus.core.ability_schema import AbilitySchema
from nexus.core.ingestion import build_ability, ingest_ability_payload
from nexus.core.models import CoreState
from nexus.simulation.engine import NEXUSEngine

# Primordial Walk baseline: high Chaos, low Order/Law, elevated Void.
PRIMORDIAL_BASELINE = CoreState(
    chaos=0.8,
    order=0.2,
    void=0.6,
    light=0.1,
    balance=0.1,
    law=0.1,
    magic=0.1,
)


def primordial_baseline() -> CoreState:
    """Return a fresh primordial-chaos CoreState."""
    return CoreState(**PRIMORDIAL_BASELINE.as_dict())


class SuperSimulation:
    """Import-safe Super-Simulation surface over the canonical NEXUSEngine."""

    def __init__(
        self,
        output_dir: str = "data/runs",
        state: Optional[CoreState] = None,
        use_primordial: bool = True,
    ):
        initial = state if state is not None else (
            primordial_baseline() if use_primordial else CoreState()
        )
        self.engine = NEXUSEngine(output_dir=output_dir, state=initial)
        self.runs: List[Dict[str, Any]] = []

    def snapshot(self) -> Dict[str, Any]:
        return self.engine.snapshot()

    def reset(self, use_primordial: bool = True) -> Dict[str, Any]:
        self.engine.state = primordial_baseline() if use_primordial else CoreState()
        self.engine.time_step = 0
        self.runs.clear()
        return self.snapshot()

    def ingest_payload(self, payload: Dict[str, Any], run_id: Optional[str] = None) -> Dict[str, Any]:
        """Validate a Superpower-Wiki-style payload and apply it if accepted."""
        validation = ingest_ability_payload(payload)
        if not validation["accepted"] or validation["ability"] is None:
            record = {
                "run_id": run_id or f"rejected-{len(self.runs) + 1}",
                "accepted": False,
                "issues": validation.get("issues", []),
                "state": self.snapshot(),
            }
            self.runs.append(record)
            return record

        ability = build_ability(payload)
        rid = run_id or f"run-{len(self.runs) + 1:04d}"
        result = self.engine.apply_ability(ability, rid)
        record = {
            "run_id": rid,
            "accepted": True,
            "ability": ability.to_dict(),
            "before": result.before.as_dict(),
            "after": result.after.as_dict(),
            "interpretation": result.interpretation,
            "state": self.snapshot(),
        }
        self.runs.append(record)
        return record

    def ingest_ability(self, ability: AbilitySchema, run_id: Optional[str] = None) -> Dict[str, Any]:
        """Apply a pre-built AbilitySchema."""
        rid = run_id or f"run-{len(self.runs) + 1:04d}"
        result = self.engine.apply_ability(ability, rid)
        record = {
            "run_id": rid,
            "accepted": "accepted" in result.interpretation,
            "ability": ability.to_dict(),
            "before": result.before.as_dict(),
            "after": result.after.as_dict(),
            "interpretation": result.interpretation,
            "state": self.snapshot(),
        }
        self.runs.append(record)
        return record

    def ingest_batch(
        self,
        payloads: Sequence[Dict[str, Any]],
        batch_id: str = "batch",
    ) -> Dict[str, Any]:
        """Ingest a sequence of ability payloads (e.g. a batch of 10)."""
        before = self.snapshot()
        results = [
            self.ingest_payload(payload, run_id=f"{batch_id}-{i + 1:02d}")
            for i, payload in enumerate(payloads)
        ]
        after = self.snapshot()
        return {
            "batch_id": batch_id,
            "count": len(payloads),
            "accepted": sum(1 for r in results if r.get("accepted")),
            "rejected": sum(1 for r in results if not r.get("accepted")),
            "before": before,
            "after": after,
            "results": results,
            "recommendations": self.recommend(),
        }

    def recommend(self) -> List[Dict[str, str]]:
        """Heuristic build recommendations from current state and subject gaps.

        These are evidence-shaped suggestions for OS module work, not oracle
        outputs. Higher void / lower order / law suggest foundation work;
        growth-tagged runs and covered subjects inform prioritization.
        """
        s = self.engine.state
        tips: List[Dict[str, str]] = []

        if s.void >= 0.5:
            tips.append({
                "priority": "high",
                "focus": "foundations",
                "reason": "Void is elevated: missing structure should be filled with explicit contracts and domain modules.",
            })
        if s.chaos >= 0.6 and s.order <= 0.4:
            tips.append({
                "priority": "high",
                "focus": "stabilization",
                "reason": "Chaos dominates Order: prefer stabilizing abilities and policy constraints before expansion.",
            })
        if s.law <= 0.3:
            tips.append({
                "priority": "medium",
                "focus": "policy_and_governance",
                "reason": "Law is low: strengthen acceptance rules, accounting, and GAIA coordination surfaces.",
            })
        if s.light <= 0.3:
            tips.append({
                "priority": "medium",
                "focus": "observability",
                "reason": "Light is low: improve logging, traceability, and inspection of runs.",
            })
        if s.balance <= 0.3:
            tips.append({
                "priority": "medium",
                "focus": "cross_domain_coupling",
                "reason": "Balance is low: mix subject domains deliberately rather than stacking one layer.",
            })
        if not tips:
            tips.append({
                "priority": "low",
                "focus": "incremental_expansion",
                "reason": "State is relatively settled: expand modules carefully and keep contracts testable.",
            })
        return tips


def initialize_super_simulation(
    output_dir: str = "data/runs",
    use_primordial: bool = True,
) -> SuperSimulation:
    """Single public entrypoint for Super-Simulation initialization.

    Import-safe and suitable for smoke tests:

        from nexus.simulation import initialize_super_simulation
        sim = initialize_super_simulation()
        sim.ingest_payload({...})
    """
    return SuperSimulation(output_dir=output_dir, use_primordial=use_primordial)
