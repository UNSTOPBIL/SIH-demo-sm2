#!/usr/bin/env python3
"""
Deploy frontend to Vercel in clean git-free staging directory.
"""

import os
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path

VERCEL_TOKEN = os.environ.get("VERCEL_TOKEN", "")
ROOT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT_DIR / "frontend"

def deploy():
    # 1. Build frontend locally first to ensure dist is fresh
    print("[*] Running npm run build in frontend...")
    subprocess.run(["cmd.exe", "/c", "npm", "run", "build"], cwd=str(FRONTEND_DIR), check=True)

    # 2. Stage files
    tmpdir = tempfile.mkdtemp()
    try:
        dest = Path(tmpdir) / "packai-frontend"
        print(f"[*] Staging frontend files in {dest}...")
        shutil.copytree(
            FRONTEND_DIR,
            dest,
            ignore=shutil.ignore_patterns("node_modules", ".git")
        )

        cmd = [
            "cmd.exe", "/c",
            "npx", "vercel",
            "--prod",
            "--token", VERCEL_TOKEN,
            "--yes"
        ]

        print(f"[*] Executing Vercel frontend deployment...")
        res = subprocess.run(
            cmd,
            cwd=str(dest),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        print(res.stdout)
        if res.returncode != 0:
            print(f"[!] Vercel returned code {res.returncode}")
    finally:
        try:
            shutil.rmtree(tmpdir, ignore_errors=True)
        except Exception:
            pass

if __name__ == "__main__":
    deploy()
