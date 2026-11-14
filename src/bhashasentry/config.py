from enum import Enum
from typing import Dict, List
from pydantic import BaseModel, Field

class SupportedLanguage(str, Enum):
    EN = "en"  # English
    HI = "hi"  # Hindi
    TE = "te"  # Telugu
    TA = "ta"  # Tamil
    BN = "bn"  # Bengali
    MR = "mr"  # Marathi

class LanguageFamily(str, Enum):
    GERMANIC = "germanic"
    INDO_ARYAN = "indo_aryan"
    DRAVIDIAN = "dravidian"

LANGUAGE_METADATA: Dict[SupportedLanguage, Dict] = {
    SupportedLanguage.EN: {
        "name": "English",
        "script": "Latin",
        "family": LanguageFamily.GERMANIC,
        "unicode_range": (0x0020, 0x007F),
    },
    SupportedLanguage.HI: {
        "name": "Hindi",
        "script": "Devanagari",
        "family": LanguageFamily.INDO_ARYAN,
        "unicode_range": (0x0900, 0x097F),
    },
    SupportedLanguage.TE: {
        "name": "Telugu",
        "script": "Telugu",
        "family": LanguageFamily.DRAVIDIAN,
        "unicode_range": (0x0C00, 0x0C7F),
    },
    SupportedLanguage.TA: {
        "name": "Tamil",
        "script": "Tamil",
        "family": LanguageFamily.DRAVIDIAN,
        "unicode_range": (0x0B80, 0x0BFF),
    },
    SupportedLanguage.BN: {
        "name": "Bengali",
        "script": "Bengali",
        "family": LanguageFamily.INDO_ARYAN,
        "unicode_range": (0x0980, 0x09FF),
    },
    SupportedLanguage.MR: {
        "name": "Marathi",
        "script": "Devanagari",
        "family": LanguageFamily.INDO_ARYAN,
        "unicode_range": (0x0900, 0x097F),
    },
}

class BhashaSentryConfig(BaseModel):
    # Retrieval Hyperparameters
    bm25_k1: float = 1.5
    bm25_b: float = 0.75
    rrf_k: int = 60
    top_k_retrieval: int = 5
    dense_dim: int = 384
    
    # Traceability Multi-Signal Weights
    weight_retrieval: float = 0.25
    weight_support: float = 0.45
    weight_contradiction: float = 0.20
    weight_consistency: float = 0.10
    
    # Abstention Thresholds
    tau_answer: float = 0.72
    tau_warn: float = 0.45
    
    # Random Seed
    random_seed: int = 42
