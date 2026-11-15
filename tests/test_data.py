import unittest
from bhashasentry.data.dataset_loader import DatasetLoader
from bhashasentry.data.benchmark_curator import BenchmarkCurator
from bhashasentry.core.types import AtomicClaim
from bhashasentry.config import SupportedLanguage
from bhashasentry.data.claim_annotator import ClaimAnnotator

class TestDatasetLoader(unittest.TestCase):
    def setUp(self):
        self.loader = DatasetLoader()
        self.curator = BenchmarkCurator()
        self.annotator = ClaimAnnotator()
        
    def test_load_benchmark(self):
        data = self.loader.load_gold_benchmark()
        self.assertGreaterEqual(len(data), 2)
        stats = self.curator.validate_split_integrity(data)
        self.assertIn("te", stats["language_counts"])
        self.assertGreater(stats["claims_by_verdict"]["SUPPORTED"], 0)

    def test_claim_annotation(self):
        claim = AtomicClaim(
            id="c_test",
            text="Chandrayaan-3 soft landed on 23 August 2023",
            language=SupportedLanguage.EN
        )
        evidence = "Chandrayaan-3 achieved a soft landing on 23 August 2023 near the lunar south pole."
        res = self.annotator.annotate(claim, evidence)
        self.assertEqual(res.verdict.value, "SUPPORTED")
        self.assertGreater(res.entailment_score, 0.7)

if __name__ == "__main__":
    unittest.main()
