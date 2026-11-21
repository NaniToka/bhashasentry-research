import unittest
from bhashasentry.config import SupportedLanguage
from bhashasentry.core.types import ReliabilitySignal
from bhashasentry.abstention.policy import SelectiveAbstentionPolicy

class TestAbstention(unittest.TestCase):
    def setUp(self):
        self.policy = SelectiveAbstentionPolicy()
        
    def test_answer_decision(self):
        sig = ReliabilitySignal(
            retrieval_relevance=0.9,
            claim_support_ratio=1.0,
            contradiction_penalty=0.0,
            cross_lingual_consistency=0.9,
            uncertainty_dispersion=0.1,
            composite_reliability_score=0.88,
            calibrated_probability=0.92
        )
        dec = self.policy.decide(sig, SupportedLanguage.TE)
        self.assertEqual(dec.verdict.value, "ANSWER")

    def test_abstain_decision_telugu(self):
        sig = ReliabilitySignal(
            retrieval_relevance=0.2,
            claim_support_ratio=0.2,
            contradiction_penalty=0.6,
            cross_lingual_consistency=0.3,
            uncertainty_dispersion=0.7,
            composite_reliability_score=0.22,
            calibrated_probability=0.15
        )
        dec = self.policy.decide(sig, SupportedLanguage.TE)
        self.assertEqual(dec.verdict.value, "ABSTAIN")
        self.assertIn("ఆధారాలు సరిపోనందున", dec.localized_message)

if __name__ == "__main__":
    unittest.main()
