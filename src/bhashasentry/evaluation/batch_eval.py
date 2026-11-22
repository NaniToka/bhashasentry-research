from typing import List, Dict, Any
from bhashasentry.pipeline import BhashaSentryPipeline
from bhashasentry.data.dataset_loader import DatasetLoader
from bhashasentry.config import SupportedLanguage

class BatchPipelineEvaluator:
    """
    Runs end-to-end evaluation of the full BhashaSentry pipeline across the benchmark.
    """
    def __init__(self):
        self.pipeline = BhashaSentryPipeline()
        self.loader = DatasetLoader()
        
    def evaluate(self) -> Dict[str, Any]:
        passages = self.loader.load_passages()
        benchmark = self.loader.load_gold_benchmark()
        self.pipeline.index_knowledge_base(passages)
        
        traces = []
        for item in benchmark:
            t = self.pipeline.process_query(item["query"], SupportedLanguage(item["language"]))
            traces.append(t)
            
        answered = [t for t in traces if t.decision.verdict.value == "ANSWER"]
        warned = [t for t in traces if t.decision.verdict.value == "WARN"]
        abstained = [t for t in traces if t.decision.verdict.value == "ABSTAIN"]
        
        return {
            "total_evaluated": len(traces),
            "answered_count": len(answered),
            "warned_count": len(warned),
            "abstained_count": len(abstained),
            "mean_composite_reliability": sum(t.reliability_signal.composite_reliability_score for t in traces) / len(traces)
        }
