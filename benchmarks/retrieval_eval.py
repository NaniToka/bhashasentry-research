import json
from typing import List, Dict, Any
from bhashasentry.core.types import Query, Passage
from bhashasentry.retrieval.hybrid import HybridRRFRetriever
from bhashasentry.data.dataset_loader import DatasetLoader
from bhashasentry.config import SupportedLanguage

def evaluate_retrieval() -> Dict[str, Any]:
    loader = DatasetLoader()
    benchmark = loader.load_gold_benchmark()
    passages = loader.load_passages()
    
    retriever = HybridRRFRetriever()
    retriever.index(passages)
    
    hits_at_1 = 0
    hits_at_3 = 0
    total = len(benchmark)
    
    for item in benchmark:
        q = Query(
            id=item["id"],
            text=item["query"],
            language=SupportedLanguage(item["language"])
        )
        gold_id = item["gold_passage_id"]
        retrieved = retriever.retrieve(q, top_k=3)
        retrieved_ids = [p.id for p, _ in retrieved]
        
        if retrieved_ids and retrieved_ids[0] == gold_id:
            hits_at_1 += 1
        if gold_id in retrieved_ids:
            hits_at_3 += 1
            
    return {
        "total_queries": total,
        "recall@1": hits_at_1 / max(1, total),
        "recall@3": hits_at_3 / max(1, total),
        "mrr": hits_at_1 / max(1, total)
    }

if __name__ == "__main__":
    res = evaluate_retrieval()
    print("Retrieval Benchmark Results:", json.dumps(res, indent=2))
