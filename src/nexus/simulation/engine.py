from pathlib import Path
from typing import Dict, Any
import json

from nexus.core.models import CoreState, AbilityRecord, RunResult
from nexus.core.policy import assess_ability, should_accept_ability
from nexus.io.accounting import Ledger


class NEXUSEngine:
    def __init__(self, output_dir: str = "data/runs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.state = CoreState()
        self.ledger = Ledger()

    def reset(self) -> None:
        self.state = CoreState()

    def apply_ability(self, ability: AbilityRecord, run_id: str) -> RunResult:
        if not should_accept_ability(ability):
            result = RunResult(run_id=run_id, ability=ability, before=CoreState(**self.state.as_dict()), after=CoreState(**self.state.as_dict()), interpretation="rejected")
            self.ledger.add({"run_id": run_id, "ability": ability.to_dict(), "decision": "rejected"})
            self._persist_run(result)
            return result

        before = CoreState(**self.state.as_dict())
        self._apply_effects(ability.effects)
        after = CoreState(**self.state.as_dict())
        result = RunResult(run_id=run_id, ability=ability, before=before, after=after, interpretation=str(assess_ability(ability)))
        self.ledger.add({"run_id": run_id, "ability": ability.to_dict(), "decision": "accepted"})
        self._persist_run(result)
        return result

    def _apply_effects(self, effects: Dict[str, float]) -> None:
        for key, delta in effects.items():
            if hasattr(self.state, key):
                setattr(self.state, key, getattr(self.state, key) + float(delta))

    def _persist_run(self, result: RunResult) -> None:
        path = self.output_dir / f"{result.run_id}.json"
        path.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
