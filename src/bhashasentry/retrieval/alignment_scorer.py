from typing import Tuple
from bhashasentry.core.types import Query, Passage
from bhashasentry.config import SupportedLanguage, LANGUAGE_METADATA

class CrossLingualAlignmentScorer:
    """
    Measures cross-lingual alignment degradation when query and passage
    belong to different language families (e.g. Dravidian query -> English passage).
    """
    def score_alignment(self, query: Query, passage: Passage) -> float:
        if query.language == passage.language:
            return 1.0
            
        fam_q = LANGUAGE_METADATA[query.language]["family"]
        fam_p = LANGUAGE_METADATA[passage.language]["family"]
        
        if fam_q == fam_p:
            # Same language family (e.g. Hindi and Marathi, or Telugu and Tamil)
            return 0.85
        elif query.language == SupportedLanguage.EN or passage.language == SupportedLanguage.EN:
            # Cross-lingual bridge (English to Indic)
            return 0.70
        else:
            # Dravidian to Indo-Aryan cross-family
            return 0.55
