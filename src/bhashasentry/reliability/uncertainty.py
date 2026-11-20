import math
from typing import List

class UncertaintyEstimator:
    """
    Estimates predictive uncertainty via entropy and dispersion across candidate scores.
    """
    def compute_dispersion(self, candidate_scores: List[float]) -> float:
        if not candidate_scores or len(candidate_scores) == 1:
            return 0.0
        mean = sum(candidate_scores) / len(candidate_scores)
        variance = sum((s - mean) ** 2 for s in candidate_scores) / len(candidate_scores)
        return math.sqrt(variance)
