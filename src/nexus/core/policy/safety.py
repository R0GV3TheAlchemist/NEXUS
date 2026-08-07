"""Protective measures for Primordial Walk abilities (Batch 1–2).

These controls exist so NEXUS maps absolute sinks without embodying them.
God is the Source; the system must not become the Source.

Safety is not optional flavor — it is load-bearing policy for operators
and for anyone carrying the Walk.
"""

from __future__ import annotations

from typing import Any, Dict, FrozenSet

from nexus.core.ability_schema import AbilitySchema, AbilityGrowthTag, AbilityStability


# Explicit registry of walk-001 abilities that must stay non-operational
# as unbounded sinks. Names match Superpower Wiki titles used in the catalog.
QUARANTINED_ABILITY_NAMES: FrozenSet[str] = frozenset({
    "Absolute Electricity Absorption",
    "Absolute Electromagnetic Absorption",
    "Absolute Gamma Absorption",
    "Absolute Heat Absorption",
    "Absolute Ionic Absorption",
    "Absolute Kinetic Absorption",
    "Absolute Light Absorption",
    "Absolute Nuclear Absorption",
    "Absolute Quantum Absorption",
    "Absolute Radiation Absorption",
    "Absolute Sound Absorption",
    "Absolute Solar Absorption",
    "Absolute Stellar Absorption",
    "Absolute Thermic Absorption",
    "Absolute Wave Absorption",
})

# Soft quarantine: rule_breaking but not destructive_oriented — still
# capacity-limited; never default OS identity.
CAPACITY_LIMITED_NAMES: FrozenSet[str] = frozenset({
    "Absolute Absorption",
    "Absolute Cosmic Absorption",
})

PROTECTIVE_CONSTRAINTS: Dict[str, str] = {
    "no_embody": (
        "Quarantined abilities must not be implemented as unbounded OS "
        "identity, default resource pools, or autonomous actuators."
    ),
    "capacity_required": (
        "Any constrained substrate use requires explicit capacity, rate, "
        "and discharge limits under Law before activation."
    ),
    "production_reject": (
        "In production / GAIA operational mode, quarantine candidates are "
        "hard-rejected unless a multi-key governance override is recorded."
    ),
    "research_map_only": (
        "Research / Primordial Walk mode may map effects under clamped "
        "CoreState for evidence only; mapping is not permission to deploy."
    ),
    "operator_care": (
        "Operators carrying the Walk should pace intake, prefer stabilizers "
        "when distressed, and treat quarantine as protection for self and system."
    ),
    "steward_bound": (
        "NEXUS and GAIA are steward systems. God is the Source. "
        "Never become the Source."
    ),
}


def is_named_quarantine(name: str) -> bool:
    """True if the ability name is on the explicit walk-001 quarantine list."""
    return name.strip() in QUARANTINED_ABILITY_NAMES


def is_capacity_limited(name: str) -> bool:
    return name.strip() in CAPACITY_LIMITED_NAMES


def _pattern_quarantine(ability: AbilitySchema) -> bool:
    return (
        ability.stability == AbilityStability.RULE_BREAKING
        and ability.growth_tag == AbilityGrowthTag.DESTRUCTIVE_ORIENTED
    )


def protective_status(ability: AbilitySchema) -> Dict[str, Any]:
    """Full protective assessment for an ability."""
    quarantine = _pattern_quarantine(ability) or is_named_quarantine(ability.name)
    capacity = is_capacity_limited(ability.name) or quarantine
    return {
        "name": ability.name,
        "quarantine": quarantine,
        "named_registry": is_named_quarantine(ability.name),
        "capacity_limited": capacity,
        "embody_allowed": not quarantine,
        "production_deployable": False if quarantine else True,
        "constraints": (
            list(PROTECTIVE_CONSTRAINTS.keys())
            if quarantine
            else ["capacity_required", "steward_bound"]
        ),
        "constraint_text": (
            [PROTECTIVE_CONSTRAINTS[k] for k in (
                "no_embody", "capacity_required", "production_reject",
                "research_map_only", "operator_care", "steward_bound",
            )]
            if quarantine
            else [PROTECTIVE_CONSTRAINTS["capacity_required"], PROTECTIVE_CONSTRAINTS["steward_bound"]]
        ),
        "steward_note": (
            "PROTECTED: map only; do not embody. God is Source."
            if quarantine
            else "Constrained use under Law only."
        ),
    }


def safety_summary() -> Dict[str, Any]:
    """Summary of active protective measures for abilities 1–20."""
    return {
        "session": "walk-001",
        "batches_covered": [1, 2],
        "quarantined_count": len(QUARANTINED_ABILITY_NAMES),
        "capacity_limited_extra": len(CAPACITY_LIMITED_NAMES),
        "quarantined_names": sorted(QUARANTINED_ABILITY_NAMES),
        "constraints": PROTECTIVE_CONSTRAINTS,
        "production_default": "reject_quarantine",
        "research_default": "map_under_clamp_no_embody",
    }
