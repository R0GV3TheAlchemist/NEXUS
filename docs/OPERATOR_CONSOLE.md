# Creator Self-Control Console

**Scope:** Help the operator control *themselves* during the Primordial Walk.  
**Not in scope:** Control of other people, remote influence, replacing the Source.

Standing rule: Map fully; never become the Source. God is the Source.  
The console is a brake and a mirror, not a throne.

## Why it exists

Batches 1–2 showed that stacked absolute sinks collapse CoreState. Protective
measures quarantine those sinks. The operator still carries the Walk. This
console gives *you* explicit levers for pace, hold, capacity, and emergency
stop — so self-control is structural, not only intention.

## Levers

| Action | Effect |
|--------|--------|
| `set_pace("allow")` | Next ability may be ingested |
| `hold()` / `set_pace("hold")` | No ingest until released |
| `stabilizers_only()` | Prefer non-destructive / non-quarantine only |
| `engage_emergency_hold()` | Full stop until `clear_emergency_hold()` |
| `set_check_in(clear=True/False)` | Operator marks readiness (not a medical diagnosis) |
| `set_session_cap(n)` | Max high-risk maps per session (default 3) |
| `quarantine_board()` | Live list of protected sinks (`embody=false`) |
| `steward_reminder()` | Fixed steward text |

## Usage

```python
from nexus.operator import create_operator_console
from nexus.simulation import initialize_super_simulation

console = create_operator_console(session_id="walk-001")
sim = initialize_super_simulation()
sim.attach_console(console)  # gates ingest through may_ingest

console.set_check_in(clear=True, sober_self_report=True)
console.set_pace("allow")

# If weight is high:
console.stabilizers_only()
# or
console.engage_emergency_hold()
```

## Explicit forbids

- Control of others  
- Remote influence APIs  
- Unbounded embodiment of quarantined abilities  
- Claiming to be or replace the Source  

## Relation to safety

- `docs/SAFETY.md` — system quarantine for abilities 1–20  
- This console — operator self-regulation while mapping  

Both are required before Batch 3 (ability #21+).
