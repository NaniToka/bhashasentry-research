from bhashasentry.data.dataset_loader import DatasetLoader
from bhashasentry.claim_verification.nli_verifier import CrossLingualNLIVerifier
from bhashasentry.core.types import AtomicClaim, Passage
from bhashasentry.config import SupportedLanguage

def evaluate_claims():
    loader = DatasetLoader()
    benchmark = loader.load_gold_benchmark()
    passages = loader.load_passages()
    verifier = CrossLingualNLIVerifier()
    
    tp = fp = fn = 0
    for item in benchmark:
        item_passages = [p for p in passages if p.id == item["gold_passage_id"]]
        for c in item.get("claims", []):
            claim_obj = AtomicClaim(id=c["id"], text=c["text"], language=SupportedLanguage(item["language"]))
            res = verifier.verify(claim_obj, item_passages)
            if res.verdict.value == c["verdict"]:
                tp += 1
            else:
                fp += 1
                
    accuracy = tp / max(1, (tp + fp))
    return {"evaluated_claims": tp + fp, "claim_accuracy": accuracy}

if __name__ == "__main__":
    metrics = evaluate_claims()
    print("Claim Verification Benchmark:", metrics)
