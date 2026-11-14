import re
from typing import List
from bhashasentry.config import SupportedLanguage

class IndicTokenizer:
    """
    Sentence and word tokenization handling Western punctuation,
    Indic Purna Viram (danda '\u0964' and double danda '\u0965'),
    and language-specific morpheme boundaries.
    """
    
    SENTENCE_SPLIT_REGEX = re.compile(r"[.?!|\u0964\u0965\n]+")
    WORD_SPLIT_REGEX = re.compile(r"[\s,\.!?;:\"'()\[\]{}|/\\\u0964\u0965]+")
    
    def split_sentences(self, text: str) -> List[str]:
        if not text:
            return []
        raw_splits = self.SENTENCE_SPLIT_REGEX.split(text)
        return [s.strip() for s in raw_splits if s.strip()]
        
    def tokenize_words(self, text: str) -> List[str]:
        if not text:
            return []
        raw_words = self.WORD_SPLIT_REGEX.split(text)
        return [w.strip() for w in raw_words if w.strip()]
