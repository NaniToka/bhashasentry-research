from typing import Dict, Any, List
from bhashasentry.config import SupportedLanguage, LanguageFamily, LANGUAGE_METADATA

class LanguageFamilyClusterAnalyzer:
    """
    Analyzes consistency variance within family (Dravidian: te, ta; Indo-Aryan: hi, bn, mr)
    versus across language families.
    """
    def analyze_clusters(self, matrix: List[List[float]], langs: List[SupportedLanguage]) -> Dict[str, float]:
        intra_family = []
        inter_family = []
        
        for i in range(len(langs)):
            for j in range(i + 1, len(langs)):
                fam_i = LANGUAGE_METADATA[langs[i]]["family"]
                fam_j = LANGUAGE_METADATA[langs[j]]["family"]
                score = matrix[i][j]
                if fam_i == fam_j:
                    intra_family.append(score)
                else:
                    inter_family.append(score)
                    
        return {
            "mean_intra_family_consistency": sum(intra_family) / max(1, len(intra_family)),
            "mean_inter_family_consistency": sum(inter_family) / max(1, len(inter_family))
        }
