#!/usr/bin/env python3
"""
Deploy PackAI FastAPI backend to Hugging Face Spaces (Docker SDK).
Repo: ustop/packai-backend
"""

import os
import sys
import time
import shutil
import tempfile
from pathlib import Path
from huggingface_hub import HfApi, create_repo

HF_TOKEN = os.environ.get("HF_TOKEN", "")
REPO_NAME = "packai-backend"
REPO_ID = f"ustop/{REPO_NAME}"

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"

README_CONTENT = """---
title: PackAI India Backend
emoji: 📦
colorFrom: green
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# PackAI India - Intelligent Food Packaging Decision Engine
FastAPI Backend for Smart India Hackathon (SIH26236)
MoFPI PMFME & ODOP Micro-Enterprise Support
"""

DOCKERFILE_CONTENT = """FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app/backend

ENV PYTHONPATH=/app
ENV PORT=7860

EXPOSE 7860

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
"""

def deploy():
    api = HfApi(token=HF_TOKEN)
    print(f"[*] Authenticated as: {api.whoami()['name']}")

    # 1. Create Space repo if not exists
    print(f"[*] Ensuring Space exists: {REPO_ID} (sdk=docker)...")
    try:
        api.create_repo(
            repo_id=REPO_ID,
            repo_type="space",
            space_sdk="docker",
            private=False,
            exist_ok=True
        )
        print(f"[OK] Space repository verified: https://huggingface.co/spaces/{REPO_ID}")
    except Exception as e:
        print(f"[!] Info on create_repo: {e}")

    # 2. Build staging folder
    with tempfile.TemporaryDirectory() as tmpdir:
        staging = Path(tmpdir)
        print(f"[*] Staging files in {staging}...")

        # README.md
        (staging / "README.md").write_text(README_CONTENT, encoding="utf-8")

        # Dockerfile
        (staging / "Dockerfile").write_text(DOCKERFILE_CONTENT, encoding="utf-8")

        # requirements.txt
        req_src = BACKEND_DIR / "requirements.txt"
        shutil.copy(req_src, staging / "requirements.txt")

        # backend package
        staging_backend = staging / "backend"
        shutil.copytree(
            BACKEND_DIR,
            staging_backend,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache")
        )

        print(f"[*] Uploading staged files to Hugging Face Space: {REPO_ID}...")
        api.upload_folder(
            folder_path=str(staging),
            repo_id=REPO_ID,
            repo_type="space",
            commit_message="Deploy PackAI India FastAPI Backend v1.0",
        )
        print("[OK] Files uploaded successfully!")

    # 3. Check Space Runtime Status
    print("[*] Monitoring Space runtime status...")
    direct_url = f"https://ustop-{REPO_NAME}.hf.space"
    space_page = f"https://huggingface.co/spaces/{REPO_ID}"
    print(f"[*] Space Page: {space_page}")
    print(f"[*] Direct API URL: {direct_url}")

    for attempt in range(60):
        runtime = api.get_space_runtime(repo_id=REPO_ID)
        stage = runtime.stage
        print(f"    [{attempt+1}/60] Stage: {stage}")
        if stage == "RUNNING":
            print(f"\n[SUCCESS] Hugging Face Space is RUNNING!")
            print(f"API Base URL: {direct_url}")
            return direct_url
        elif stage in ["BUILD_ERROR", "RUNTIME_ERROR"]:
            print(f"\n[ERROR] Space entered error stage: {stage}")
            print(f"Please check logs at {space_page}")
            return None
        time.sleep(5)

    return direct_url

if __name__ == "__main__":
    url = deploy()
    print("Result URL:", url)
