from pathlib import Path
import json
from typing import Dict

from nexus.core.models import CoreState, RunResult
from nexus.core.policy import assess_ability, should_accept_ability
from nexus.core.ability_schema import AbilitySchema
from nexus.io.accounting import Ledger
from nexus.subjects.adapter import adapt_ability_to_subjects


class NEXUSEngine:
    def __init__(self, output_dir: str = "data/runs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.state = CoreState()
        self.ledger = Ledger()

    def reset(self) -> None:
        self.state = CoreState()

    def apply_ability(self, ability: AbilitySchema, run_id: str) -> RunResult:
        subject_view = adapt_ability_to_subjects(ability)
        accepted = should_accept_ability(ability)
        before = CoreState(**self.state.as_dict())
        if accepted:
            self._apply_effects(ability.effects)
        after = CoreState(**self.state.as_dict())
        result = RunResult(
            run_id=run_id,
            ability=ability,
            before=before,
            after=after,
            interpretation=str({"accept": accepted, "assessment": assess_ability(ability), "subjects": subject_view}),
        )
        self.ledger.add({
            "run_id": run_id,
            "ability": ability.to_dict(),
            "decision": "accepted" if accepted else "rejected",
            "subjects": subject_view,
        })
        self._persist_run(result)
        return result

    def _apply_effects(self, effects: Dict[str, float]) -> None:
        for key, delta in effects.items():
            if hasattr(self.state, key):
                setattr(self.state, key, getattr(self.state, key) + float(delta))

    def _persist_run(self, result: RunResult) -> None:
        path = self.output_dir / f"{result.run_id}.json"
        path.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
