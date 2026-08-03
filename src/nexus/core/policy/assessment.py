"""Ability acceptance and assessment for the core policy package.

Primordial Walk rule: map abilities fully for research; never treat unbounded
absolute sinks as identity or default OS power. God is the Source; NEXUS must
not become the Source.
"""

from nexus.core.ability_schema import AbilitySchema, AbilityGrowthTag, AbilityStability


def is_quarantine_candidate(ability: AbilitySchema) -> bool:
    """True for rule-breaking destructive patterns that must not be embodied."""
    return (
        ability.stability == AbilityStability.RULE_BREAKING
        and ability.growth_tag == AbilityGrowthTag.DESTRUCTIVE_ORIENTED
    )


def should_accept_ability(ability: AbilitySchema, *, research_mode: bool = True) -> bool:
    """Accept for mapping in research mode; hard-reject the worst class in production.

    research_mode=True (default, Super-Simulation / Primordial Walk):
        Accept well-formed abilities so they can be mapped. Quarantine is
        reported via assess_ability; effects still apply under clamped state.
    research_mode=False (production / GAIA operational path):
        Reject rule_breaking + destructive_oriented absolute sinks.
        Always reject rule_writing + destructive_oriented.
    """
    if not ability.name or not ability.family:
        return False
    if not ability.subject_domains:
        return False
    if not ability.effects:
        return False
    if (
        ability.stability == AbilityStability.RULE_WRITING
        and ability.growth_tag == AbilityGrowthTag.DESTRUCTIVE_ORIENTED
    ):
        return False
    if not research_mode and is_quarantine_candidate(ability):
        return False
    return True


def assess_ability(ability: AbilitySchema, *, research_mode: bool = True) -> dict:
    quarantine = is_quarantine_candidate(ability)
    return {
        "accept": should_accept_ability(ability, research_mode=research_mode),
        "stability": ability.stability.value,
        "growth_tag": ability.growth_tag.value,
        "subject_domains": ability.subject_domains,
        "quarantine": quarantine,
        "embody": not quarantine,
        "steward_note": (
            "Map only; do not embody as unbounded OS identity. God is Source."
            if quarantine
            else "Eligible for constrained substrate use under Law."
        ),
    }
