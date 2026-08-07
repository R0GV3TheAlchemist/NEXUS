"""Data models for the Superpower Wiki catalog (I1).

Boring, deterministic dataclasses with dict round-trip.
No network I/O. No CoreState side effects.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping

POLICY_TAGS: frozenset[str] = frozenset(
    {
        "quarantine_named",
        "ethics_reject",
        "high_risk",
        "stabilizer",
        "resource_pool",
        "map_ok",
        "needs_human",
    }
)

_STABILITY = frozenset({"stable", "conditionally_stable", "rule_breaking"})
_GROWTH = frozenset(
    {"growth_oriented", "context_dependent", "destructive_oriented"}
)
_WALK_STATUS = frozenset(
    {"pending", "applied", "skipped", "blocked", "side_queue"}
)


def _require_str(data: Mapping[str, Any], key: str) -> str:
    val = data.get(key)
    if not isinstance(val, str) or not val.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return val.strip()


@dataclass(frozen=True)
class SchemaDraft:
    """Draft AbilitySchema fields — hints only until Walk adjudicates."""

    family: str = "unknown"
    stability: str = "conditionally_stable"
    growth_tag: str = "context_dependent"
    subject_domains: tuple[str, ...] = ()
    effects_hint: Mapping[str, float] = field(default_factory=dict)
    physics_analog: str = ""

    def __post_init__(self) -> None:
        if self.stability not in _STABILITY:
            raise ValueError(f"invalid stability: {self.stability}")
        if self.growth_tag not in _GROWTH:
            raise ValueError(f"invalid growth_tag: {self.growth_tag}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "family": self.family,
            "stability": self.stability,
            "growth_tag": self.growth_tag,
            "subject_domains": list(self.subject_domains),
            "effects_hint": dict(self.effects_hint),
            "physics_analog": self.physics_analog,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> SchemaDraft:
        if not data:
            return cls()
        domains = data.get("subject_domains") or []
        effects = data.get("effects_hint") or {}
        if not isinstance(domains, (list, tuple)):
            raise ValueError("subject_domains must be a list")
        if not isinstance(effects, Mapping):
            raise ValueError("effects_hint must be a mapping")
        coerced = {
            str(k): float(v) for k, v in effects.items()
        }
        return cls(
            family=str(data.get("family") or "unknown"),
            stability=str(data.get("stability") or "conditionally_stable"),
            growth_tag=str(data.get("growth_tag") or "context_dependent"),
            subject_domains=tuple(str(d) for d in domains),
            effects_hint=coerced,
            physics_analog=str(data.get("physics_analog") or ""),
        )


@dataclass(frozen=True)
class WalkRef:
    """Optional link from a catalog row to a Primordial Walk apply."""

    status: str = "pending"
    ability_index: int | None = None
    batch_id: str | None = None
    session_id: str | None = None

    def __post_init__(self) -> None:
        if self.status not in _WALK_STATUS:
            raise ValueError(f"invalid walk status: {self.status}")
        if self.ability_index is not None and self.ability_index < 0:
            raise ValueError("ability_index must be >= 0")

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "ability_index": self.ability_index,
            "batch_id": self.batch_id,
            "session_id": self.session_id,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> WalkRef:
        if not data:
            return cls()
        idx = data.get("ability_index")
        if idx is not None:
            idx = int(idx)
        return cls(
            status=str(data.get("status") or "pending"),
            ability_index=idx,
            batch_id=data.get("batch_id"),
            session_id=data.get("session_id"),
        )


@dataclass(frozen=True)
class CatalogEntry:
    """One Superpower Wiki page row in the catalog."""

    name: str
    url: str
    category_path: tuple[str, ...] = ("Absorption",)
    letter_bucket: str = ""
    source_license: str = "CC-BY-SA"
    attribution: str = "Superpower Wiki contributors"
    fanon: bool = False
    summary: str = ""
    schema_draft: SchemaDraft = field(default_factory=SchemaDraft)
    policy_tags: tuple[str, ...] = ()
    walk: WalkRef = field(default_factory=WalkRef)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name is required")
        if not self.url.strip():
            raise ValueError("url is required")
        unknown = set(self.policy_tags) - POLICY_TAGS
        if unknown:
            raise ValueError(f"unknown policy_tags: {sorted(unknown)}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "url": self.url,
            "category_path": list(self.category_path),
            "letter_bucket": self.letter_bucket,
            "source_license": self.source_license,
            "attribution": self.attribution,
            "fanon": self.fanon,
            "summary": self.summary,
            "schema_draft": self.schema_draft.to_dict(),
            "policy_tags": list(self.policy_tags),
            "walk": self.walk.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CatalogEntry:
        path = data.get("category_path") or ["Absorption"]
        if not isinstance(path, (list, tuple)):
            raise ValueError("category_path must be a list")
        tags = data.get("policy_tags") or []
        if not isinstance(tags, (list, tuple)):
            raise ValueError("policy_tags must be a list")
        letter = str(data.get("letter_bucket") or "")
        if not letter and data.get("name"):
            letter = str(data["name"]).strip()[:1].upper()
        return cls(
            name=_require_str(data, "name"),
            url=_require_str(data, "url"),
            category_path=tuple(str(p) for p in path),
            letter_bucket=letter,
            source_license=str(data.get("source_license") or "CC-BY-SA"),
            attribution=str(
                data.get("attribution") or "Superpower Wiki contributors"
            ),
            fanon=bool(data.get("fanon", False)),
            summary=str(data.get("summary") or ""),
            schema_draft=SchemaDraft.from_dict(data.get("schema_draft")),
            policy_tags=tuple(str(t) for t in tags),
            walk=WalkRef.from_dict(data.get("walk")),
        )


@dataclass(frozen=True)
class CatalogCursor:
    """Category walk cursor — does not advance on stabilizer side-queue."""

    session_id: str
    category: str
    last_applied_name: str | None = None
    last_ability_index: int | None = None
    next_name: str | None = None
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CatalogCursor:
        idx = data.get("last_ability_index")
        if idx is not None:
            idx = int(idx)
        return cls(
            session_id=_require_str(data, "session_id"),
            category=_require_str(data, "category"),
            last_applied_name=data.get("last_applied_name"),
            last_ability_index=idx,
            next_name=data.get("next_name"),
            updated_at=str(data.get("updated_at") or ""),
        )
