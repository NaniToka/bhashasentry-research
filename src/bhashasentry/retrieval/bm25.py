import math
from collections import Counter, defaultdict
from typing import List, Tuple, Dict
from bhashasentry.retrieval.base import BaseRetriever
from bhashasentry.core.types import Query, Passage
from bhashasentry.nlp.tokenizer import IndicTokenizer
from bhashasentry.nlp.normalizer import IndicNormalizer

class BM25Retriever(BaseRetriever):
    """
    Okapi BM25 Sparse Retriever with language-aware tokenization
    and length normalization for Indic and English text.
    """
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.tokenizer = IndicTokenizer()
        self.normalizer = IndicNormalizer()
        self.passages: List[Passage] = []
        self.doc_len: List[int] = []
        self.avg_dl: float = 0.0
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.inverted_index: Dict[str, List[Tuple[int, int]]] = defaultdict(list)
        self.total_docs: int = 0
        
    def index(self, passages: List[Passage]) -> None:
        self.passages = passages
        self.total_docs = len(passages)
        self.doc_len = []
        self.doc_freqs = defaultdict(int)
        self.inverted_index = defaultdict(list)
        
        total_len = 0
        for doc_id, passage in enumerate(passages):
            norm_text = self.normalizer.normalize(passage.text, passage.language)
            tokens = self.tokenizer.tokenize_words(norm_text.lower())
            length = len(tokens)
            self.doc_len.append(length)
            total_len += length
            
            tf = Counter(tokens)
            for token, count in tf.items():
                self.doc_freqs[token] += 1
                self.inverted_index[token].append((doc_id, count))
                
        self.avg_dl = (total_len / self.total_docs) if self.total_docs > 0 else 1.0

    def retrieve(self, query: Query, top_k: int = 5) -> List[Tuple[Passage, float]]:
        if not self.passages or self.total_docs == 0:
            return []
            
        norm_query = self.normalizer.normalize(query.text, query.language)
        query_tokens = self.tokenizer.tokenize_words(norm_query.lower())
        scores: Dict[int, float] = defaultdict(float)
        
        for token in query_tokens:
            if token not in self.doc_freqs:
                continue
            df = self.doc_freqs[token]
            idf = math.log(1.0 + (self.total_docs - df + 0.5) / (df + 0.5))
            for doc_id, tf in self.inverted_index[token]:
                dl = self.doc_len[doc_id]
                denom = tf + self.k1 * (1.0 - self.b + self.b * (dl / self.avg_dl))
                scores[doc_id] += idf * ((tf * (self.k1 + 1.0)) / max(1e-6, denom))
                
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        results = []
        for doc_id, score in ranked:
            p = self.passages[doc_id].model_copy()
            p.score = float(score)
            results.append((p, float(score)))
        return results
