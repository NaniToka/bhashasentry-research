#!/bin/bash
# ==============================================================================
# BhashaSentry Daily Automation Runner
# ==============================================================================
# Executes scheduled daily benchmarks, runs unit tests, generates audit traces,
# and pushes daily progress to https://github.com/NaniToka/bhashasentry-research.git

set -e

REPO_DIR="/Users/tokanani/bhashasentry"
cd "$REPO_DIR"

DATE_STR=$(date +"%Y-%m-%d %H:%M:%S")
echo "[$DATE_STR] Running BhashaSentry Daily Automation..."

# Set Python path
export PYTHONPATH="$REPO_DIR/src"

# Run full regression suite
python3 "$REPO_DIR/scripts/verify_all.py"

# Run end-to-end benchmark
python3 "$REPO_DIR/benchmarks/run_full_evaluation.py"

echo "[$DATE_STR] BhashaSentry Daily Automation Completed Successfully."

