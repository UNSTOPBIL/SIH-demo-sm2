#!/usr/bin/env python3
r"""
Neural Audio Narration Generator for SIH26236 Demo Video
Synthesizes professional Indian English narration using edge-tts (en-IN-PrabhatNeural).
Exports 5 dedicated audio clips matching:
  - Audio 1: Slide 1 (Team KATSURO Intro)
  - Audio 2: Slide 2 (Problem Statement Breakdown)
  - Audio 3: Scene A (Screen 1 & 2: Biophysics & Kinetics)
  - Audio 4: Scene B (Screen 3 & 4: Statutory Shield & PDF)
  - Audio 5: Scene C (Passport, Auditor & Architecture Closing)
Records exact millisecond durations in audio_manifest.json for strict synchronization.
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
import edge_tts

# Ensure UTF-8 output encoding on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "audio"
MANIFEST_FILE = BASE_DIR / "audio_manifest.json"
VOICE = "en-IN-PrabhatNeural"

AUDIOS = [
    {
        "id": "audio1_intro",
        "title": "Intro & Team Katsuro",
        "rate": "+8%",
        "text": (
            "Respected evaluators, Team Katsuro presents Pack A-I India for Smart India "
            "Hackathon 2026, Problem Statement S-I-H 26236 under the Ministry of Food Processing Industries."
        )
    },
    {
        "id": "audio2_problem",
        "title": "Problem Statement Breakdown",
        "rate": "+8%",
        "text": (
            "India's P-M-F-M-E and O-D-O-P schemes empower over two lakh food micro-enterprises, "
            "yet processors lose up to 30 percent of agricultural produce due to empirical packaging "
            "and F-S-S-A-I non-compliance. Existing global tools are English-only and ignore Indian law. "
            "Pack A-I India closes this gap."
        )
    },
    {
        "id": "audio3_physics",
        "title": "Screen 1 & 2: Biophysics & Kinetics",
        "rate": "+8%",
        "text": (
            "Demonstrating with Foxnut, or Mithila Makhana from Bihar. Using simulation presets, "
            "we stress-test under extreme tropical warehousing at 42 degrees Celsius and 90 percent "
            "humidity. Applying the Tetens saturation vapor pressure equation, the engine calculates "
            "required W-V-T-R and O-T-R thresholds. Under this tropical moisture demand, the solver "
            "rejects mono-films and engineers an optimal three-layer Aluminium Foil barrier triplex. "
            "The converter economics module calculates composite G-S-M at 92.3, unit cost at 82 paise, "
            "and demonstrates a 400 percent spoilage prevention R-O-I."
        )
    },
    {
        "id": "audio4_compliance",
        "title": "Screen 3 & 4: Statutory Shield & PDF",
        "rate": "+8%",
        "text": (
            "Advancing to the India Statutory Shield, Pack A-I India automatically chains national "
            "regulations: F-S-S-A-I 2018 Packaging Schedule Four, mandatory B-I-S standard I-S 10146, "
            "and the I-S 9845 migration simulant protocol across distilled water, acetic acid, and iso-octane, "
            "while classifying under C-P-C-B E-P-R Category Three. Micro-enterprises can instantly export an "
            "official, audit-ready one-page A4 P-D-F readiness certificate generated via ReportLab."
        )
    },
    {
        "id": "audio5_passport_auditor",
        "title": "Passport, Auditor & Architecture Closing",
        "rate": "+8%",
        "text": (
            "Every batch receives a cryptographically verifiable Digital Product Passport with an "
            "S-H-A 256 seal and N-A-B-L testing protocol. Furthermore, our reverse label artwork auditor "
            "tests draft packaging against F-S-S-A-I 2020 Display and Legal Metrology rules, flagging "
            "missing license digits and allergen alerts. Engineered with FastAPI and Scikit-Learn "
            "achieving 92.2 percent accuracy, Team Katsuro delivers institutional-grade packaging engineering. "
            "Thank you."
        )
    }
]


def get_audio_duration(file_path: Path) -> float:
    """Get precise audio duration in seconds using ffprobe."""
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(file_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())
    except Exception as e:
        print(f"Warning: ffprobe failed for {file_path}: {e}")
        return 0.0


async def generate_single_audio(item: dict) -> dict:
    item_id = item["id"]
    output_path = OUTPUT_DIR / f"{item_id}.mp3"
    print(f"Synthesizing [{item_id}] ({item['title']})...")

    rate = item.get("rate", "+8%")
    communicate = edge_tts.Communicate(item["text"], VOICE, rate=rate, pitch="+0Hz")
    await communicate.save(str(output_path))

    duration = get_audio_duration(output_path)
    print(f"  -> Generated {output_path.name} | Duration: {duration:.2f}s")

    return {
        "id": item_id,
        "title": item["title"],
        "file": f"audio/{output_path.name}",
        "duration_sec": duration,
        "text": item["text"]
    }


async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "voice": VOICE,
        "audios": [],
        "total_duration_sec": 0.0
    }

    for item in AUDIOS:
        meta = await generate_single_audio(item)
        manifest["audios"].append(meta)
        manifest["total_duration_sec"] += meta["duration_sec"]

    total = manifest["total_duration_sec"]
    mins = int(total // 60)
    secs = int(total % 60)
    print(f"\n==========================================")
    print(f"Total Narration Runtime: {mins}m {secs}s ({total:.2f}s)")
    print(f"Strict Target Window (145s - 165s): {'PASSED' if 145 <= total <= 165 else 'ADJUST'}")
    print(f"==========================================")

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Manifest written to: {MANIFEST_FILE}")
    return manifest


if __name__ == "__main__":
    asyncio.run(main())
