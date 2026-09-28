#!/usr/bin/env python3
"""
Deploy PackAI India frontend to Hugging Face Spaces (static SDK).
Space: ustop/packai-india
Direct URL: https://ustop-packai-india.hf.space
"""

import os
import sys
import shutil
import tempfile
from pathlib import Path
from huggingface_hub import HfApi

HF_TOKEN = os.environ.get("HF_TOKEN", "")
SPACE_NAME = "packai-india"
REPO_ID = f"ustop/{SPACE_NAME}"

ROOT_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT_DIR / "frontend" / "dist"

README_CONTENT = """---
title: PackAI India
emoji: 🌾
colorFrom: green
colorTo: indigo
sdk: static
pinned: false
---

# PackAI India
### AI-Based Intelligent Food Packaging Material Recommendation System
**Smart India Hackathon 2026 • Problem Statement SIH26236**
**Ministry of Food Processing Industries (MoFPI)**

- **Biophysical Barrier Kinetics:** Tetens Saturation Vapor Pressure equation & Oxygen Permeation Modeling.
- **India Statutory Shield:** FSSAI (Packaging) Regulations 2018 Schedule IV, BIS IS 10146, IS 9845 Migration Matrix, and CPCB-EPR Category III.
- **Industrial Converter Economics:** GSM, yield, pouch unit cost, and spoilage prevention ROI.
- **Cryptographic Traceability:** SHA-256 Digital Product Passport.
- **Reverse Artwork Auditor:** FSSAI 2020 Display Mandates & Legal Metrology pre-print checks.
"""

def deploy_to_hf(backend_url: str = ""):
    api = HfApi(token=HF_TOKEN)
    print(f"[*] Authenticated as: {api.whoami()['name']}")

    if not DIST_DIR.exists() or not (DIST_DIR / "index.html").exists():
        raise FileNotFoundError(f"Dist directory not found at {DIST_DIR}. Please run npm run build first.")

    with tempfile.TemporaryDirectory() as tmpdir:
        staging = Path(tmpdir)
        print(f"[*] Staging static files in {staging}...")

        # Copy dist content
        for item in DIST_DIR.iterdir():
            if item.is_dir():
                shutil.copytree(item, staging / item.name)
            else:
                shutil.copy2(item, staging / item.name)

        # Write README.md frontmatter for HF Static Space
        (staging / "README.md").write_text(README_CONTENT, encoding="utf-8")

        print(f"[*] Uploading files to Hugging Face Space: {REPO_ID}...")
        api.upload_folder(
            folder_path=str(staging),
            repo_id=REPO_ID,
            repo_type="space",
            commit_message="Deploy PackAI India Web Studio to Hugging Face Spaces",
        )
        print(f"[SUCCESS] Uploaded to Hugging Face Space: https://huggingface.co/spaces/{REPO_ID}")

    direct_url = f"https://ustop-{SPACE_NAME}.hf.space"
    print(f"[*] Direct Web App URL: {direct_url}")
    return direct_url

if __name__ == "__main__":
    url = deploy_to_hf()
    print("HF Space Live URL:", url)
