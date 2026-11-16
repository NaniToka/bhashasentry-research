from typing import List, Tuple
from bhashasentry.core.types import Query, Passage
from bhashasentry.nlp.normalizer import IndicNormalizer

class CrossLingualReranker:
    """
    Cross-encoder style reranking candidate passages based on
    cross-lingual entity and keyword salience.
    """
    def __init__(self):
        self.normalizer = IndicNormalizer()
        
    def rerank(self, query: Query, candidates: List[Tuple[Passage, float]]) -> List[Tuple[Passage, float]]:
        if not candidates:
            return []
        reranked = []
        q_tokens = set(self.normalizer.normalize(query.text, query.language).lower().split())
        for passage, init_score in candidates:
            p_tokens = set(self.normalizer.normalize(passage.text, passage.language).lower().split())
            overlap = len(q_tokens.intersection(p_tokens)) / max(1, len(q_tokens))
            new_score = (init_score * 0.7) + (overlap * 0.3)
            p_copy = passage.model_copy()
            p_copy.score = float(new_score)
            reranked.append((p_copy, float(new_score)))
            
        return sorted(reranked, key=lambda x: x[1], reverse=True)
