from typing import List
from bhashasentry.core.types import ClaimVerificationResult, ClaimVerdict

class ContradictionDetector:
    """
    Detects hard factual contradictions between verified claims and context passages.
    """
    def detect_contradictions(self, verification_results: List[ClaimVerificationResult]) -> List[ClaimVerificationResult]:
        return [res for res in verification_results if res.verdict == ClaimVerdict.REFUTED]
