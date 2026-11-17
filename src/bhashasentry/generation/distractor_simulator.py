import random
from typing import List
from bhashasentry.core.types import Query, Passage

class DistractorSimulator:
    """
    Simulates Problem C (Evidence utilization failure) where irrelevant
    distractor passages bleed into generated responses.
    """
    def simulate_distractor_bleed(self, answer_text: str, distractor_passage: Passage) -> str:
        distractor_snippet = " ".join(distractor_passage.text.split()[:8])
        return f"{answer_text} Furthermore, {distractor_snippet}."
