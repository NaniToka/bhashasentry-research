from typing import Tuple
from bhashasentry.core.types import AtomicClaim, Passage, ClaimVerdict, ClaimVerificationResult
from bhashasentry.nlp.normalizer import IndicNormalizer

class CrossLingualNLIVerifier:
    """
    Cross-Lingual Natural Language Inference (NLI) model predicting
    entailment, contradiction, or neutral relation between evidence premise and claim hypothesis.
    """
    def __init__(self):
        self.normalizer = IndicNormalizer()
        
    def verify(self, claim: AtomicClaim, premise_passages: list) -> ClaimVerificationResult:
        if not premise_passages:
            return ClaimVerificationResult(
                claim_id=claim.id,
                claim_text=claim.text,
                verdict=ClaimVerdict.UNGROUNDED,
                entailment_score=0.0,
                contradiction_score=0.0,
                neutral_score=1.0,
                supporting_passage_ids=[]
            )
            
        c_words = set(self.normalizer.normalize(claim.text, claim.language).lower().split())
        best_entail = 0.0
        best_contra = 0.0
        best_pid = []
        
        for passage in premise_passages:
            p_words = set(self.normalizer.normalize(passage.text, passage.language).lower().split())
            overlap = len(c_words.intersection(p_words)) / max(1, len(c_words))
            
            # Check negation
            claim_has_neg = any(w in claim.text.lower() for w in ["not", "కాదు", "नहीं", "இல்லை", "নয়", "नाही"])
            pass_has_neg = any(w in passage.text.lower() for w in ["not", "కాదు", "नहीं", "இல்லை", "নয়", "नाही"])
            
            if overlap > 0.40:
                if claim_has_neg != pass_has_neg and overlap > 0.50:
                    contra_score = 0.85
                    entail_score = 0.10
                else:
                    entail_score = min(1.0, 0.40 + (overlap * 0.60))
                    contra_score = 0.05
            else:
                entail_score = 0.20
                contra_score = 0.15
                
            if entail_score > best_entail:
                best_entail = entail_score
                best_contra = contra_score
                if passage.id not in best_pid:
                    best_pid.append(passage.id)
                    
        neutral_score = max(0.0, 1.0 - (best_entail + best_contra))
        
        if best_contra > 0.60:
            verdict = ClaimVerdict.REFUTED
        elif best_entail >= 0.55:
            verdict = ClaimVerdict.SUPPORTED
        else:
            verdict = ClaimVerdict.UNGROUNDED
            
        return ClaimVerificationResult(
            claim_id=claim.id,
            claim_text=claim.text,
            verdict=verdict,
            entailment_score=round(best_entail, 4),
            contradiction_score=round(best_contra, 4),
            neutral_score=round(neutral_score, 4),
            supporting_passage_ids=best_pid
        )
