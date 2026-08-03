from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List


class Stability(str, Enum):
    STABLE = "stable"
    CONDITIONALLY_STABLE = "conditionally_stable"
    RULE_BREAKING = "rule_breaking"
    RULE_WRITING = "rule_writing"


class GrowthTag(str, Enum):
    GROWTH_ORIENTED = "growth_oriented"
    DESTRUCTIVE_ORIENTED = "destructive_oriented"
    CONTEXT_DEPENDENT = "context_dependent"


@dataclass
class CoreState:
    chaos: float = 0.0
    order: float = 0.0
    void: float = 0.0
    light: float = 0.0
    balance: float = 0.0
    law: float = 0.0
    magic: float = 0.0

    def as_dict(self) -> Dict[str, float]:
        return asdict(self)

    def clamp(self, low: float = 0.0, high: float = 1.0) -> "CoreState":
        """Constrain all state variables to [low, high]. Mutates and returns self."""
        for key in ("chaos", "order", "void", "light", "balance", "law", "magic"):
            value = float(getattr(self, key))
            if value < low:
                setattr(self, key, low)
            elif value > high:
                setattr(self, key, high)
        return self


@dataclass
class RunResult:
    run_id: str
    ability: Any
    before: CoreState
    after: CoreState
    interpretation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        ability_dict = self.ability.to_dict() if hasattr(self.ability, "to_dict") else self.ability
        return {
            "run_id": self.run_id,
            "ability": ability_dict,
            "before": self.before.as_dict(),
            "after": self.after.as_dict(),
            "interpretation": self.interpretation,
        }
