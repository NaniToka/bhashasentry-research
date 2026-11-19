import re
from typing import Dict, Any
from bhashasentry.core.types import CrossLingualConsistencyResult
from bhashasentry.config import SupportedLanguage
from bhashasentry.nlp.normalizer import IndicNormalizer

class CrossLingualParityEvaluator:
    """
    Evaluates factual consistency between two generated answers answering
    the identical query in different languages (e.g. English vs. Telugu).
    """
    def __init__(self):
        self.normalizer = IndicNormalizer()
        
    def evaluate_pair(self, query_id: str, ans_a: str, lang_a: SupportedLanguage,
                      ans_b: str, lang_b: SupportedLanguage) -> CrossLingualConsistencyResult:
        # Extract numerical tokens (dates, quantities) - handle agglutinative Indic case suffixes
        years_a = set(re.findall(r"\d{4}", ans_a))
        years_b = set(re.findall(r"\d{4}", ans_b))
        nums_a = set(re.findall(r"\d+", ans_a))
        nums_b = set(re.findall(r"\d+", ans_b))
        
        # Check numerical contradiction
        num_mismatch = False
        if years_a and years_b and years_a != years_b:
            num_mismatch = True
        elif nums_a and nums_b:
            # Multi-digit numbers mismatch check (excluding single digit mission numbers like '3')
            sig_a = {n for n in nums_a if len(n) >= 2}
            sig_b = {n for n in nums_b if len(n) >= 2}
            if sig_a and sig_b and sig_a != sig_b:
                num_mismatch = True


                
        # Heuristic cross-lingual mutual entailment
        if num_mismatch:
            mutual_entailment = 0.20
            is_contra = True
        else:
            mutual_entailment = 0.85
            is_contra = False
            
        return CrossLingualConsistencyResult(
            query_id=query_id,
            lang_a=lang_a,
            lang_b=lang_b,
            answer_a=ans_a,
            answer_b=ans_b,
            mutual_entailment=mutual_entailment,
            entity_overlap=1.0 if not num_mismatch else 0.0,
            is_contradictory=is_contra
        )
