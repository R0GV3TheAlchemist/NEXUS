"""Named quarantine registry for catalog classification (I4).

Prefers QUARANTINED_ABILITY_NAMES from nexus.core.policy.safety when importable.
Fallback list covers the absolute energy / omni-sink class from early Walk batches.
Keep this aligned with docs/SAFETY.md.
"""

from __future__ import annotations

# Fallback if core.policy.safety is unavailable or empty.
_FALLBACK_QUARANTINED: frozenset[str] = frozenset(
    {
        "Absolute Absorption",
        "Absolute Energy Absorption",
        "Absolute Life-Force Absorption",
        "Absolute Superpower Absorption",
        "Omni-Absorption",
        "Omni Absorption",
        "Totality Absorption",
        "Reality Consumption",
        "Meta Space-Time Absorption",
        "Absolute Nuclear Absorption",
        "Absolute Stellar Absorption",
        "Absolute Solar Absorption",
        "Absolute Lunar Absorption",
        "Absolute Cosmic Absorption",
        "Absolute Darkness Absorption",
    }
)


def quarantined_ability_names() -> frozenset[str]:
    """Return exact-name quarantine set (case-sensitive wiki titles)."""
    try:
        from nexus.core.policy import safety as safety_mod  # type: ignore
    except Exception:
        return _FALLBACK_QUARANTINED

    for attr in (
        "QUARANTINED_ABILITY_NAMES",
        "QUARANTINE_NAMES",
        "NAMED_QUARANTINE",
    ):
        raw = getattr(safety_mod, attr, None)
        if raw:
            return frozenset(str(x) for x in raw)
    return _FALLBACK_QUARANTINED
