import unicodedata
import re
from bhashasentry.config import SupportedLanguage

class IndicNormalizer:
    """
    Normalizes Indic Unicode text: NFC normalization, nukta handling,
    zero-width joiners/non-joiners, danda standardizations, and whitespace trimming.
    """
    
    DANDA = "\u0964"
    DOUBLE_DANDA = "\u0965"
    ZWJ = "\u200D"
    ZWNJ = "\u200C"
    
    def __init__(self, remove_zw=False):
        self.remove_zw = remove_zw
        
    def normalize(self, text: str, lang: SupportedLanguage = SupportedLanguage.EN) -> str:
        if not text:
            return ""
            
        normalized = unicodedata.normalize("NFC", text)
        
        if self.remove_zw:
            normalized = normalized.replace(self.ZWJ, "").replace(self.ZWNJ, "")
            
        normalized = re.sub(r"\s+", " ", normalized).strip()
        
        if lang in [SupportedLanguage.HI, SupportedLanguage.MR, SupportedLanguage.BN]:
            normalized = re.sub(r"\.\s*$", f" {self.DANDA}", normalized)
            
        return normalized
