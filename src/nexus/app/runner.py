from typing import Any, Dict

from .entrypoint import NexusApp


class NexusRunner:
    def __init__(self):
        self.app = NexusApp()

    def run(self, principal: Dict[str, Any], ability_payload: Dict[str, Any], policy: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return self.app.submit(principal, ability_payload, policy)


def run_ability(principal: Dict[str, Any], ability_payload: Dict[str, Any], policy: Dict[str, Any] | None = None) -> Dict[str, Any]:
    return NexusRunner().run(principal, ability_payload, policy)
