import unittest
from bhashasentry.config import SupportedLanguage
from bhashasentry.core.types import Query, Passage
from bhashasentry.retrieval.bm25 import BM25Retriever
from bhashasentry.retrieval.dense import DenseMultilingualRetriever
from bhashasentry.retrieval.hybrid import HybridRRFRetriever

class TestRetrieval(unittest.TestCase):
    def setUp(self):
        self.passages = [
            Passage(id="p1", text="Chandrayaan-3 landed on the lunar south pole in August 2023.", language=SupportedLanguage.EN),
            Passage(id="p2", text="Mangalyaan orbited Mars in September 2014.", language=SupportedLanguage.EN),
            Passage(id="p3", text="చంద్రయాన్-3 చంద్రునిపై విజయవంతంగా దిగింది.", language=SupportedLanguage.TE)
        ]
        self.bm25 = BM25Retriever()
        self.dense = DenseMultilingualRetriever()
        self.hybrid = HybridRRFRetriever()
        
        self.bm25.index(self.passages)
        self.dense.index(self.passages)
        self.hybrid.index(self.passages)

    def test_bm25_retrieval(self):
        query = Query(id="q1", text="Chandrayaan-3 lunar landing", language=SupportedLanguage.EN)
        res = self.bm25.retrieve(query, top_k=2)
        self.assertGreater(len(res), 0)
        self.assertEqual(res[0][0].id, "p1")

    def test_hybrid_rrf(self):
        query = Query(id="q2", text="చంద్రయాన్-3 ల్యాండింగ్", language=SupportedLanguage.TE)
        res = self.hybrid.retrieve(query, top_k=2)
        self.assertGreater(len(res), 0)
        self.assertIn("p3", [r[0].id for r in res])

if __name__ == "__main__":
    unittest.main()
