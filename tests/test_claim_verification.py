import unittest
from bhashasentry.config import SupportedLanguage
from bhashasentry.core.types import AtomicClaim, Passage
from bhashasentry.claim_verification.claim_extractor import AtomicClaimExtractor
from bhashasentry.claim_verification.nli_verifier import CrossLingualNLIVerifier

class TestClaimVerification(unittest.TestCase):
    def setUp(self):
        self.extractor = AtomicClaimExtractor()
        self.verifier = CrossLingualNLIVerifier()
        self.passages = [
            Passage(id="doc_1", text="Chandrayaan-3 landed near lunar south pole on August 23, 2023.", language=SupportedLanguage.EN)
        ]
        
    def test_claim_extraction(self):
        text = "Chandrayaan-3 was launched in July and it landed in August 2023."
        claims = self.extractor.extract_claims(text, SupportedLanguage.EN)
        self.assertGreaterEqual(len(claims), 1)

    def test_nli_support(self):
        claim = AtomicClaim(id="c1", text="Chandrayaan-3 landed on August 23, 2023.", language=SupportedLanguage.EN)
        res = self.verifier.verify(claim, self.passages)
        self.assertEqual(res.verdict.value, "SUPPORTED")
        self.assertGreater(res.entailment_score, 0.5)

if __name__ == "__main__":
    unittest.main()
