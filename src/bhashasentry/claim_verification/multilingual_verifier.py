from typing import List
from bhashasentry.core.types import AtomicClaim, Passage, ClaimVerificationResult
from bhashasentry.claim_verification.nli_verifier import CrossLingualNLIVerifier

class MultilingualBatchClaimVerifier:
    """
    Executes claim verification over sets of atomic claims across multiple languages.
    """
    def __init__(self):
        self.nli = CrossLingualNLIVerifier()
        
    def verify_all(self, claims: List[AtomicClaim], passages: List[Passage]) -> List[ClaimVerificationResult]:
        return [self.nli.verify(c, passages) for c in claims]
