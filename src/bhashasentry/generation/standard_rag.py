from typing import List
from bhashasentry.generation.base import BaseGenerator
from bhashasentry.core.types import Query, Passage

class StandardRAGGenerator(BaseGenerator):
    """
    Standard unconstrained RAG generator baseline without strict evidence citations.
    Simulates standard commercial LLM generation behavior.
    """
    def generate(self, query: Query, context_passages: List[Passage]) -> str:
        if not context_passages:
            return f"Answer for query '{query.text}' based on general knowledge."
            
        top_passage = context_passages[0]
        # Summarize or synthesize leading information
        return f"{top_passage.text} [Generated via standard RAG]"
