import unicodedata
from typing import Tuple, Dict
from bhashasentry.config import SupportedLanguage, LANGUAGE_METADATA

class IndicLanguageIdentifier:
    """
    Script-based and character-range language identifier for Indic scripts and English.
    """
    
    def identify(self, text: str) -> Tuple[SupportedLanguage, float]:
        if not text or not text.strip():
            return SupportedLanguage.EN, 0.0
            
        char_counts: Dict[SupportedLanguage, int] = {lang: 0 for lang in SupportedLanguage}
        total_letters = 0
        
        for ch in text:
            code = ord(ch)
            if ch.isalpha():
                total_letters += 1
                if 0x0020 <= code <= 0x007F:
                    char_counts[SupportedLanguage.EN] += 1
                elif 0x0C00 <= code <= 0x0C7F:
                    char_counts[SupportedLanguage.TE] += 1
                elif 0x0B80 <= code <= 0x0BFF:
                    char_counts[SupportedLanguage.TA] += 1
                elif 0x0980 <= code <= 0x09FF:
                    char_counts[SupportedLanguage.BN] += 1
                elif 0x0900 <= code <= 0x097F:
                    if code == 0x0933:
                        char_counts[SupportedLanguage.MR] += 2
                    else:
                        char_counts[SupportedLanguage.HI] += 1
                        
        if total_letters == 0:
            return SupportedLanguage.EN, 1.0
            
        if char_counts[SupportedLanguage.HI] > 0 or char_counts[SupportedLanguage.MR] > 0:
            marathi_markers = ["आहे", "नाही", "आणि", "यांचे", "केले", "होते", "महाराष्ट्र", "झाले"]
            hindi_markers = ["है", "नहीं", "और", "उनके", "किया", "था", "थे", "भारत"]
            
            mr_hits = sum(1 for w in marathi_markers if w in text)
            hi_hits = sum(1 for w in hindi_markers if w in text)
            
            if mr_hits > hi_hits:
                char_counts[SupportedLanguage.MR] += mr_hits * 10
            else:
                char_counts[SupportedLanguage.HI] += hi_hits * 10
                
        best_lang = max(char_counts.items(), key=lambda x: x[1])
        confidence = min(1.0, best_lang[1] / max(1, total_letters))
        return best_lang[0], confidence
