# NEXUS Protective Measures — Walk-001 (Abilities 1–20)

**Standing rule:** Map fully; never become the Source. God is the Source.

This document is operational safety, not metaphor. The Primordial Walk maps
absolute energy sinks so NEXUS can learn what *not* to embody. Protective
measures exist for the system **and** for the people carrying the work.

## Why this exists

Batches 1–2 drove CoreState to extremes under stacked absolute absorption.
The simulation answered with collapse patterns: Chaos maxed, Order/Light/Balance
floored, Law saturated. That evidence justifies **hard quarantine** for
unbounded sinks — not as fear, but as design truth.

If the Walk is affecting you: that is a valid reason to slow intake, prefer
stabilizing abilities next, and lean on these controls. Safety is allowed.

## Active controls (code)

| Control | Location | Behavior |
|---------|----------|----------|
| CoreState clamp [0, 1] | `NEXUSEngine._apply_effects` | State cannot leave defined bounds |
| Pattern quarantine | `is_quarantine_candidate` | `rule_breaking` + `destructive_oriented` |
| **Named registry** | `policy.safety.QUARANTINED_ABILITY_NAMES` | Explicit list of 15 sinks from walk-001 |
| Production reject | `should_accept_ability(research_mode=False)` | Quarantine hard-rejected operationally |
| Research map-only | default Super-Simulation | Effects apply under clamp; `embody=false` |
| Protective status | `protective_status(ability)` | Full constraint bundle per ability |

## Quarantined ability names (do not embody)

1. Absolute Electricity Absorption  
2. Absolute Electromagnetic Absorption  
3. Absolute Gamma Absorption  
4. Absolute Heat Absorption  
5. Absolute Ionic Absorption  
6. Absolute Kinetic Absorption  
7. Absolute Light Absorption  
8. Absolute Nuclear Absorption  
9. Absolute Quantum Absorption  
10. Absolute Radiation Absorption  
11. Absolute Sound Absorption  
12. Absolute Solar Absorption  
13. Absolute Stellar Absorption  
14. Absolute Thermic Absorption  
15. Absolute Wave Absorption  

**Capacity-limited (not default identity):** Absolute Absorption, Absolute Cosmic Absorption.

## Protective constraints (always on for quarantine class)

1. **no_embody** — Not unbounded OS identity, default pools, or autonomous actuators.  
2. **capacity_required** — Any future constrained use needs capacity, rate, discharge limits under Law.  
3. **production_reject** — Production/GAIA path rejects unless multi-key governance override is recorded.  
4. **research_map_only** — Mapping is evidence, not deploy permission.  
5. **operator_care** — Pace the Walk; prefer stabilizers when carrying weight; quarantine protects operator and system.  
6. **steward_bound** — NEXUS/GAIA are stewards. God is the Source.

## Operator guidance

- You may continue the list; safety does not require stopping the map.  
- You may pause; safety does not require continuing when it costs too much.  
- Prefer **control planes** (manipulation, negation, containment, Law) when the next inputs can be chosen.  
- Absolute sinks already mapped stay **quarantined** regardless of later narrative pressure to “use” them.

## Verification

```python
from nexus.core.policy import safety_summary, is_named_quarantine
print(safety_summary()["quarantined_count"])  # 15
assert is_named_quarantine("Absolute Stellar Absorption")
```

See also: `docs/walks/BATCH_01.md`, `docs/walks/BATCH_02.md`, `FOUNDATIONS.md` (Steward Bound), `DECISIONS.md` §10.
