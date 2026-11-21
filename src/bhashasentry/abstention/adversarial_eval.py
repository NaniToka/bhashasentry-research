from typing import Dict, Any
from bhashasentry.core.types import ReliabilitySignal
from bhashasentry.abstention.policy import SelectiveAbstentionPolicy
from bhashasentry.config import SupportedLanguage

class AdversarialAbstentionAuditor:
    """
    Tests abstention safety on completely unanswerable, out-of-domain,
    and adversarial distractor queries.
    """
    def test_unanswerable_query(self) -> Dict[str, Any]:
        policy = SelectiveAbstentionPolicy()
        fake_signal = ReliabilitySignal(
            retrieval_relevance=0.15,
            claim_support_ratio=0.10,
            contradiction_penalty=0.80,
            cross_lingual_consistency=0.20,
            uncertainty_dispersion=0.85,
            composite_reliability_score=0.12,
            calibrated_probability=0.08
        )
        dec = policy.decide(fake_signal, SupportedLanguage.TE)
        return {
            "verdict": dec.verdict.value,
            "abstained": dec.verdict.value == "ABSTAIN",
            "message": dec.localized_message
        }
