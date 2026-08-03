"""Canonical NEXUS simulation package.

Public surface:
- ``NEXUSEngine`` — apply abilities to CoreState under policy
- ``CoreState`` / ``RunResult`` — state contract (re-exported for convenience)

Shim package ``nexus.sim`` is not part of this public surface.
See DECISIONS.md and STATUS.md.
"""

from .engine import NEXUSEngine
from .state import CoreState, RunResult

__all__ = ["NEXUSEngine", "CoreState", "RunResult"]
