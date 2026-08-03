"""Core policy package.

Canonical exports for AAA helpers and ability acceptance/assessment.
The legacy module ``nexus.core.policy`` (policy.py) is shadowed by this
package and should not be used; see DECISIONS.md simulation boundary notes.
"""

from .aaa import decide, account
from .assessment import (
    assess_ability,
    should_accept_ability,
    is_quarantine_candidate,
)

__all__ = [
    "decide",
    "account",
    "assess_ability",
    "should_accept_ability",
    "is_quarantine_candidate",
]
