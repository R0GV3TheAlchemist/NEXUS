from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PolicySchema:
    name: str
    description: str = ""
    allow: List[str] = field(default_factory=list)
    deny: List[str] = field(default_factory=list)
    role: Optional[str] = None
    guards: List[str] = field(default_factory=list)
    conditions: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "allow": list(self.allow),
            "deny": list(self.deny),
            "role": self.role,
            "guards": list(self.guards),
            "conditions": dict(self.conditions),
            "metadata": dict(self.metadata),
        }


def normalize_policy(policy: Dict[str, Any]) -> PolicySchema:
    return PolicySchema(
        name=policy.get("name", "default"),
        description=policy.get("description", ""),
        allow=policy.get("allow", []) or [],
        deny=policy.get("deny", []) or [],
        role=policy.get("role"),
        guards=policy.get("guards", []) or [],
        conditions=policy.get("conditions", {}) or {},
        metadata=policy.get("metadata", {}) or {},
    )
