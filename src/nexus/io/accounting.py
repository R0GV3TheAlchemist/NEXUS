from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List
import json


@dataclass
class Ledger:
    entries: List[Dict[str, Any]] = field(default_factory=list)

    def add(self, entry: Dict[str, Any]) -> None:
        self.entries.append(entry)

    def save(self, path: str) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(self.entries, indent=2), encoding="utf-8")
