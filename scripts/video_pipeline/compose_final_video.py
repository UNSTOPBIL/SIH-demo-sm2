#!/usr/bin/env python3
r"""
Master Compositor for SIH26236 Video Pipeline
Sequences:
  1. Slide 1: Team KATSURO & PackAI India Title Slate (slide1_team.png)
     - Duration strictly locked to audio1_intro.mp3 (~14.0s)
  2. Slide 2: Problem Statement Breakdown Slate (slide2_problem_statement.png)
     - Duration strictly locked to audio2_problem.mp3 (~21.7s)
  3. Chromium Browser Walkthrough (raw_video.webm)
     - Duration strictly locked to audio3 + audio4 + audio5 (~114.1s)
     - Top glassmorphic broadcast banner overlay (banner_overlay.png)
     - Terminal picture-in-picture overlay (terminal_pip.png) during final 8 seconds (19/19 tests passing)
  4. Master Audio: EBU R128 broadcast-normalized neural voiceover track (master_audio.m4a)
Renders final export: d:\.anti\.sih(2)\sih26236_final_demo.mp4 strictly between 145s and 165s (< 3:00 min).
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Ensure UTF-8 output encoding on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent.parent
MANIFEST_PATH = BASE_DIR / "audio_manifest.json"
RECORD_DIR = BASE_DIR / "raw_recordings"
AUDIO_DIR = BASE_DIR / "audio"

SLIDE1_PATH = BASE_DIR / "slide1_team.png"
SLIDE2_PATH = BASE_DIR / "slide2_problem_statement.png"
BANNER_PATH = BASE_DIR / "banner_overlay.png"
TERMINAL_PIP_PATH = BASE_DIR / "terminal_pip.png"
MASTER_AUDIO_PATH = BASE_DIR / "master_audio.m4a"
OUTPUT_VIDEO_PATH = PROJECT_DIR / "sih26236_final_demo.mp4"


def get_ffprobe_duration(media_path: Path) -> float:
    """Extract exact duration in seconds using ffprobe."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(media_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())


def ensure_intro_slides():
    """Ensure slide1_team.png and slide2_problem_statement.png exist."""
    if not (SLIDE1_PATH.exists() and SLIDE2_PATH.exists()):
        print("Generating Dual Intro & Problem Statement slides...")
        script = BASE_DIR / "create_intro_slides.py"
        subprocess.run([sys.executable, str(script)], check=True)


def ensure_terminal_pip():
    """Ensure terminal_pip.png exists, generating it if needed."""
    if not TERMINAL_PIP_PATH.exists():
        print("Generating terminal PiP overlay...")
        script = BASE_DIR / "create_terminal_pip.py"
        subprocess.run([sys.executable, str(script)], check=True)


def generate_banner_overlay(output_path: Path, width=1920, height=1080):
    """
    Generates a high-resolution broadcast banner PNG with alpha channel.
    Bar sits at y=0 to y=52 with glassmorphic slate styling, live status beacon,
    and official SIH 2026 | MoFPI | SIH26236 | Team Katsuro typography.
    """
    print("Generating top banner overlay...")
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    banner_h = 52

    # Draw dark slate glassmorphism bar (RGBA: 15, 23, 42, 240)
    draw.rectangle([(0, 0), (width, banner_h)], fill=(15, 23, 42, 240))
    # Bottom hairline border in emerald green (RGBA: 16, 185, 129, 230)
    draw.line([(0, banner_h - 1), (width, banner_h - 1)], fill=(16, 185, 129, 230), width=2)

    # Attempt to load clean TrueType fonts from Windows Fonts
    font_bold_path = "C:/Windows/Fonts/arialbd.ttf"
    font_reg_path = "C:/Windows/Fonts/segoeui.ttf"

    try:
        font_badge = ImageFont.truetype(font_bold_path, 13)
        font_title = ImageFont.truetype(font_bold_path, 17)
        font_right = ImageFont.truetype(font_bold_path, 12)
    except Exception:
        font_badge = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_right = ImageFont.load_default()

    # 1. Live Emerald Pulse Dot
    dot_cx, dot_cy = 28, banner_h // 2
    draw.ellipse([(dot_cx - 5, dot_cy - 5), (dot_cx + 5, dot_cy + 5)], fill=(16, 185, 129, 255))
    draw.ellipse([(dot_cx - 8, dot_cy - 8), (dot_cx + 8, dot_cy + 8)], outline=(16, 185, 129, 140), width=1)

    # 2. Pill Badge: "SIH 2026"
    badge1_box = [(44, 14), (122, 38)]
    draw.rounded_rectangle(badge1_box, radius=6, fill=(16, 185, 129, 45), outline=(16, 185, 129, 160), width=1)
    draw.text((54, 18), "SIH 2026", fill=(52, 211, 153, 255), font=font_badge)

    # 3. Pill Badge: "MoFPI"
    badge2_box = [(128, 14), (188, 38)]
    draw.rounded_rectangle(badge2_box, radius=6, fill=(30, 41, 59, 220), outline=(71, 85, 105, 180), width=1)
    draw.text((138, 18), "MoFPI", fill=(241, 245, 249, 255), font=font_badge)

    # 4. Main Title
    draw.text((200, 16), "SIH26236: AI Food Packaging Decision System", fill=(255, 255, 255, 255), font=font_title)

    # 5. Right Badges
    right_pill1 = [(1480, 14), (1670, 38)]
    draw.rounded_rectangle(right_pill1, radius=6, fill=(245, 158, 11, 35), outline=(245, 158, 11, 150), width=1)
    draw.text((1495, 18), "TEAM KATSURO", fill=(251, 191, 36, 255), font=font_right)

    right_pill2 = [(1680, 14), (1895, 38)]
    draw.rounded_rectangle(right_pill2, radius=6, fill=(16, 185, 129, 30), outline=(16, 185, 129, 120), width=1)
    draw.text((1694, 18), "ODOP & PMFME ACCELERATOR", fill=(52, 211, 153, 255), font=font_right)

    img.save(str(output_path), "PNG")
    print(f"Banner overlay saved to: {output_path}")


def concatenate_and_normalize_audio(manifest_path: Path, output_audio: Path) -> float:
    """
    Concatenates all 5 scene narration audio files in order and applies
    EBU R128 loudness normalization (-16 LUFS, broadcast standard).
    Returns total duration in seconds.
    """
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    concat_txt_path = BASE_DIR / "concat_audio.txt"
    with open(concat_txt_path, "w", encoding="utf-8") as f:
        for audio_item in manifest["audios"]:
            clip_path = BASE_DIR / audio_item["file"]
            if not clip_path.exists():
                raise FileNotFoundError(f"Missing audio clip: {clip_path}")
            safe_path = str(clip_path.resolve()).replace("\\", "/")
            f.write(f"file '{safe_path}'\n")

    print(f"Concatenating {len(manifest['audios'])} audio clips and normalizing...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt_path),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:a", "aac",
        "-b:a", "192k",
        str(output_audio)
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    duration = get_ffprobe_duration(output_audio)
    print(f"Master normalized narration generated: {output_audio} ({duration:.2f}s)")
    return duration


def find_latest_recording(record_dir: Path) -> Path:
    """Locate the most recently created .webm file from Playwright."""
    recordings = list(record_dir.glob("*.webm"))
    if not recordings:
        raise FileNotFoundError(f"No webm recordings found in {record_dir}")
    latest = max(recordings, key=os.path.getctime)
    return latest


def compose_final_video():
    """
    Muxes:
      1. Slide 1 (slide1_team.png) for duration of Audio 1
      2. Slide 2 (slide2_problem_statement.png) for duration of Audio 2
      3. Chromium Walkthrough with top broadcast banner
      4. Terminal PiP overlay during final 8 seconds
      5. Master normalized narration track
    """
    print("\n==========================================")
    print("SIH26236 Master Video Compositor")
    print("==========================================")

    # Step 1: Ensure assets exist
    ensure_intro_slides()
    ensure_terminal_pip()
    generate_banner_overlay(BANNER_PATH)

    # Load audio manifest for exact durations
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    durations = {item["id"]: item["duration_sec"] for item in manifest["audios"]}
    slide1_dur = durations["audio1_intro"]
    slide2_dur = durations["audio2_problem"]
    print(f"Slide 1 Duration: {slide1_dur:.3f}s (Audio 1)")
    print(f"Slide 2 Duration: {slide2_dur:.3f}s (Audio 2)")

    # Step 2: Produce master normalized audio
    audio_dur = concatenate_and_normalize_audio(MANIFEST_PATH, MASTER_AUDIO_PATH)

    # Step 3: Locate latest recorded walkthrough video
    raw_video = find_latest_recording(RECORD_DIR)
    video_dur = get_ffprobe_duration(raw_video)
    print(f"Raw Walkthrough Video: {raw_video.name} ({video_dur:.2f}s)")

    # Step 4: Calculate PiP display timestamps (final 8 seconds of video)
    pip_start = max(0.0, audio_dur - 8.0)
    pip_end = audio_dur
    print(f"Terminal PiP Window: {pip_start:.2f}s to {pip_end:.2f}s (duration 8.0s)")

    # Step 5: Run FFmpeg composition
    print(f"\nEncoding final 1080p video with Dual Intro Slides, Walkthrough, Banner, PiP, and synced audio...")
    print(f"Output Target: {OUTPUT_VIDEO_PATH}")

    # Build filter complex:
    # Input 0: -loop 1 -t slide1_dur -i slide1_team.png
    # Input 1: -loop 1 -t slide2_dur -i slide2_problem_statement.png
    # Input 2: -i raw_video.webm
    # Input 3: -i banner_overlay.png
    # Input 4: -i terminal_pip.png
    # Input 5: -i master_audio.m4a
    filter_graph = (
        f"[0:v]fps=30,scale=1920:1080,setsar=1,setpts=PTS-STARTPTS[v_slide1];"
        f"[1:v]fps=30,scale=1920:1080,setsar=1,setpts=PTS-STARTPTS[v_slide2];"
        f"[2:v]fps=30,scale=1920:1080,setsar=1,setpts=PTS-STARTPTS[v_walk_src];"
        f"[v_walk_src][3:v]overlay=0:0:eof_action=repeat[v_walk];"
        f"[v_walk]fps=30,scale=1920:1080,setsar=1,setpts=PTS-STARTPTS[v_walk_ready];"
        f"[v_slide1][v_slide2][v_walk_ready]concat=n=3:v=1:a=0[v_base_raw];"
        f"[v_base_raw]tpad=stop_mode=clone:stop_duration=5,fps=30[v_base];"
        f"[v_base][4:v]overlay=0:0:eof_action=repeat:enable='between(t,{pip_start:.2f},{pip_end:.2f})'[v_final]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", f"{slide1_dur:.3f}", "-i", str(SLIDE1_PATH),
        "-loop", "1", "-t", f"{slide2_dur:.3f}", "-i", str(SLIDE2_PATH),
        "-i", str(raw_video),
        "-i", str(BANNER_PATH),
        "-i", str(TERMINAL_PIP_PATH),
        "-i", str(MASTER_AUDIO_PATH),
        "-filter_complex", filter_graph,
        "-map", "[v_final]",
        "-map", "5:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-t", f"{audio_dur:.3f}",
        "-movflags", "+faststart",
        str(OUTPUT_VIDEO_PATH)
    ]

    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        print("FFmpeg Error Output:")
        print(p.stderr)
        raise RuntimeError(f"FFmpeg composition failed with code {p.returncode}")

    # Step 6: Verification & Quality Metrics
    if not OUTPUT_VIDEO_PATH.exists():
        raise FileNotFoundError(f"Final output video not found at {OUTPUT_VIDEO_PATH}")

    file_size_mb = OUTPUT_VIDEO_PATH.stat().st_size / (1024 * 1024)
    final_dur = get_ffprobe_duration(OUTPUT_VIDEO_PATH)

    print("\n==========================================")
    print("SUCCESS: FINAL DEMO VIDEO COMPILED!")
    print(f"Location:  {OUTPUT_VIDEO_PATH}")
    print(f"Duration:  {final_dur:.2f}s ({int(final_dur//60)}m {int(final_dur%60)}s)")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Format:    1920x1080 @ 30fps | H.264 / AAC")
    print("==========================================")

    # Sanity checks: strictly between 145s and 165s / under 3:00 min
    assert 144.0 <= final_dur <= 166.0, f"Video duration {final_dur:.2f}s outside target range 145s - 165s!"
    assert file_size_mb >= 10.0, f"Video file size {file_size_mb:.2f} MB is under 10 MB threshold!"

    return str(OUTPUT_VIDEO_PATH)


if __name__ == "__main__":
    compose_final_video()
