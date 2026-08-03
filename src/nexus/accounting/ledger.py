from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Ledger:
    entries: List[Dict[str, Any]] = field(default_factory=list)

    def record(self, actor: str, action: str, outcome: str, reason: str = "", signature: str = "") -> Dict[str, Any]:
        entry = {
            "actor": actor,
            "action": action,
            "outcome": outcome,
            "reason": reason,
            "signature": signature,
        }
        self.entries.append(entry)
        return entry

    def last(self) -> Dict[str, Any] | None:
        return self.entries[-1] if self.entries else None

    def snapshot(self) -> List[Dict[str, Any]]:
        return list(self.entries)
