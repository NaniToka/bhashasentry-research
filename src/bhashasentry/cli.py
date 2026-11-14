import argparse
import sys
from bhashasentry import __version__
from bhashasentry.config import SupportedLanguage
from bhashasentry.nlp.lang_id import IndicLanguageIdentifier

def main():
    parser = argparse.ArgumentParser(
        prog="bhashasentry",
        description="BhashaSentry: Multilingual Evidence Reliability & Hallucination Detection Engine in RAG"
    )
    parser.add_argument("--version", action="version", version=f"BhashaSentry v{__version__}")
    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")
    
    # Subcommand: identify
    id_parser = subparsers.add_parser("identify", help="Identify language of input text")
    id_parser.add_argument("text", type=str, help="Text to classify")
    
    # Subcommand: audit
    audit_parser = subparsers.add_parser("audit", help="Run end-to-end reliability audit on a query-answer pair")
    audit_parser.add_argument("--query", "-q", type=str, required=True, help="User query")
    audit_parser.add_argument("--answer", "-a", type=str, required=True, help="Generated answer")
    audit_parser.add_argument("--evidence", "-e", type=str, default="", help="Retrieved evidence passage")
    
    args = parser.parse_args()
    
    if args.subcommand == "identify":
        lang_id = IndicLanguageIdentifier()
        lang, conf = lang_id.identify(args.text)
        print(f"Language: {lang.value} ({lang.name}), Confidence: {conf:.4f}")
    elif args.subcommand == "audit":
        print(f"BhashaSentry Audit Engine initialized.")
        print(f"Query: {args.query}")
        print(f"Answer: {args.answer}")
        print(f"Audit status: Pending full pipeline execution.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
