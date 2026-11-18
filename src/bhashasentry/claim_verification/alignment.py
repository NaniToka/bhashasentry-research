from typing import List, Dict, Any
from bhashasentry.core.types import AtomicClaim, Passage

class ClaimEvidenceAligner:
    """
    Calculates token-level and phrase-level semantic alignment
    between claim spans and evidence sentences.
    """
    def align(self, claim: AtomicClaim, passage: Passage) -> Dict[str, Any]:
        c_tokens = set(claim.text.lower().split())
        p_tokens = set(passage.text.lower().split())
        shared = c_tokens.intersection(p_tokens)
        return {
            "claim_id": claim.id,
            "passage_id": passage.id,
            "shared_tokens": list(shared),
            "coverage_ratio": len(shared) / max(1, len(c_tokens))
        }
