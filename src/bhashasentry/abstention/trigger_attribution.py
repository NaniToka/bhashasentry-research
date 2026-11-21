from bhashasentry.core.types import ReliabilitySignal

class AbstentionTriggerAttributor:
    """
    Identifies root causes triggering an abstention decision:
    - RETRIEVAL_EMPTY / RETRIEVAL_LOW
    - UNGROUNDED_CLAIMS
    - CONTRADICTORY_EVIDENCE
    - CROSS_LINGUAL_DISAGREEMENT
    """
    def attribute_cause(self, signal: ReliabilitySignal) -> str:
        if signal.retrieval_relevance < 0.40:
            return "RETRIEVAL_FAILURE: Insufficient knowledge retrieved."
        elif signal.contradiction_penalty > 0.30:
            return "CONTRADICTION: Generated answer directly conflicts with source evidence."
        elif signal.claim_support_ratio < 0.50:
            return "EVIDENCE_UTILIZATION: Claims lack factual grounding in retrieved text."
        elif signal.cross_lingual_consistency < 0.60:
            return "CROSS_LINGUAL_DRIFT: Inconsistent factual answers across languages."
        return "LOW_CONFIDENCE: Overall multi-signal score below reliable threshold."
