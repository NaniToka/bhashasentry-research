import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from bhashasentry.config import SupportedLanguage
from bhashasentry.core.types import Query, Passage

class DatasetLoader:
    """
    Loads and parses multilingual RAG datasets, supporting IndicRAGSuite,
    BHRAM-IL schemas, and native BhashaSentry benchmark formats.
    """
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path("data")
        
    def load_gold_benchmark(self, filename: str = "processed/bhashasentry_gold_benchmark.json") -> List[Dict[str, Any]]:
        target_path = self.data_dir / filename
        if not target_path.exists():
            raise FileNotFoundError(f"Benchmark dataset not found at: {target_path}")
        with open(target_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_passages(self, filename: str = "processed/multilingual_passages.json") -> List[Passage]:
        target_path = self.data_dir / filename
        if not target_path.exists():
            return []
        with open(target_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        return [Passage(**p) for p in raw_data]

    def load_cross_lingual_queries(self, filename: str = "processed/cross_lingual_queries.json") -> List[Dict[str, Any]]:
        target_path = self.data_dir / filename
        if not target_path.exists():
            return []
        with open(target_path, "r", encoding="utf-8") as f:
            return json.load(f)
