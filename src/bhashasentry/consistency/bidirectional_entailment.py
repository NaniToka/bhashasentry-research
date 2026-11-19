from typing import Tuple

class BidirectionalEntailment:
    """
    Computes bidirectional entailment score between cross-lingual text representations.
    Score = (P(A entails B) + P(B entails A)) / 2.
    """
    def score(self, entail_ab: float, entail_ba: float) -> float:
        return (entail_ab + entail_ba) / 2.0
