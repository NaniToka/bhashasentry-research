import unittest
from bhashasentry.pipeline import BhashaSentryPipeline
from bhashasentry.config import SupportedLanguage
from bhashasentry.core.types import Passage

class TestFullRegression(unittest.TestCase):
    def test_complete_stack(self):
        pipe = BhashaSentryPipeline()
        p = Passage(id="doc_final", text="ISRO successfully launched Chandrayaan-3.", language=SupportedLanguage.EN, is_gold=True)
        pipe.index_knowledge_base([p])
        trace = pipe.process_query("చంద్రయాన్-3 ప్రయోగం గురించి చెప్పండి.", SupportedLanguage.TE)
        self.assertIsNotNone(trace.decision.verdict)
        self.assertGreaterEqual(trace.reliability_signal.composite_reliability_score, 0.0)

if __name__ == "__main__":
    unittest.main()
