from typing import List, Optional
from bhashasentry.core.types import ReliabilitySignal, ClaimVerificationResult, ClaimVerdict, Passage
from bhashasentry.config import BhashaSentryConfig

class TraceabilityReliabilityScorer:
    """
    Cross-Lingual Evidence Traceability & Reliability (CLETR) Joint Formulation:
    R(q, a, E) = w_ret * S_ret + w_sup * S_sup - w_contra * S_contra + w_cons * S_cons
    """
    def __init__(self, config: Optional[BhashaSentryConfig] = None):
        self.config = config or BhashaSentryConfig()
        
    def compute_reliability(
        self,
        retrieval_score: float,
        verifications: List[ClaimVerificationResult],
        consistency_score: float = 0.85,
        uncertainty: float = 0.15
    ) -> ReliabilitySignal:
        total_claims = max(1, len(verifications))
        supported_count = sum(1 for v in verifications if v.verdict == ClaimVerdict.SUPPORTED)
        refuted_count = sum(1 for v in verifications if v.verdict == ClaimVerdict.REFUTED)
        
        sup_ratio = supported_count / total_claims
        contra_penalty = refuted_count / total_claims
        
        # Weighted linear combination
        raw_score = (
            self.config.weight_retrieval * retrieval_score +
            self.config.weight_support * sup_ratio -
            self.config.weight_contradiction * contra_penalty +
            self.config.weight_consistency * consistency_score
        )
        
        bounded_score = max(0.0, min(1.0, raw_score))
        
        # Logistic calibration approximation
        # P(correct | score) = 1 / (1 + exp(-5 * (score - 0.5)))
        import math
        calibrated_p = 1.0 / (1.0 + math.exp(-6.0 * (bounded_score - 0.45)))
        
        return ReliabilitySignal(
            retrieval_relevance=round(retrieval_score, 4),
            claim_support_ratio=round(sup_ratio, 4),
            contradiction_penalty=round(contra_penalty, 4),
            cross_lingual_consistency=round(consistency_score, 4),
            uncertainty_dispersion=round(uncertainty, 4),
            composite_reliability_score=round(bounded_score, 4),
            calibrated_probability=round(calibrated_p, 4)
        )
