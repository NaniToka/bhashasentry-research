from typing import List

class ExpectedCalibrationError:
    """
    Computes Expected Calibration Error (ECE) across M equally spaced probability bins.
    """
    def compute_ece(self, probs: List[float], labels: List[int], n_bins: int = 10) -> float:
        if not probs:
            return 0.0
            
        bins = [[] for _ in range(n_bins)]
        for p, y in zip(probs, labels):
            b_idx = min(n_bins - 1, int(p * n_bins))
            bins[b_idx].append((p, y))
            
        ece = 0.0
        n_total = len(probs)
        for b in bins:
            if not b:
                continue
            b_size = len(b)
            avg_prob = sum(x[0] for x in b) / b_size
            avg_acc = sum(x[1] for x in b) / b_size
            ece += (b_size / n_total) * abs(avg_acc - avg_prob)
            
        return round(ece, 4)
