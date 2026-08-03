"""Simulation state contract for the canonical package.

``CoreState`` is the single state vector for Super-Simulation / Primordial Walk
work (Chaos, Order, Void, Light, Balance, Law, Magic). This module re-exports
it so simulation consumers have one obvious import path:

    from nexus.simulation.state import CoreState
    from nexus.simulation import NEXUSEngine

Do not introduce a second parallel state type under ``nexus.simulation``.
The shim package ``nexus.sim.SimulationState`` remains only for the app
entrypoint ledger/time-step helper until that consumer is migrated.
"""

from nexus.core.models import CoreState, RunResult, Stability, GrowthTag

__all__ = ["CoreState", "RunResult", "Stability", "GrowthTag"]
