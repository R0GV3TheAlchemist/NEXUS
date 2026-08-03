"""Canonical NEXUS simulation package.

This is the single public simulation architecture path. New Super-Simulation
and Primordial Walk work must land here. See DECISIONS.md and STATUS.md.
"""

from .engine import NEXUSEngine

__all__ = ["NEXUSEngine"]
