from typing import Any, Dict

from .state import SimulationState


class SimulationEngine:
    def __init__(self, state: SimulationState | None = None):
        self.state = state or SimulationState()

    def ingest(self, ability: Dict[str, Any], accepted: bool, reason: str = "") -> Dict[str, Any]:
        entry = {
            "time_step": self.state.time_step,
            "ability": ability,
            "accepted": accepted,
            "reason": reason,
        }
        if accepted:
            self.state.register_ability(ability)
        self.state.append_ledger_entry(entry)
        return entry

    def step(self) -> Dict[str, Any]:
        self.state.advance()
        return self.state.snapshot()

    def run_once(self, ability: Dict[str, Any], accepted: bool, reason: str = "") -> Dict[str, Any]:
        self.ingest(ability, accepted, reason)
        return self.step()
