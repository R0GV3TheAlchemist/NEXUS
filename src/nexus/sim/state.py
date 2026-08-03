from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class SimulationState:
    time_step: int = 0
    active_domains: List[str] = field(default_factory=list)
    abilities: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    ledger: List[Dict[str, Any]] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "time_step": self.time_step,
            "active_domains": list(self.active_domains),
            "abilities": dict(self.abilities),
            "ledger": list(self.ledger),
            "variables": dict(self.variables),
        }

    def advance(self) -> None:
        self.time_step += 1

    def register_ability(self, ability: Dict[str, Any]) -> None:
        name = ability.get("name")
        if name:
            self.abilities[name] = ability

    def append_ledger_entry(self, entry: Dict[str, Any]) -> None:
        self.ledger.append(entry)
