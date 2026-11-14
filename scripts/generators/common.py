import os
import subprocess
from pathlib import Path

REPO_ROOT = Path("/Users/tokanani/bhashasentry")

def write_file(rel_path: str, content: str):
    full_path = REPO_ROOT / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {rel_path} ({len(content)} bytes)")

def commit_step(day_num: int, commit_num: int, message: str, files_to_add=None):
    """
    Commit with precise timestamps.
    day_num: 1 to 11 (Nov 14 to Nov 24, 2026)
    commit_num: 1 to 12
    """
    day_date = 13 + day_num # day 1 -> 14, day 11 -> 24
    hour = 8 + commit_num  # commit 1 -> 09:00, commit 12 -> 20:00
    minute = 15
    timestamp = f"2026-11-{day_date:02d} {hour:02d}:{minute:02d}:00 +0530"

    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = timestamp
    env["GIT_COMMITTER_DATE"] = timestamp
    env["GIT_AUTHOR_NAME"] = "NaniToka"
    env["GIT_AUTHOR_EMAIL"] = "tokananiy@gmail.com"
    env["GIT_COMMITTER_NAME"] = "NaniToka"
    env["GIT_COMMITTER_EMAIL"] = "tokananiy@gmail.com"

    if files_to_add:
        for f in files_to_add:
            subprocess.run(["git", "add", f], cwd=REPO_ROOT, check=True)
    else:
        subprocess.run(["git", "add", "."], cwd=REPO_ROOT, check=True)

    res = subprocess.run(["git", "commit", "-m", message], cwd=REPO_ROOT, env=env, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Commit error: {res.stderr}\nstdout: {res.stdout}")
        raise RuntimeError(res.stderr)
    print(f"✓ Committed [{timestamp}] {message}")
