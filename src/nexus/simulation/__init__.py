"""Canonical NEXUS simulation package.

Public surface:
- ``NEXUSEngine`` — apply abilities to CoreState under policy
- ``CoreState`` / ``RunResult`` — state contract
- ``SuperSimulation`` / ``initialize_super_simulation`` — minimal Super-Simulation entrypoint

Shim package ``nexus.sim`` is not part of this public surface.
See DECISIONS.md and STATUS.md.
"""

from .engine import NEXUSEngine
from .state import CoreState, RunResult
from .super_simulation import SuperSimulation, initialize_super_simulation, primordial_baseline

__all__ = [
    "NEXUSEngine",
    "CoreState",
    "RunResult",
    "SuperSimulation",
    "initialize_super_simulation",
    "primordial_baseline",
]
