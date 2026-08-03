from typing import Any, Dict

from .entrypoint import NexusApp


def process_ability(principal: Dict[str, Any], ability_payload: Dict[str, Any], policy: Dict[str, Any] | None = None) -> Dict[str, Any]:
    app = NexusApp()
    return app.submit(principal, ability_payload, policy)
