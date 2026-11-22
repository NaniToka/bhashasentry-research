from typing import Dict, Any
from bhashasentry.core.types import AuditTrace, DecisionVerdict

class StageErrorAttributionEngine:
    """
    Quantifies the root error stage (Problems A through F) for failed or abstained instances:
    Problem A: Query understanding failure
    Problem B: Retrieval failure
    Problem C: Evidence utilization failure
    Problem D: Generation failure (hallucination)
    Problem E: Cross-lingual consistency failure
    Problem F: Reliability estimation failure
    """
    def attribute(self, trace: AuditTrace) -> str:
        if len(trace.retrieved_passages) == 0:
            return "Problem B: Retrieval Failure (Zero passages retrieved)"
        top_gold = any(p.is_gold for p in trace.retrieved_passages)
        if not top_gold:
            return "Problem B: Retrieval Failure (No gold passage in top-k)"
            
        contra_count = sum(1 for v in trace.claim_verifications if v.verdict.value == "REFUTED")
        if contra_count > 0:
            return "Problem D: Generation Failure (Hallucinated contradictory claims)"
            
        unsupported = sum(1 for v in trace.claim_verifications if v.verdict.value == "UNGROUNDED")
        if unsupported > 0:
            return "Problem C: Evidence Utilization Failure (Ungrounded claims introduced)"
            
        if trace.reliability_signal.cross_lingual_consistency < 0.60:
            return "Problem E: Cross-Lingual Consistency Failure"
            
        return "No Failure Attributed (Clean Execution)"
