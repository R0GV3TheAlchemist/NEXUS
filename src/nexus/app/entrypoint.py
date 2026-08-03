from typing import Any, Dict

from nexus.core.ingestion import ingest_ability_payload
from nexus.core.policy.aaa import decide, account
from nexus.accounting.ledger import Ledger
from nexus.sim.engine import SimulationEngine


class NexusApp:
    def __init__(self):
        self.ledger = Ledger()
        self.engine = SimulationEngine()

    def submit(self, principal: Dict[str, Any], ability_payload: Dict[str, Any], policy: Dict[str, Any] | None = None) -> Dict[str, Any]:
        ingest_result = ingest_ability_payload(ability_payload)
        if not ingest_result["accepted"]:
            decision = decide(principal, "ingest_ability", ability_payload, policy)
            record = account(principal, "ingest_ability", "rejected", "validation_failed")
            self.ledger.record(record["actor"], record["action"], record["outcome"], record["reason"], record["signature"])
            self.engine.ingest(ability_payload, False, "validation_failed")
            return {"accepted": False, "validation": ingest_result, "decision": decision, "record": record}

        decision = decide(principal, "ingest_ability", ability_payload, policy)
        outcome = "approved" if decision.authorized and decision.accounted else "rejected"
        record = account(principal, "ingest_ability", outcome, decision.reason)
        self.ledger.record(record["actor"], record["action"], record["outcome"], record["reason"], record["signature"])
        self.engine.ingest(ingest_result["ability"] or ability_payload, decision.authorized and decision.accounted, decision.reason)
        return {"accepted": decision.authorized and decision.accounted, "validation": ingest_result, "decision": decision, "record": record, "state": self.engine.state.snapshot()}
