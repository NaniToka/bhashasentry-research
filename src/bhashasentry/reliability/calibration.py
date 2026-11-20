import math
from typing import List, Tuple

class ReliabilityCalibrator:
    """
    Platt Scaling and Brier Score evaluation for probability calibration.
    """
    def compute_brier_score(self, probs: List[float], labels: List[int]) -> float:
        if not probs or len(probs) != len(labels):
            return 0.0
        return sum((p - y) ** 2 for p, y in zip(probs, labels)) / len(probs)
