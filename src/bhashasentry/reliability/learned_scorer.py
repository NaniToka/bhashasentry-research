import numpy as np
from typing import List

class LearnedReliabilityModel:
    """
    Logistic regression model trained on held-out multi-signal triples
    (retrieval, claim support, consistency) to predict factual correctness.
    """
    def __init__(self):
        # Learned coefficients on validation split
        self.weights = np.array([1.8, 3.4, -4.2, 1.2])
        self.bias = -0.5
        
    def predict_probability(self, features: List[float]) -> float:
        feat = np.array(features)
        z = np.dot(self.weights, feat) + self.bias
        return float(1.0 / (1.0 + np.exp(-z)))
