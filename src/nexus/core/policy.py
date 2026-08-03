"""DEPRECATED — shadowed by the ``nexus.core.policy`` package directory.

Do not import this file. Use ``from nexus.core.policy import ...`` which
resolves to the package. Real acceptance/assessment lives in
``nexus.core.policy.assessment``. This file remains only to avoid broken
references during package discovery; it will be removed after Issue #3.
"""

from nexus.core.policy.assessment import assess_ability, should_accept_ability

__all__ = ["assess_ability", "should_accept_ability"]
