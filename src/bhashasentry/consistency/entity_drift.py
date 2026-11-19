import re
from typing import Set, Dict, Any

class EntityDriftDetector:
    """
    Detects entity and numerical drift across translation pairs
    (e.g., date modified from 2023 to 2019 or missing landing site).
    """
    def detect_drift(self, ref_entities: Set[str], candidate_text: str) -> Dict[str, Any]:
        found = set()
        missing = set()
        for ent in ref_entities:
            if ent.lower() in candidate_text.lower():
                found.add(ent)
            else:
                missing.add(ent)
        return {
            "preserved_entities": list(found),
            "missing_entities": list(missing),
            "drift_ratio": len(missing) / max(1, len(ref_entities))
        }
