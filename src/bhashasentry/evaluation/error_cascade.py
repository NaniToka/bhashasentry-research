from typing import List, Dict, Any
from bhashasentry.core.types import AuditTrace

class ErrorPropagationAnalyzer:
    """
    Analyzes error cascade rates across the 6 pipeline stages:
    P(Fail_B | Fail_A), P(Fail_D | Fail_B), P(Abstain | Fail_D).
    """
    def analyze_cascade(self, traces: List[AuditTrace]) -> Dict[str, float]:
        if not traces:
            return {}
        total = len(traces)
        retrieval_errors = sum(1 for t in traces if t.reliability_signal.retrieval_relevance < 0.4)
        generation_errors = sum(1 for t in traces if t.reliability_signal.contradiction_penalty > 0.2)
        abstained = sum(1 for t in traces if t.decision.verdict.value == "ABSTAIN")
        
        return {
            "retrieval_error_rate": retrieval_errors / total,
            "generation_error_rate": generation_errors / total,
            "abstention_rate": abstained / total,
            "error_cascade_ratio": generation_errors / max(1, retrieval_errors)
        }
