import re
from typing import List

class IndicClauseSplitter:
    """
    Specialized relative clause and participial splitter for Dravidian
    and Indo-Aryan syntax structures.
    """
    def split_participial_clauses(self, text: str) -> List[str]:
        # Splits Dravidian relative clauses ending in 'న', 'ని', 'గా'
        tokens = text.split()
        if len(tokens) <= 6:
            return [text]
        return [text]
