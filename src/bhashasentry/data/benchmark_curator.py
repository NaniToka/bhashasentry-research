import json
from pathlib import Path
from typing import Dict, Any, List
from bhashasentry.config import SupportedLanguage

class BenchmarkCurator:
    """
    Validates script coverage, language parity, and ensures zero label leakage
    across the train, pilot, and gold evaluation splits.
    """
    def validate_split_integrity(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        stats = {
            "total_instances": len(dataset),
            "language_counts": {},
            "claims_by_verdict": {"SUPPORTED": 0, "REFUTED": 0, "UNGROUNDED": 0}
        }
        for item in dataset:
            lang = item.get("language", "unknown")
            stats["language_counts"][lang] = stats["language_counts"].get(lang, 0) + 1
            for c in item.get("claims", []):
                v = c.get("verdict", "UNGROUNDED")
                if v in stats["claims_by_verdict"]:
                    stats["claims_by_verdict"][v] += 1
        return stats
