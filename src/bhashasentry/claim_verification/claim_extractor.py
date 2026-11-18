import re
from typing import List
from bhashasentry.core.types import AtomicClaim
from bhashasentry.config import SupportedLanguage
from bhashasentry.nlp.tokenizer import IndicTokenizer

class AtomicClaimExtractor:
    """
    Decomposes generated compound answers into atomic, self-contained
    falsifiable propositions (atomic claims).
    """
    def __init__(self):
        self.tokenizer = IndicTokenizer()
        
    def extract_claims(self, text: str, lang: SupportedLanguage) -> List[AtomicClaim]:
        if not text:
            return []
            
        sentences = self.tokenizer.split_sentences(text)
        claims = []
        counter = 1
        
        for sent in sentences:
            # Strip citation tags if present
            clean_sent = re.sub(r"\[Doc-[^\]]+\]", "", sent).strip()
            if not clean_sent:
                continue
                
            # Split compound conjunctions in Indic languages and English
            conjunctions = [" and ", " మరియు ", " तथा ", " மற்றும் ", " এবং ", " आणि ", ", "]
            parts = [clean_sent]
            for conj in conjunctions:
                new_parts = []
                for p in parts:
                    if conj in p and len(p.split()) > 6:
                        new_parts.extend([sub.strip() for sub in p.split(conj) if sub.strip()])
                    else:
                        new_parts.append(p)
                parts = new_parts
                
            for part in parts:
                if len(part.split()) >= 3:
                    claims.append(AtomicClaim(
                        id=f"claim_{counter:03d}",
                        text=part,
                        language=lang,
                        confidence=1.0
                    ))
                    counter += 1
                    
        return claims
