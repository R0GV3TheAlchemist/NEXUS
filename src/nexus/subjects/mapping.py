from typing import Dict

from nexus.core.ability_schema import AbilitySchema


DEFAULT_DOMAINS = [
    "physics",
    "chemistry",
    "biology",
    "ecology",
    "psychology",
    "sociology",
    "economics",
    "governance",
    "ethics",
    "philosophy",
    "computer_science",
]


def map_ability_to_domains(ability: AbilitySchema) -> Dict[str, Dict[str, float]]:
    return {domain: ability.domain_effects.get(domain, {}) for domain in ability.subject_domains}


def ensure_known_domains(ability: AbilitySchema) -> list[str]:
    return [domain for domain in ability.subject_domains if domain not in DEFAULT_DOMAINS]
