"""Canonical NEXUS simulation engine.

Applies AbilitySchema effects to CoreState under policy gates, records a
ledger entry, and persists each run. This is the Super-Simulation substrate;
batch / Primordial Walk orchestration will layer on top (Issue #4).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from nexus.core.ability_schema import AbilitySchema
from nexus.core.models import CoreState, RunResult
from nexus.core.policy import assess_ability, should_accept_ability
from nexus.io.accounting import Ledger
from nexus.subjects.adapter import adapt_ability_to_subjects

# Core state variable names used for effect application and snapshots.
STATE_KEYS = ("chaos", "order", "void", "light", "balance", "law", "magic")


class NEXUSEngine:
    """Apply abilities to a CoreState under policy, with ledger + persistence."""

    def __init__(self, output_dir: str = "data/runs", state: Optional[CoreState] = None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.state = state if state is not None else CoreState()
        self.ledger = Ledger()
        self.time_step: int = 0

    def reset(self) -> None:
        self.state = CoreState()
        self.time_step = 0

    def snapshot(self) -> Dict[str, Any]:
        """Return a plain dict of the current state and time step."""
        data = self.state.as_dict()
        data["time_step"] = self.time_step
        return data

    def apply_ability(self, ability: AbilitySchema, run_id: str) -> RunResult:
        subject_view = adapt_ability_to_subjects(ability)
        accepted = should_accept_ability(ability)
        before = CoreState(**self.state.as_dict())
        if accepted:
            self._apply_effects(ability.effects)
            self.time_step += 1
        after = CoreState(**self.state.as_dict())
        assessment = assess_ability(ability)
        result = RunResult(
            run_id=run_id,
            ability=ability,
            before=before,
            after=after,
            interpretation=str(
                {
                    "accept": accepted,
                    "assessment": assessment,
                    "subjects": subject_view,
                    "time_step": self.time_step,
                }
            ),
        )
        self.ledger.add(
            {
                "run_id": run_id,
                "ability": ability.to_dict(),
                "decision": "accepted" if accepted else "rejected",
                "subjects": subject_view,
                "time_step": self.time_step,
            }
        )
        self._persist_run(result)
        return result

    def _apply_effects(self, effects: Dict[str, float]) -> None:
        for key, delta in effects.items():
            if key in STATE_KEYS and hasattr(self.state, key):
                current = float(getattr(self.state, key))
                setattr(self.state, key, current + float(delta))

    def _persist_run(self, result: RunResult) -> None:
        path = self.output_dir / f"{result.run_id}.json"
        path.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
