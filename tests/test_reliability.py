import unittest
from bhashasentry.core.types import ClaimVerificationResult, ClaimVerdict
from bhashasentry.reliability.scorer import TraceabilityReliabilityScorer
from bhashasentry.reliability.ece import ExpectedCalibrationError

class TestReliability(unittest.TestCase):
    def setUp(self):
        self.scorer = TraceabilityReliabilityScorer()
        self.ece = ExpectedCalibrationError()
        
    def test_high_reliability(self):
        verifications = [
            ClaimVerificationResult(claim_id="c1", claim_text="Fact A", verdict=ClaimVerdict.SUPPORTED, entailment_score=0.9, contradiction_score=0.0, neutral_score=0.1)
        ]
        sig = self.scorer.compute_reliability(retrieval_score=0.9, verifications=verifications, consistency_score=0.9)
        self.assertGreater(sig.composite_reliability_score, 0.70)
        self.assertGreater(sig.calibrated_probability, 0.75)

    def test_low_reliability_with_refutation(self):
        verifications = [
            ClaimVerificationResult(claim_id="c2", claim_text="Fact B", verdict=ClaimVerdict.REFUTED, entailment_score=0.1, contradiction_score=0.9, neutral_score=0.0)
        ]
        sig = self.scorer.compute_reliability(retrieval_score=0.2, verifications=verifications, consistency_score=0.3)
        self.assertLess(sig.composite_reliability_score, 0.35)

    def test_ece_computation(self):
        probs = [0.9, 0.8, 0.3, 0.2]
        labels = [1, 1, 0, 0]
        val = self.ece.compute_ece(probs, labels, n_bins=5)
        self.assertLessEqual(val, 0.25)

if __name__ == "__main__":
    unittest.main()
