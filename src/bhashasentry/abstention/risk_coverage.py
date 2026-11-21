from typing import List, Dict, Any

class RiskCoverageOptimizer:
    """
    Computes Coverage-Risk curves across threshold sweeps.
    Coverage = Fraction of queries where system does not abstain.
    Risk = Error rate on answered queries.
    """
    def generate_curve(self, reliability_scores: List[float], is_correct: List[int]) -> List[Dict[str, float]]:
        curve = []
        for tau in [0.0, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
            answered = [y for s, y in zip(reliability_scores, is_correct) if s >= tau]
            cov = len(answered) / max(1, len(reliability_scores))
            if answered:
                risk = sum(1 for y in answered if y == 0) / len(answered)
            else:
                risk = 0.0
            curve.append({"threshold": tau, "coverage": round(cov, 4), "risk": round(risk, 4)})
        return curve
