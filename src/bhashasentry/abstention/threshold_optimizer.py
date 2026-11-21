from typing import List, Tuple

class ThresholdOptimizer:
    """
    Optimizes decision boundaries (tau_answer, tau_warn) to maximize
    coverage subject to a maximum acceptable risk budget alpha (e.g. risk <= 5%).
    """
    def optimize_thresholds(self, scores: List[float], labels: List[int], max_risk: float = 0.05) -> Tuple[float, float]:
        # Grid search over candidate thresholds
        best_tau = 0.70
        for tau in [0.60, 0.65, 0.70, 0.75, 0.80, 0.85]:
            accepted = [(s, y) for s, y in zip(scores, labels) if s >= tau]
            if not accepted:
                continue
            risk = sum(1 - y for _, y in accepted) / len(accepted)
            if risk <= max_risk:
                best_tau = tau
                break
        return best_tau, max(0.40, best_tau - 0.25)
