from .models import AbilityRecord, GrowthTag, Stability


def should_accept_ability(ability: AbilityRecord) -> bool:
    if not ability.name or not ability.family:
        return False
    if ability.stability == Stability.RULE_WRITING and ability.growth_tag == GrowthTag.DESTRUCTIVE_ORIENTED:
        return False
    return True


def assess_ability(ability: AbilityRecord) -> dict:
    return {
        "accept": should_accept_ability(ability),
        "stability": ability.stability.value,
        "growth_tag": ability.growth_tag.value,
        "subject_domains": ability.subject_domains,
    }
