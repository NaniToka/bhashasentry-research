import unittest
from bhashasentry.config import SupportedLanguage
from bhashasentry.core.types import Passage
from bhashasentry.pipeline import BhashaSentryPipeline

class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = BhashaSentryPipeline()
        self.passages = [
            Passage(id="p_test_1", text="Chandrayaan-3 landed on August 23, 2023.", language=SupportedLanguage.EN, is_gold=True),
            Passage(id="p_test_2", text="చంద్రయాన్-3 చంద్రుని దక్షిణ ధ్రువంపై దిగింది.", language=SupportedLanguage.TE, is_gold=True)
        ]
        self.pipeline.index_knowledge_base(self.passages)
        
    def test_pipeline_english(self):
        trace = self.pipeline.process_query("When did Chandrayaan-3 land on the Moon?", SupportedLanguage.EN)
        self.assertIsNotNone(trace.generated_answer)
        self.assertIn(trace.decision.verdict.value, ["ANSWER", "WARN", "ABSTAIN"])

    def test_pipeline_telugu(self):
        trace = self.pipeline.process_query("చంద్రయాన్-3 ఎప్పుడు దిగింది?", SupportedLanguage.TE)
        self.assertIsNotNone(trace.generated_answer)
        self.assertEqual(trace.query.language, SupportedLanguage.TE)

if __name__ == "__main__":
    unittest.main()
