import json
from bhashasentry.data.dataset_loader import DatasetLoader
from bhashasentry.generation.constrained import EvidenceConstrainedGenerator
from bhashasentry.generation.standard_rag import StandardRAGGenerator
from bhashasentry.core.types import Query
from bhashasentry.config import SupportedLanguage

def run_generation_benchmark():
    loader = DatasetLoader()
    benchmark = loader.load_gold_benchmark()
    passages = loader.load_passages()
    
    std_gen = StandardRAGGenerator()
    c_gen = EvidenceConstrainedGenerator()
    
    results = []
    for item in benchmark:
        q = Query(id=item["id"], text=item["query"], language=SupportedLanguage(item["language"]))
        ans_std = std_gen.generate(q, passages)
        ans_c = c_gen.generate(q, passages)
        results.append({
            "id": q.id,
            "lang": q.language.value,
            "standard_answer": ans_std,
            "constrained_answer": ans_c
        })
    return results

if __name__ == "__main__":
    out = run_generation_benchmark()
    print("Generation benchmark run successfully for", len(out), "queries.")
