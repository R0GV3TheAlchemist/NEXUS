"""Fail-closed policy classifier for catalog rows (I4).

Tags only — does not mutate CoreState, embody, or production-enable.
Precedence (highest first):
  quarantine_named > ethics_reject > high_risk > needs_human
  > stabilizer | resource_pool > map_ok
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from nexus.catalog.models import POLICY_TAGS, CatalogEntry, SchemaDraft
from nexus.catalog.quarantine_names import quarantined_ability_names
from nexus.catalog.store import CatalogStore

_ETHICS_NAME = re.compile(
    r"("
    r"life[- ]?force|soul|aura absorption|personality|"
    r"beauty thievery|youth thievery|age thievery|"
    r"vampir|blood drain|drain touch|"
    r"assimilative infection|assimilative evolution|"
    r"bio-absorbing replication|consumptive replication|"
    r"power absorption|superpower absorption|"
    r"benevorous|malevorous|"
    r"mind absorption|memory absorption|knowledge absorption"
    r")",
    re.I,
)

_ETHICS_SUMMARY = re.compile(
    r"("
    r"absorb(?:s|ing|ed)? (?:the )?powers? of others|"
    r"steal(?:s|ing)? (?:the )?powers?|"
    r"life[- ]?force|soul(?:s)?|personality|"
    r"infect(?:s|ing|ion)?|contagion|"
    r"assimilat(?:e|es|ing|ion).{0,40}(living|people|others|beings)|"
    r"feed(?:s|ing)? (?:off|on) (?:the )?(?:goodness|darkness|youth|beauty)|"
    r"taking away (?:their|the) (?:targets?'? )?(?:radiance|health|vitality|youth|beauty)"
    r")",
    re.I,
)

_HIGH_RISK_NAME = re.compile(
    r"("
    r"antimatter|absolute |omni-|omni |meta |totality |"
    r"nuclear absorption|stellar absorption|"
    r"infection|vortex creation|black hole|void absorption"
    r")",
    re.I,
)

_NEEDS_HUMAN = re.compile(
    r"("
    r"omni|absolute|almighty|godhood|near-god|transcendent|"
    r"unlimited|boundless|without limit|totality|meta-"
    r")",
    re.I,
)

_STABILIZER = re.compile(
    r"("
    r"immunity|shield|stabilit|purification|containment|"
    r"order manipulation|seal|barrier|ward|resistance"
    r")",
    re.I,
)

_RESOURCE_POOL = re.compile(
    r"("
    r"capacitor|battery|store (?:ambient )?energy|energy storage|"
    r"bio-capacitor|living battery"
    r")",
    re.I,
)

_STABILITY_FOR_TAGS = {
    "quarantine_named": "rule_breaking",
    "ethics_reject": "rule_breaking",
    "high_risk": "rule_breaking",
    "needs_human": "conditionally_stable",
    "stabilizer": "stable",
    "resource_pool": "conditionally_stable",
    "map_ok": "conditionally_stable",
}

_GROWTH_FOR_TAGS = {
    "quarantine_named": "destructive_oriented",
    "ethics_reject": "destructive_oriented",
    "high_risk": "destructive_oriented",
    "needs_human": "context_dependent",
    "stabilizer": "growth_oriented",
    "resource_pool": "growth_oriented",
    "map_ok": "growth_oriented",
}


@dataclass(frozen=True)
class ClassifyResult:
    name: str
    tags: tuple[str, ...]
    reasons: tuple[str, ...]
    primary: str


@dataclass(frozen=True)
class ClassifyReport:
    total: int
    updated: int
    by_primary: dict[str, int]


def _text(entry: CatalogEntry) -> str:
    return f"{entry.name}\n{entry.summary}"


def classify_text(name: str, summary: str = "") -> ClassifyResult:
    dummy = CatalogEntry(name=name, url="https://example.invalid/" + name, summary=summary)
    return classify_entry(dummy)


def classify_entry(entry: CatalogEntry) -> ClassifyResult:
    reasons: list[str] = []
    tags: list[str] = []
    name = entry.name.strip()
    blob = _text(entry)
    qnames = quarantined_ability_names()

    if name.startswith("Category:") or (
        len(entry.category_path) > 1 and entry.category_path[-1] == "_subcat"
    ):
        return ClassifyResult(
            name=name,
            tags=(),
            reasons=("structural_subcategory",),
            primary="structural",
        )

    if name in qnames:
        tags.append("quarantine_named")
        reasons.append("exact_quarantine_name")

    if _ETHICS_NAME.search(name) or _ETHICS_SUMMARY.search(blob):
        if "ethics_reject" not in tags:
            tags.append("ethics_reject")
        reasons.append("ethics_pattern")

    if _HIGH_RISK_NAME.search(name) or _HIGH_RISK_NAME.search(entry.summary):
        if "high_risk" not in tags:
            tags.append("high_risk")
        reasons.append("high_risk_pattern")

    if _NEEDS_HUMAN.search(name) or _NEEDS_HUMAN.search(entry.summary):
        if "needs_human" not in tags:
            tags.append("needs_human")
        reasons.append("absolute_or_omni_language")

    if _STABILIZER.search(name) or _STABILIZER.search(entry.summary):
        if "ethics_reject" not in tags and "quarantine_named" not in tags:
            tags.append("stabilizer")
            reasons.append("stabilizer_pattern")

    if _RESOURCE_POOL.search(name) or _RESOURCE_POOL.search(entry.summary):
        if "ethics_reject" not in tags and "quarantine_named" not in tags:
            tags.append("resource_pool")
            reasons.append("resource_pool_pattern")

    blocking = {"quarantine_named", "ethics_reject", "high_risk", "needs_human"}
    if not (set(tags) & blocking):
        if "stabilizer" in tags or "resource_pool" in tags or not tags:
            if "map_ok" not in tags:
                tags.append("map_ok")
            reasons.append("no_blocking_tags")

    tags = [t for t in tags if t in POLICY_TAGS]
    primary = _primary_tag(tags)
    return ClassifyResult(
        name=name, tags=tuple(tags), reasons=tuple(reasons), primary=primary
    )


def _primary_tag(tags: list[str]) -> str:
    order = [
        "quarantine_named",
        "ethics_reject",
        "high_risk",
        "needs_human",
        "stabilizer",
        "resource_pool",
        "map_ok",
    ]
    for key in order:
        if key in tags:
            return key
    return "untagged"


def apply_classification(
    entry: CatalogEntry,
    result: ClassifyResult,
    *,
    update_schema_hints: bool = True,
) -> CatalogEntry:
    draft = entry.schema_draft
    if update_schema_hints and result.primary in _STABILITY_FOR_TAGS:
        draft = SchemaDraft(
            family=draft.family,
            stability=_STABILITY_FOR_TAGS[result.primary],
            growth_tag=_GROWTH_FOR_TAGS[result.primary],
            subject_domains=draft.subject_domains,
            effects_hint=dict(draft.effects_hint),
            physics_analog=draft.physics_analog,
        )
    return CatalogEntry(
        name=entry.name,
        url=entry.url,
        category_path=entry.category_path,
        letter_bucket=entry.letter_bucket,
        source_license=entry.source_license,
        attribution=entry.attribution,
        fanon=entry.fanon,
        summary=entry.summary,
        schema_draft=draft,
        policy_tags=result.tags,
        walk=entry.walk,
    )


def classify_index(
    store: CatalogStore,
    *,
    write: bool = True,
    names: Iterable[str] | None = None,
    update_schema_hints: bool = True,
) -> tuple[ClassifyReport, list[ClassifyResult]]:
    entries = store.load_index()
    allow = {n.casefold() for n in names} if names is not None else None
    results: list[ClassifyResult] = []
    out: list[CatalogEntry] = []
    updated = 0
    by_primary: dict[str, int] = {}

    for entry in entries:
        if allow is not None and entry.name.casefold() not in allow:
            out.append(entry)
            continue
        result = classify_entry(entry)
        results.append(result)
        by_primary[result.primary] = by_primary.get(result.primary, 0) + 1
        new_entry = apply_classification(
            entry, result, update_schema_hints=update_schema_hints
        )
        if new_entry.policy_tags != entry.policy_tags or (
            update_schema_hints
            and new_entry.schema_draft.stability != entry.schema_draft.stability
        ):
            updated += 1
        out.append(new_entry)

    if write:
        ordered = sorted(out, key=lambda e: e.name.casefold())
        store.save_index(ordered)

    report = ClassifyReport(total=len(results), updated=updated, by_primary=by_primary)
    return report, results
