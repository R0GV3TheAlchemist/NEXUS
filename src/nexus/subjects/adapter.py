from typing import Dict

from nexus.core.ability_schema import AbilitySchema
from .mapping import map_ability_to_domains, ensure_known_domains


def adapt_ability_to_subjects(ability: AbilitySchema) -> Dict[str, object]:
    unknown_domains = ensure_known_domains(ability)
    return {
        "known_domains": [d for d in ability.subject_domains if d not in unknown_domains],
        "domain_effects": map_ability_to_domains(ability),
        "unknown_domains": unknown_domains,
    }
