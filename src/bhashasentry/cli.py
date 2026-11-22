import argparse
import sys
import json
from bhashasentry import __version__
from bhashasentry.config import SupportedLanguage
from bhashasentry.nlp.lang_id import IndicLanguageIdentifier
from benchmarks.retrieval_eval import evaluate_retrieval
from benchmarks.generation_eval import run_generation_benchmark
from benchmarks.claim_eval import evaluate_claims
from benchmarks.consistency_eval import evaluate_cross_lingual_consistency
from benchmarks.hallucination_eval import evaluate_hallucination_detection
from benchmarks.abstention_eval import evaluate_abstention_tradeoff
from benchmarks.run_full_evaluation import run_full_evaluation

def main():
    parser = argparse.ArgumentParser(
        prog="bhashasentry",
        description="BhashaSentry: Multilingual Evidence Reliability & Hallucination Detection Engine in RAG"
    )
    parser.add_argument("--version", action="version", version=f"BhashaSentry v{__version__}")
    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")
    
    id_parser = subparsers.add_parser("identify", help="Identify language of input text")
    id_parser.add_argument("text", type=str, help="Text to classify")
    
    ret_parser = subparsers.add_parser("eval-retrieval", help="Run retrieval benchmark evaluation")
    gen_parser = subparsers.add_parser("eval-generation", help="Run generation benchmark evaluation")
    claim_parser = subparsers.add_parser("eval-claims", help="Run claim verification benchmark evaluation")
    cons_parser = subparsers.add_parser("eval-consistency", help="Run cross-lingual consistency benchmark")
    hall_parser = subparsers.add_parser("eval-hallucination", help="Run hallucination detection benchmark")
    abs_parser = subparsers.add_parser("eval-abstention", help="Run selective abstention coverage-risk benchmark")
    all_parser = subparsers.add_parser("run-all", help="Execute complete end-to-end evaluation")
    
    args = parser.parse_args()
    
    if args.subcommand == "identify":
        lang_id = IndicLanguageIdentifier()
        lang, conf = lang_id.identify(args.text)
        print(f"Language: {lang.value} ({lang.name}), Confidence: {conf:.4f}")
    elif args.subcommand == "eval-retrieval":
        res = evaluate_retrieval()
        print(json.dumps(res, indent=2))
    elif args.subcommand == "eval-generation":
        res = run_generation_benchmark()
        print(f"Generated {len(res)} benchmark outputs.")
    elif args.subcommand == "eval-claims":
        res = evaluate_claims()
        print(json.dumps(res, indent=2))
    elif args.subcommand == "eval-consistency":
        res = evaluate_cross_lingual_consistency()
        print(json.dumps(res, indent=2))
    elif args.subcommand == "eval-hallucination":
        res = evaluate_hallucination_detection()
        print(json.dumps(res, indent=2))
    elif args.subcommand == "eval-abstention":
        res = evaluate_abstention_tradeoff()
        print(json.dumps(res, indent=2))
    elif args.subcommand == "run-all":
        res = run_full_evaluation()
        print(json.dumps(res, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
