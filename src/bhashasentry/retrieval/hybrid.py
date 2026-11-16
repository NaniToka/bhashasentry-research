from typing import List, Tuple, Dict
from collections import defaultdict
from bhashasentry.retrieval.base import BaseRetriever
from bhashasentry.retrieval.bm25 import BM25Retriever
from bhashasentry.retrieval.dense import DenseMultilingualRetriever
from bhashasentry.core.types import Query, Passage

class HybridRRFRetriever(BaseRetriever):
    """
    Reciprocal Rank Fusion (RRF) combining Sparse BM25 and Dense Semantic Retrievers.
    Formula: RRF_score(d) = sum(1.0 / (k + rank_m(d))) for m in {bm25, dense}.
    """
    def __init__(self, k: int = 60, bm25_weight: float = 0.5, dense_weight: float = 0.5):
        self.k = k
        self.bm25_weight = bm25_weight
        self.dense_weight = dense_weight
        self.bm25 = BM25Retriever()
        self.dense = DenseMultilingualRetriever()
        self.passages: List[Passage] = []
        
    def index(self, passages: List[Passage]) -> None:
        self.passages = passages
        self.bm25.index(passages)
        self.dense.index(passages)

    def retrieve(self, query: Query, top_k: int = 5) -> List[Tuple[Passage, float]]:
        if not self.passages:
            return []
            
        pool_k = max(top_k * 2, 10)
        bm25_results = self.bm25.retrieve(query, top_k=pool_k)
        dense_results = self.dense.retrieve(query, top_k=pool_k)
        
        rrf_scores: Dict[str, float] = defaultdict(float)
        passage_map: Dict[str, Passage] = {p.id: p for p in self.passages}
        
        for rank, (p, _) in enumerate(bm25_results):
            rrf_scores[p.id] += self.bm25_weight / (self.k + rank + 1)
            
        for rank, (p, _) in enumerate(dense_results):
            rrf_scores[p.id] += self.dense_weight / (self.k + rank + 1)
            
        ranked = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        results = []
        for pid, score in ranked:
            p = passage_map[pid].model_copy()
            p.score = float(score)
            results.append((p, float(score)))
        return results
