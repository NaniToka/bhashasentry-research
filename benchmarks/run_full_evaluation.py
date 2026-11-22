import json
from bhashasentry.evaluation.batch_eval import BatchPipelineEvaluator

def run_full_evaluation():
    evaluator = BatchPipelineEvaluator()
    res = evaluator.evaluate()
    return res

if __name__ == "__main__":
    out = run_full_evaluation()
    print("Full End-to-End Evaluation Summary:")
    print(json.dumps(out, indent=2))
