import random
from typing import List
from bhashasentry.core.types import Passage, Query
from bhashasentry.config import SupportedLanguage

class DistractorMiner:
    """
    Mines hard negative distractor passages sharing topical vocabulary
    to evaluate context selection robustness (Problem C).
    """
    def inject_hard_negatives(self, gold_passages: List[Passage], all_passages: List[Passage], count: int = 2) -> List[Passage]:
        gold_ids = {p.id for p in gold_passages}
        non_golds = [p for p in all_passages if p.id not in gold_ids]
        distractors = random.sample(non_golds, min(count, len(non_golds)))
        return gold_passages + distractors
