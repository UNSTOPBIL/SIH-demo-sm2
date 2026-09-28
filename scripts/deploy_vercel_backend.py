#!/usr/bin/env python3
"""
Deploy backend to Vercel without Git metadata interference.
"""

import os
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path

VERCEL_TOKEN = os.environ.get("VERCEL_TOKEN", "")
ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"

def deploy():
    with tempfile.TemporaryDirectory() as tmpdir:
        dest = Path(tmpdir) / "packai-backend"
        print(f"[*] Staging backend files in {dest} (clean from .git)...")
        shutil.copytree(
            BACKEND_DIR,
            dest,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache", ".git")
        )

        cmd = [
            "cmd.exe", "/c",
            "npx", "vercel",
            "--prod",
            "--token", VERCEL_TOKEN,
            "--yes"
        ]

        print(f"[*] Executing Vercel deployment...")
        res = subprocess.run(
            cmd,
            cwd=str(dest),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        print(res.stdout)
        if res.returncode != 0:
            sys.exit(f"Vercel deployment failed with code {res.returncode}")

if __name__ == "__main__":
    deploy()
