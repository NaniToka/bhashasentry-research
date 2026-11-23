import json
from pathlib import Path

def load_results():
    p = Path("experiments/results/raw_experiment_metrics.json")
    with open(p, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    r = load_results()
    print("Loaded experiment baseline metrics. Total languages:", len(r["languages"]))
