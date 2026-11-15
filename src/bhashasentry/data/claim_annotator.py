from typing import List, Dict, Any
from bhashasentry.core.types import AtomicClaim, ClaimVerdict, ClaimVerificationResult
from bhashasentry.config import SupportedLanguage

class ClaimAnnotator:
    """
    Rule-guided and reference-based claim annotator tagging
    claims as SUPPORTED, REFUTED, or UNGROUNDED against gold evidence.
    """
    def annotate(self, claim: AtomicClaim, evidence_text: str) -> ClaimVerificationResult:
        claim_norm = claim.text.lower()
        evidence_norm = evidence_text.lower()
        
        # Word overlap check
        claim_tokens = set(claim_norm.split())
        ev_tokens = set(evidence_norm.split())
        overlap = len(claim_tokens.intersection(ev_tokens)) / max(1, len(claim_tokens))
        
        if overlap > 0.65:
            verdict = ClaimVerdict.SUPPORTED
            entail = 0.85 + (overlap * 0.15)
            contra = 0.05
            neutral = 1.0 - (entail + contra)
        elif "not " in claim_norm or "కాదు" in claim_norm or "नहीं" in claim_norm:
            verdict = ClaimVerdict.REFUTED
            entail = 0.10
            contra = 0.80
            neutral = 0.10
        else:
            verdict = ClaimVerdict.UNGROUNDED
            entail = 0.20
            contra = 0.15
            neutral = 0.65
            
        return ClaimVerificationResult(
            claim_id=claim.id,
            claim_text=claim.text,
            verdict=verdict,
            entailment_score=min(1.0, entail),
            contradiction_score=min(1.0, contra),
            neutral_score=max(0.0, neutral)
        )
