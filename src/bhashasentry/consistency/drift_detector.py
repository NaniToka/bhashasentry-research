from typing import List, Dict, Any
from bhashasentry.config import SupportedLanguage
from bhashasentry.consistency.cross_lingual_parity import CrossLingualParityEvaluator

class CrossLingualFactualDriftEngine:
    """
    Detects factual drift across answers generated across all six languages.
    """
    def __init__(self):
        self.evaluator = CrossLingualParityEvaluator()
        
    def audit_query_answers(self, query_id: str, answers: Dict[SupportedLanguage, str]) -> List[Dict[str, Any]]:
        results = []
        langs = list(answers.keys())
        for i in range(len(langs)):
            for j in range(i + 1, len(langs)):
                la, lb = langs[i], langs[j]
                res = self.evaluator.evaluate_pair(query_id, answers[la], la, answers[lb], lb)
                results.append(res.model_dump())
        return results
