from typing import Dict, List
import numpy as np
from bhashasentry.config import SupportedLanguage
from bhashasentry.consistency.cross_lingual_parity import CrossLingualParityEvaluator

class PairwiseConsistencyMatrix:
    """
    Generates a 6x6 pairwise consistency matrix quantifying factual agreement
    across English, Hindi, Telugu, Tamil, Bengali, and Marathi.
    """
    def __init__(self):
        self.evaluator = CrossLingualParityEvaluator()
        self.langs = [
            SupportedLanguage.EN,
            SupportedLanguage.HI,
            SupportedLanguage.TE,
            SupportedLanguage.TA,
            SupportedLanguage.BN,
            SupportedLanguage.MR
        ]
        
    def compute_matrix(self, parallel_answers: Dict[SupportedLanguage, str]) -> List[List[float]]:
        n = len(self.langs)
        matrix = [[1.0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                li, lj = self.langs[i], self.langs[j]
                ans_i = parallel_answers.get(li, "")
                ans_j = parallel_answers.get(lj, "")
                res = self.evaluator.evaluate_pair("matrix_eval", ans_i, li, ans_j, lj)
                score = round(res.mutual_entailment, 3)
                matrix[i][j] = score
                matrix[j][i] = score
                
        return matrix
