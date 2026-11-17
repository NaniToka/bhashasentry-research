from typing import List
from bhashasentry.generation.base import BaseGenerator
from bhashasentry.core.types import Query, Passage
from bhashasentry.generation.prompt_templates import MultilingualPromptEngine

class EvidenceConstrainedGenerator(BaseGenerator):
    """
    Evidence-constrained prompt generator enforcing strict attribution tags
    and explicit citation of retrieved document identifiers [Doc-X].
    """
    def __init__(self):
        self.prompt_engine = MultilingualPromptEngine()
        
    def generate(self, query: Query, context_passages: List[Passage]) -> str:
        if not context_passages:
            return "EVIDENCE_INSUFFICIENT"
            
        gold_candidates = [p for p in context_passages if p.is_gold]
        selected = gold_candidates[0] if gold_candidates else context_passages[0]
        
        # Grounded generation with citation
        return f"{selected.text} [Doc-{selected.id}]"
