from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class AbilityStability(str, Enum):
    STABLE = "stable"
    CONDITIONALLY_STABLE = "conditionally_stable"
    RULE_BREAKING = "rule_breaking"
    RULE_WRITING = "rule_writing"


class AbilityGrowthTag(str, Enum):
    GROWTH_ORIENTED = "growth_oriented"
    DESTRUCTIVE_ORIENTED = "destructive_oriented"
    CONTEXT_DEPENDENT = "context_dependent"


@dataclass
class AbilitySchema:
    name: str
    family: str
    source: str = "Superpower Wiki"
    aliases: List[str] = field(default_factory=list)
    subject_domains: List[str] = field(default_factory=list)
    physics_analog: str = ""
    effects: Dict[str, float] = field(default_factory=dict)
    domain_effects: Dict[str, Dict[str, float]] = field(default_factory=dict)
    scale: str = ""
    stability: AbilityStability = AbilityStability.CONDITIONALLY_STABLE
    growth_tag: AbilityGrowthTag = AbilityGrowthTag.CONTEXT_DEPENDENT
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "family": self.family,
            "source": self.source,
            "aliases": self.aliases,
            "subject_domains": self.subject_domains,
            "physics_analog": self.physics_analog,
            "effects": self.effects,
            "domain_effects": self.domain_effects,
            "scale": self.scale,
            "stability": self.stability.value,
            "growth_tag": self.growth_tag.value,
            "notes": self.notes,
            "metadata": self.metadata,
        }
