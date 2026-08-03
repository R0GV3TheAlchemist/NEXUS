from .ability_schema import AbilitySchema, AbilityGrowthTag, AbilityStability


def should_accept_ability(ability: AbilitySchema) -> bool:
    if not ability.name or not ability.family:
        return False
    if not ability.subject_domains:
        return False
    if not ability.effects:
        return False
    if ability.stability == AbilityStability.RULE_WRITING and ability.growth_tag == AbilityGrowthTag.DESTRUCTIVE_ORIENTED:
        return False
    return True


def assess_ability(ability: AbilitySchema) -> dict:
    return {
        "accept": should_accept_ability(ability),
        "stability": ability.stability.value,
        "growth_tag": ability.growth_tag.value,
        "subject_domains": ability.subject_domains,
    }
