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


@dataclass
class AbilityRecord:
    name: str
    family: str
    subject_domains: List[str]
    physics_analog: str = ""
    effects: Dict[str, float] = field(default_factory=dict)
    domain_effects: Dict[str, Dict[str, float]] = field(default_factory=dict)
    scale: str = ""
    stability: Stability = Stability.CONDITIONALLY_STABLE
    growth_tag: GrowthTag = GrowthTag.CONTEXT_DEPENDENT
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["stability"] = self.stability.value
        data["growth_tag"] = self.growth_tag.value
        return data
