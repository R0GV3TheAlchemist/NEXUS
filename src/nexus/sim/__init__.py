"""Compatibility shim for the lightweight simulation helper.

Canonical simulation package: ``nexus.simulation`` (see DECISIONS.md).

This package remains only to support ``nexus.app.entrypoint`` until that
consumer is migrated. Do not add new public APIs here.
"""

from .engine import SimulationEngine
from .state import SimulationState

__all__ = ["SimulationEngine", "SimulationState"]
