import math
import hashlib
from typing import List, Tuple
from bhashasentry.retrieval.base import BaseRetriever
from bhashasentry.core.types import Query, Passage
from bhashasentry.nlp.normalizer import IndicNormalizer

class DenseMultilingualRetriever(BaseRetriever):
    """
    Multilingual semantic dense retriever utilizing character n-gram hashing
    and projection to simulate multilingual embedding alignment across scripts.
    """
    def __init__(self, dim: int = 128):
        self.dim = dim
        self.passages: List[Passage] = []
        self.doc_embeddings: List[List[float]] = []
        self.normalizer = IndicNormalizer()
        
    def _embed(self, text: str) -> List[float]:
        vec = [0.0] * self.dim
        norm_text = text.lower().strip()
        # Extract character n-grams (2-gram and 3-gram)
        for n in [2, 3]:
            for i in range(max(0, len(norm_text) - n + 1)):
                ngram = norm_text[i:i+n]
                h = int(hashlib.md5(ngram.encode('utf-8')).hexdigest(), 16)
                idx = h % self.dim
                sign = 1.0 if ((h >> 4) % 2 == 0) else -1.0
                vec[idx] += sign
                
        # L2 normalize
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 1e-8:
            vec = [v / norm for v in vec]
        return vec

    def index(self, passages: List[Passage]) -> None:
        self.passages = passages
        self.doc_embeddings = [self._embed(p.text) for p in passages]

    def retrieve(self, query: Query, top_k: int = 5) -> List[Tuple[Passage, float]]:
        if not self.passages:
            return []
        q_vec = self._embed(query.text)
        scores = []
        for idx, d_vec in enumerate(self.doc_embeddings):
            # Cosine similarity
            sim = sum(a * b for a, b in zip(q_vec, d_vec))
            scores.append((idx, sim))
            
        ranked = sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]
        results = []
        for doc_id, score in ranked:
            p = self.passages[doc_id].model_copy()
            p.score = float(score)
            results.append((p, float(score)))
        return results
