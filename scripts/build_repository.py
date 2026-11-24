#!/usr/bin/env python3
"""
BhashaSentry Repository Master Automation Engine
================================================
Generates the entire research codebase, benchmarks, datasets, documentation,
paper, and commits the 11-day x 12-commit (132 total commits) roadmap
from 2026-11-14 to 2026-11-24.
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path("/Users/tokanani/bhashasentry")

def run(cmd, env=None):
    res = subprocess.run(cmd, shell=True, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    if res.returncode != 0:
        print(f"Command failed: {cmd}\nstderr: {res.stderr}\nstdout: {res.stdout}")
        raise RuntimeError(res.stderr)
    return res.stdout.strip()

print("BhashaSentry Automation Initialized.")

