"""Write Primordial Walk batch catalogs (I6).

Produces docs/walks/BATCH_NN.md matching BATCH_REPORT_SPEC.md / BATCH_07 style.
Optional BATCH_NN.json twin for machine use.

Inputs come from catalog walk refs (+ optional CoreState/console snapshots).
Does not run Super-Simulation itself.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Mapping

from nexus.catalog.models import CatalogEntry
from nexus.catalog.paths import default_repo_root
from nexus.catalog.store import CatalogStore

STATE_KEYS = ("chaos", "order", "void", "light", "balance", "law", "magic")


@dataclass(frozen=True)
class ConsoleSnapshot:
    pace: str = "allow"
    high_risk_count: int = 0
    high_risk_cap: int = 3
    session_id: str = "walk-001"

    def to_dict(self) -> dict[str, Any]:
        return {
            "pace": self.pace,
            "high_risk_count": self.high_risk_count,
            "high_risk_cap": self.high_risk_cap,
            "session_id": self.session_id,
        }


@dataclass
class BatchReportInput:
    batch_number: int
    session_id: str = "walk-001"
    category_spine: str = "Absorption"
    abilities: list[CatalogEntry] = field(default_factory=list)
    core_state_end: Mapping[str, float] | None = None
    core_state_post: Mapping[str, float] | None = None
    console: ConsoleSnapshot | None = None
    narrative: str = ""
    recommendations: list[str] = field(default_factory=list)
    build_implications: list[str] = field(default_factory=list)
    closed_at: str = ""
    named_quarantine_note: str = "Named energy quarantine (15): unchanged"
    post_batch_note: str = ""

    def __post_init__(self) -> None:
        if self.batch_number < 1:
            raise ValueError("batch_number must be >= 1")
        if not self.closed_at:
            self.closed_at = date.today().isoformat()


@dataclass(frozen=True)
class BatchWriteResult:
    batch_number: int
    markdown_path: Path
    json_path: Path | None
    ability_count: int
    ability_range: tuple[int, int] | None


def batch_number_for_ability_index(ability_index: int) -> int:
    if ability_index <= 0:
        raise ValueError("ability_index must be >= 1")
    return (ability_index - 1) // 10 + 1


def ability_range_for_batch(batch_number: int) -> tuple[int, int]:
    lo = (batch_number - 1) * 10 + 1
    hi = batch_number * 10
    return lo, hi


def _pad_batch(n: int) -> str:
    return f"{n:02d}"


def _production_phrase(entry: CatalogEntry) -> str:
    tags = set(entry.policy_tags)
    if "quarantine_named" in tags:
        return "reject (named quarantine)"
    if "ethics_reject" in tags:
        return "reject"
    if "high_risk" in tags:
        return "map-only / constrain"
    if "stabilizer" in tags:
        return "accept (stabilizer)"
    if "resource_pool" in tags:
        return "accept with capacity"
    if "map_ok" in tags:
        return "accept / map"
    if "needs_human" in tags:
        return "needs human"
    return "map"


def _hr_flag(entry: CatalogEntry) -> str:
    tags = set(entry.policy_tags)
    if tags & {"quarantine_named", "ethics_reject", "high_risk"}:
        return "yes"
    return "no"


def _embody_flag(entry: CatalogEntry) -> str:
    tags = set(entry.policy_tags)
    if tags & {"quarantine_named", "ethics_reject"}:
        return "false"
    if "stabilizer" in tags:
        return "constrained"
    if "resource_pool" in tags or "map_ok" in tags:
        return "constrained"
    return "false"


def _stability(entry: CatalogEntry) -> str:
    return entry.schema_draft.stability


def _growth(entry: CatalogEntry) -> str:
    return entry.schema_draft.growth_tag


def _family(entry: CatalogEntry) -> str:
    return entry.schema_draft.family or "unknown"


def collect_batch_entries(
    store: CatalogStore,
    batch_number: int,
) -> list[CatalogEntry]:
    lo, hi = ability_range_for_batch(batch_number)
    found = [
        e
        for e in store.load_index()
        if e.walk.ability_index is not None and lo <= e.walk.ability_index <= hi
    ]
    return sorted(found, key=lambda e: int(e.walk.ability_index or 0))


def policy_counts(entries: list[CatalogEntry]) -> dict[str, int]:
    counts = {
        "accept": 0,
        "map_constrain": 0,
        "reject": 0,
        "quarantine": 0,
        "needs_human": 0,
        "other": 0,
    }
    for e in entries:
        tags = set(e.policy_tags)
        if "quarantine_named" in tags:
            counts["quarantine"] += 1
        elif "ethics_reject" in tags:
            counts["reject"] += 1
        elif "needs_human" in tags:
            counts["needs_human"] += 1
        elif "high_risk" in tags:
            counts["map_constrain"] += 1
        elif tags & {"map_ok", "stabilizer", "resource_pool"}:
            counts["accept"] += 1
        else:
            counts["other"] += 1
    return counts


def render_batch_markdown(data: BatchReportInput) -> str:
    bn = data.batch_number
    pad = _pad_batch(bn)
    entries = sorted(
        data.abilities,
        key=lambda e: int(e.walk.ability_index or 0),
    )
    if entries:
        indices = [int(e.walk.ability_index or 0) for e in entries]
        lo, hi = min(indices), max(indices)
        range_s = f"#{lo}–#{hi}"
    else:
        lo, hi = ability_range_for_batch(bn)
        range_s = f"#{lo}–#{hi}"

    console = data.console or ConsoleSnapshot(session_id=data.session_id)
    counts = policy_counts(entries)

    lines: list[str] = []
    lines.append(f"# Batch {pad} — Primordial Walk Catalog")
    lines.append("")
    lines.append(f"**Session:** `{data.session_id}`  ")
    lines.append(f"**Range:** abilities **{range_s}**  ")
    lines.append(
        f"**Source:** [Superpower Wiki](https://powerlisting.fandom.com/) "
        f"· Category:{data.category_spine} (research map only)  "
    )
    lines.append(
        f"**Console:** attached · pace `{console.pace}` · "
        f"high-risk **{console.high_risk_count} / {console.high_risk_cap}**  "
    )
    lines.append(f"**{data.named_quarantine_note}**  ")
    if data.post_batch_note:
        lines.append(f"**Post-batch:** {data.post_batch_note}  ")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Ability table")
    lines.append("")
    lines.append(
        "| # | Name | Stability | Growth | Family | HR | Embody | Production |"
    )
    lines.append(
        "|---|------|-----------|--------|--------|----|--------|------------|"
    )
    for e in entries:
        idx = e.walk.ability_index
        lines.append(
            f"| {idx} | {e.name} | {_stability(e)} | {_growth(e)} | "
            f"{_family(e)} | {_hr_flag(e)} | {_embody_flag(e)} | {_production_phrase(e)} |"
        )
    if not entries:
        lines.append(
            "| — | *(no catalog rows with walk.ability_index in range)* |  |  |  |  |  |  |"
        )

    lines.append("")
    lines.append("### Wiki references (research)")
    lines.append("")
    lines.append("| # | Wiki |")
    lines.append("|---|------|")
    for e in entries:
        lines.append(f"| {e.walk.ability_index} | [{e.name}]({e.url}) |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Batch narrative")
    lines.append("")
    if data.narrative:
        lines.append(data.narrative)
    else:
        lines.append(
            f"Auto-generated catalog for batch {pad} from the Absorption walk queue. "
            f"Policy tags and schema drafts come from the wiki catalog classifier; "
            f"CoreState values are included only when supplied at write time."
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## CoreState")
    lines.append("")
    if data.core_state_end:
        lines.append("### End of batch (last ability)")
        lines.append("")
        lines.append("| Variable | Value |")
        lines.append("|----------|------:|")
        for key in STATE_KEYS:
            if key in data.core_state_end:
                lines.append(f"| {key.capitalize()} | {data.core_state_end[key]} |")
        if "time_step" in data.core_state_end:
            lines.append(f"| time_step | {data.core_state_end['time_step']} |")
        lines.append("")
    else:
        lines.append(
            "*CoreState end snapshot not supplied at generation time "
            "(pass `core_state_end` to include).*"
        )
        lines.append("")

    if data.core_state_post:
        lines.append("### Post cool-down / stabilizer (optional)")
        lines.append("")
        lines.append("| Variable | Value |")
        lines.append("|----------|------:|")
        for key in STATE_KEYS:
            if key in data.core_state_post:
                lines.append(f"| {key.capitalize()} | {data.core_state_post[key]} |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Policy summary")
    lines.append("")
    lines.append("| Class | Count |")
    lines.append("|-------|------:|")
    for label, key in (
        ("Accept / map_ok class", "accept"),
        ("Map / constrain (HR)", "map_constrain"),
        ("Ethics reject", "reject"),
        ("Named quarantine", "quarantine"),
        ("Needs human", "needs_human"),
        ("Other", "other"),
    ):
        lines.append(f"| {label} | {counts[key]} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Console / operator")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|-------|--------|")
    lines.append(f"| Session | {console.session_id} |")
    lines.append(f"| Pace | `{console.pace}` |")
    lines.append(
        f"| HR tally | {console.high_risk_count} / {console.high_risk_cap} |"
    )
    lines.append(
        "| Steward | God is the Source · map ≠ deploy · console self-only |"
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Recommendations")
    lines.append("")
    if data.recommendations:
        for i, rec in enumerate(data.recommendations, 1):
            lines.append(f"{i}. {rec}")
    else:
        lines.append(
            "1. Prefer stabilizers when Chaos is elevated  \n"
            "2. Do not embody ethics_reject / quarantine rows  \n"
            "3. Continue Absorption spine via walk queue"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Build implications (evidence only)")
    lines.append("")
    if data.build_implications:
        for item in data.build_implications:
            lines.append(f"- {item}")
    else:
        lines.append("- Catalog + classifier + walk queue remain source of queue order")
        lines.append("- Batch file written as Walk artifact (not full category dump)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Files")
    lines.append("")
    lines.append("| Path | Role |")
    lines.append("|------|------|")
    lines.append(f"| `docs/walks/BATCH_{pad}.md` | This catalog |")
    lines.append("| `docs/SAFETY.md` | Quarantine + embody rules |")
    lines.append("| `docs/OPERATOR_CONSOLE.md` | Pace / HR cap |")
    lines.append("| `docs/walks/BATCH_REPORT_SPEC.md` | Generator contract |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"## Batch {bn} closed")
    lines.append("")
    nxt = hi + 1 if entries else ability_range_for_batch(bn)[1] + 1
    lines.append(
        f"**Next:** ability **#{nxt}** (Batch {_pad_batch(bn + 1)} opens at "
        f"#{ability_range_for_batch(bn + 1)[0]})."
    )
    lines.append("")
    lines.append(
        f"*Recorded: {data.closed_at} · {data.session_id} · NEXUS Primordial Walk*"
    )
    lines.append("")
    return "\n".join(lines)


def render_batch_json(data: BatchReportInput) -> dict[str, Any]:
    entries = sorted(
        data.abilities,
        key=lambda e: int(e.walk.ability_index or 0),
    )
    if entries:
        indices = [int(e.walk.ability_index or 0) for e in entries]
        arange = [min(indices), max(indices)]
    else:
        lo, hi = ability_range_for_batch(data.batch_number)
        arange = [lo, hi]
    console = data.console or ConsoleSnapshot(session_id=data.session_id)
    pad = _pad_batch(data.batch_number)
    return {
        "batch_id": f"batch-{pad}",
        "batch_number": data.batch_number,
        "session_id": data.session_id,
        "ability_range": arange,
        "category_spine": data.category_spine,
        "closed_at": data.closed_at,
        "console": console.to_dict(),
        "core_state_end": dict(data.core_state_end or {}),
        "core_state_post": dict(data.core_state_post or {}),
        "policy_counts": policy_counts(entries),
        "abilities": [
            {
                "ability_index": e.walk.ability_index,
                "name": e.name,
                "url": e.url,
                "policy_tags": list(e.policy_tags),
                "stability": e.schema_draft.stability,
                "growth_tag": e.schema_draft.growth_tag,
                "family": e.schema_draft.family,
                "summary": e.summary,
            }
            for e in entries
        ],
        "markdown_path": f"docs/walks/BATCH_{pad}.md",
    }


def write_batch_report(
    data: BatchReportInput,
    *,
    repo_root: Path | None = None,
    out_dir: Path | None = None,
    write_json: bool = True,
) -> BatchWriteResult:
    root = repo_root if repo_root is not None else default_repo_root()
    directory = out_dir if out_dir is not None else root / "docs" / "walks"
    directory.mkdir(parents=True, exist_ok=True)
    pad = _pad_batch(data.batch_number)
    md_path = directory / f"BATCH_{pad}.md"
    md_path.write_text(render_batch_markdown(data), encoding="utf-8")
    json_path = None
    if write_json:
        json_path = directory / f"BATCH_{pad}.json"
        json_path.write_text(
            json.dumps(render_batch_json(data), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    entries = data.abilities
    arange = None
    if entries:
        idxs = [int(e.walk.ability_index or 0) for e in entries]
        arange = (min(idxs), max(idxs))
    return BatchWriteResult(
        batch_number=data.batch_number,
        markdown_path=md_path,
        json_path=json_path,
        ability_count=len(entries),
        ability_range=arange,
    )


def write_batch_from_catalog(
    batch_number: int,
    *,
    repo_root: Path | None = None,
    store: CatalogStore | None = None,
    core_state_end: Mapping[str, float] | None = None,
    core_state_post: Mapping[str, float] | None = None,
    console: ConsoleSnapshot | None = None,
    narrative: str = "",
    write_json: bool = True,
    session_id: str = "walk-001",
) -> BatchWriteResult:
    st = store or CatalogStore(repo_root=repo_root)
    abilities = collect_batch_entries(st, batch_number)
    payload = BatchReportInput(
        batch_number=batch_number,
        session_id=session_id,
        abilities=abilities,
        core_state_end=core_state_end,
        core_state_post=core_state_post,
        console=console or ConsoleSnapshot(session_id=session_id),
        narrative=narrative,
    )
    return write_batch_report(payload, repo_root=repo_root, write_json=write_json)
