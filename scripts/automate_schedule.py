#!/usr/bin/env python3
"""
BhashaSentry Master Schedule Automation CLI
============================================
Allows inspecting the 132-commit roadmap (11 days x 12 commits/day),
running daily incremental tasks, and verifying synchronization with GitHub.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def check_status():
    res = subprocess.run(["git", "log", "--pretty=format:%ad", "--date=short"], cwd=REPO_ROOT, capture_output=True, text=True)
    dates = res.stdout.strip().split("\n")
    from collections import Counter
    counts = Counter(dates)
    print("=== BhashaSentry Commit Schedule Status ===")
    print(f"Total Commits: {len(dates)}")
    print("------------------------------------------")
    for d in sorted(counts.keys()):
        print(f"  {d}: {counts[d]} commits")
    print("------------------------------------------")
    expected = 132
    if len(dates) >= expected:
        print(f"✓ All {expected} scheduled commits (11 days x 12/day) are committed.")
    else:
        print(f"! Current: {len(dates)} / {expected} commits.")

def run_tests():
    cmd = ["python3", str(REPO_ROOT / "scripts" / "verify_all.py")]
    subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser(description="BhashaSentry Schedule Automation")
    parser.add_argument("--status", action="store_true", help="Print schedule status across 11 days")
    parser.add_argument("--test", action="store_true", help="Run full regression verification")
    args = parser.parse_args()

    if args.test:
        run_tests()
    else:
        check_status()

if __name__ == "__main__":
    main()

