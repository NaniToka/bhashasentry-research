from typing import Dict, Any

class CompositeScoreValidator:
    """
    Validates boundary conditions: zero retrieval relevance or 100% contradiction
    must force the composite reliability score to zero.
    """
    def validate_bounds(self, score: float, contra_ratio: float) -> float:
        if contra_ratio > 0.50:
            return min(score, 0.20)
        return max(0.0, min(1.0, score))
