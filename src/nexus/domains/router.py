from typing import Any, Dict

from nexus.domains.physics.skeleton import get_domain_manifest as get_physics_manifest
from nexus.domains.cognition.skeleton import get_domain_manifest as get_cognition_manifest
from nexus.domains.metaphysics.skeleton import get_domain_manifest as get_metaphysics_manifest


DOMAIN_MANIFESTS = {
    "physics": get_physics_manifest,
    "cognition": get_cognition_manifest,
    "metaphysics": get_metaphysics_manifest,
}


def route_domain(ability: Dict[str, Any]) -> str:
    subject_domains = [d.lower() for d in ability.get("subject_domains", []) or []]
    if "physics" in subject_domains:
        return "physics"
    if "cognition" in subject_domains:
        return "cognition"
    if "metaphysics" in subject_domains:
        return "metaphysics"
    return "physics"


def load_domain_manifest(domain: str) -> Dict[str, Any]:
    loader = DOMAIN_MANIFESTS.get(domain, get_physics_manifest)
    return loader()
