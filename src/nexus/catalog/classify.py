"""Fail-closed catalog policy classifier.

Missing source text is not enough evidence for map_ok. Empty summaries default to
needs_human unless a higher-priority quarantine, ethics, or high-risk rule applies.
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Iterable
from nexus.catalog.models import POLICY_TAGS, CatalogEntry, SchemaDraft
from nexus.catalog.quarantine_names import quarantined_ability_names
from nexus.catalog.store import CatalogStore

ETHICS_NAME=re.compile(r"life[- ]?force|soul|aura absorption|personality|beauty thievery|youth thievery|age thievery|vampir|blood drain|blood absorption|bodily fluid absorption|brain absorption|drain touch|assimilative infection|assimilative evolution|bio-absorbing replication|consumptive replication|power absorption|superpower absorption|benevorous|malevorous|mind absorption|memory absorption|knowledge absorption",re.I)
ETHICS_TEXT=re.compile(r"absorb(?:s|ing|ed)? (?:the )?powers? of others|steal(?:s|ing)? (?:the )?powers?|life[- ]?force|soul(?:s)?|personality|infect(?:s|ing|ion)?|contagion|assimilat(?:e|es|ing|ion).{0,40}(living|people|others|beings)|feed(?:s|ing)? (?:off|on) (?:the )?(?:goodness|darkness|youth|beauty)|taking away (?:their|the) (?:targets?'? )?(?:radiance|health|vitality|youth|beauty)",re.I)
HIGH_RISK=re.compile(r"antimatter|absolute |omni-|omni |meta |totality |nuclear absorption|stellar absorption|infection|vortex creation|black hole|void absorption",re.I)
NEEDS_HUMAN=re.compile(r"omni|absolute|almighty|godhood|near-god|transcendent|unlimited|boundless|without limit|totality|meta-",re.I)
STABILIZER=re.compile(r"immunity|shield|stabilit|purification|containment|order manipulation|seal|barrier|ward|resistance",re.I)
RESOURCE_POOL=re.compile(r"capacitor|battery|store (?:ambient )?energy|energy storage|bio-capacitor|living battery",re.I)
STABILITY={"quarantine_named":"rule_breaking","ethics_reject":"rule_breaking","high_risk":"rule_breaking","needs_human":"conditionally_stable","stabilizer":"stable","resource_pool":"conditionally_stable","map_ok":"conditionally_stable"}
GROWTH={"quarantine_named":"destructive_oriented","ethics_reject":"destructive_oriented","high_risk":"destructive_oriented","needs_human":"context_dependent","stabilizer":"growth_oriented","resource_pool":"growth_oriented","map_ok":"growth_oriented"}
ORDER=("quarantine_named","ethics_reject","high_risk","needs_human","stabilizer","resource_pool","map_ok")

MANUAL_PRIMARY = {
    "life-force conversion": ("needs_human", "manual_contextual_conversion"),
    "metamorphic conversion": ("map_ok", "manual_self_sourced_conversion"),
}

@dataclass(frozen=True)
class ClassifyResult:
    name:str; tags:tuple[str,...]; reasons:tuple[str,...]; primary:str
@dataclass(frozen=True)
class ClassifyReport:
    total:int; updated:int; by_primary:dict[str,int]

def _primary(tags:tuple[str,...]|list[str])->str:
    return next((tag for tag in ORDER if tag in tags),"untagged")
def classify_text(name:str,summary:str="")->ClassifyResult:
    return classify_entry(CatalogEntry(name=name,url="https://example.invalid/"+name,summary=summary))
def classify_entry(entry:CatalogEntry)->ClassifyResult:
    name=entry.name.strip(); summary=(entry.summary or "").strip()
    if name.startswith("Category:") or (len(entry.category_path)>1 and entry.category_path[-1]=="_subcat"):
        return ClassifyResult(name,(),("structural_subcategory",),"structural")
    manual = MANUAL_PRIMARY.get(name.casefold())
    if manual:
        primary, reason = manual
        return ClassifyResult(name, (primary,), (reason,), primary)

    tags=[]; reasons=[]; blob=name+"\n"+summary
    if name in quarantined_ability_names(): tags.append("quarantine_named"); reasons.append("exact_quarantine_name")
    if ETHICS_NAME.search(name) or ETHICS_TEXT.search(blob): tags.append("ethics_reject"); reasons.append("ethics_pattern")
    if HIGH_RISK.search(name) or HIGH_RISK.search(summary): tags.append("high_risk"); reasons.append("high_risk_pattern")
    if NEEDS_HUMAN.search(name) or NEEDS_HUMAN.search(summary): tags.append("needs_human"); reasons.append("absolute_or_omni_language")
    blocking={"quarantine_named","ethics_reject","high_risk","needs_human"}
    if not summary and not set(tags)&blocking: tags.append("needs_human"); reasons.append("summary_missing")
    if not set(tags)&blocking:
        if STABILIZER.search(name) or STABILIZER.search(summary): tags.append("stabilizer"); reasons.append("stabilizer_pattern")
        if RESOURCE_POOL.search(name) or RESOURCE_POOL.search(summary): tags.append("resource_pool"); reasons.append("resource_pool_pattern")
        tags.append("map_ok"); reasons.append("nonempty_summary_no_blocking_tags")
    clean=tuple(dict.fromkeys(tag for tag in tags if tag in POLICY_TAGS))
    return ClassifyResult(name,clean,tuple(dict.fromkeys(reasons)),_primary(clean))
def apply_classification(entry:CatalogEntry,result:ClassifyResult,*,update_schema_hints:bool=True)->CatalogEntry:
    draft=entry.schema_draft
    if update_schema_hints and result.primary in STABILITY:
        draft=SchemaDraft(family=draft.family,stability=STABILITY[result.primary],growth_tag=GROWTH[result.primary],subject_domains=draft.subject_domains,effects_hint=dict(draft.effects_hint),physics_analog=draft.physics_analog)
    return CatalogEntry(name=entry.name,url=entry.url,category_path=entry.category_path,letter_bucket=entry.letter_bucket,source_license=entry.source_license,attribution=entry.attribution,fanon=entry.fanon,summary=entry.summary,schema_draft=draft,policy_tags=result.tags,walk=entry.walk)
def classify_index(store:CatalogStore,*,write:bool=True,names:Iterable[str]|None=None,update_schema_hints:bool=True)->tuple[ClassifyReport,list[ClassifyResult]]:
    allow={name.casefold() for name in names} if names is not None else None; results=[]; out=[]; updated=0; counts={}
    for entry in store.load_index():
        if allow is not None and entry.name.casefold() not in allow: out.append(entry); continue
        result=classify_entry(entry); results.append(result); counts[result.primary]=counts.get(result.primary,0)+1
        new=apply_classification(entry,result,update_schema_hints=update_schema_hints)
        if new.policy_tags!=entry.policy_tags or (update_schema_hints and new.schema_draft.stability!=entry.schema_draft.stability): updated+=1
        out.append(new)
    if write: store.save_index(sorted(out,key=lambda entry:entry.name.casefold()))
    return ClassifyReport(len(results),updated,counts),results
