import re
from typing import List, Dict, Any

class ResponseParser:
    """
    Parses generated answer strings extracting inline citations [Doc-X],
    numerical entities, and proposition boundaries.
    """
    CITATION_REGEX = re.compile(r"\[Doc-([a-zA-Z0-9_-]+)\]")
    
    def parse_citations(self, answer_text: str) -> List[str]:
        return self.CITATION_REGEX.findall(answer_text)
        
    def strip_citations(self, answer_text: str) -> str:
        return self.CITATION_REGEX.sub("", answer_text).strip()
