from typing import Dict, Any, List

from nexus.core.ability_schema import AbilitySchema, AbilityStability, AbilityGrowthTag
from nexus.core.policy import should_accept_ability


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def normalize_family(value: str) -> str:
    return normalize_text(value).lower().replace(" ", "_")


def build_ability(payload: Dict[str, Any]) -> AbilitySchema:
    return AbilitySchema(
        name=normalize_text(payload.get("name", "")),
        family=normalize_family(payload.get("family", "")),
        source=payload.get("source", "Superpower Wiki"),
        aliases=payload.get("aliases", []) or [],
        subject_domains=payload.get("subject_domains", []) or [],
        physics_analog=payload.get("physics_analog", ""),
        effects=payload.get("effects", {}) or {},
        domain_effects=payload.get("domain_effects", {}) or {},
        scale=payload.get("scale", ""),
        stability=AbilityStability(payload.get("stability", AbilityStability.CONDITIONALLY_STABLE.value)),
        growth_tag=AbilityGrowthTag(payload.get("growth_tag", AbilityGrowthTag.CONTEXT_DEPENDENT.value)),
        notes=payload.get("notes", ""),
        metadata=payload.get("metadata", {}) or {},
    )


def validate_payload(payload: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    if not payload.get("name"):
        issues.append("missing_name")
    if not payload.get("family"):
        issues.append("missing_family")
    if not payload.get("subject_domains"):
        issues.append("missing_subject_domains")
    if not payload.get("effects"):
        issues.append("missing_effects")
    return issues


def ingest_ability_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    issues = validate_payload(payload)
    if issues:
        return {"accepted": False, "issues": issues, "ability": None}

    ability = build_ability(payload)
    accepted = should_accept_ability(ability)
    return {
        "accepted": accepted,
        "issues": [],
        "ability": ability.to_dict(),
    }


# src/nexus/core/registry.py
from dataclasses import dataclass, field
from typing import Dict, Optional

from .ability_schema import AbilitySchema


@dataclass
class AbilityRegistry:
    abilities: Dict[str, AbilitySchema] = field(default_factory=dict)

    def add(self, ability: AbilitySchema) -> None:
        self.abilities[ability.name] = ability

    def get(self, name: str) -> Optional[AbilitySchema]:
        return self.abilities.get(name)

    def list_names(self) -> list[str]:
        return list(self.abilities.keys())


# src/nexus/io/ability_store.py
from pathlib import Path
import json
from typing import Iterable

from nexus.core.ability_schema import AbilitySchema


def save_abilities(path: str, abilities: Iterable[AbilitySchema]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps([a.to_dict() for a in abilities], indent=2), encoding="utf-8")


def load_abilities(path: str) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))
