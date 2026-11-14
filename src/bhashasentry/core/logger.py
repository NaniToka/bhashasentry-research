import json
import logging
from pathlib import Path
from typing import Dict, Any
from bhashasentry.core.types import AuditTrace

class EvidenceAuditLogger:
    """
    Structured audit logger writing complete RAG evidence traces to JSONL.
    """
    def __init__(self, log_path: Path = Path("logs/bhashasentry_audit.jsonl")):
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
    def log_trace(self, trace: AuditTrace) -> None:
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(trace.model_dump_json() + "\n")
            
    def get_recent_traces(self, limit: int = 10):
        if not self.log_path.exists():
            return []
        traces = []
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    traces.append(json.loads(line))
        return traces[-limit:]
