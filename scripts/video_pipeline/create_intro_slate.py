#!/usr/bin/env python3
r"""
Branded Intro Slate Generator for SIH26236
Creates a high-resolution 1920x1080 title card (intro_slate.png)
featuring Team KATSURO, MoFPI, SIH 2026, and PackAI India core pillars.
"""

import sys
import asyncio
from pathlib import Path

# Ensure UTF-8 output encoding on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
SLATE_OUTPUT = BASE_DIR / "intro_slate.png"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
  }
  body {
    width: 1920px;
    height: 1080px;
    background-color: #0B0F17;
    background-image: 
      radial-gradient(ellipse 900px 600px at 50% 48%, rgba(16, 185, 129, 0.16) 0%, rgba(11, 15, 23, 0) 75%),
      radial-gradient(circle 500px at 15% 15%, rgba(245, 158, 11, 0.08) 0%, rgba(11, 15, 23, 0) 65%),
      radial-gradient(circle 500px at 85% 85%, rgba(6, 182, 212, 0.08) 0%, rgba(11, 15, 23, 0) 65%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
    color: #F8FAFC;
  }

  /* Grid overlay for high-tech aesthetic */
  .grid-pattern {
    position: absolute;
    inset: 0;
    background-size: 60px 60px;
    background-image: 
      linear-gradient(to right, rgba(255, 255, 255, 0.02) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
    pointer-events: none;
  }

  /* Decorative glowing orb */
  .glow-orb {
    position: absolute;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(16, 185, 129, 0.22) 0%, transparent 70%);
    filter: blur(80px);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 1;
    pointer-events: none;
  }

  /* Main Container Card */
  .card {
    position: relative;
    z-index: 10;
    width: 1680px;
    padding: 70px 80px;
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(16, 185, 129, 0.35);
    border-radius: 36px;
    backdrop-filter: blur(24px);
    box-shadow: 
      0 30px 100px -20px rgba(0, 0, 0, 0.8),
      0 0 60px -10px rgba(16, 185, 129, 0.2),
      inset 0 1px 2px rgba(255, 255, 255, 0.15);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  /* Top Badges Bar */
  .top-badges {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 24px;
  }
  .badge-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 20px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }
  .badge-sih {
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.4);
    color: #34D399;
  }
  .badge-mofpi {
    background: rgba(245, 158, 11, 0.12);
    border: 1px solid rgba(245, 158, 11, 0.4);
    color: #FBBF24;
  }
  .badge-ps {
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.4);
    color: #A5B4FC;
  }

  /* Header Line */
  .header-line {
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #94A3B8;
    margin-bottom: 30px;
  }

  /* Team Katsuro Presents */
  .team-title {
    font-size: 26px;
    font-weight: 900;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #F59E0B;
    margin-bottom: 16px;
    text-shadow: 0 0 35px rgba(245, 158, 11, 0.45);
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .team-title::before, .team-title::after {
    content: '';
    display: inline-block;
    width: 60px;
    height: 2px;
    background: linear-gradient(to right, transparent, #F59E0B);
  }
  .team-title::after {
    background: linear-gradient(to left, transparent, #F59E0B);
  }

  /* Project Name */
  .project-title {
    font-size: 96px;
    font-weight: 900;
    letter-spacing: -0.03em;
    line-height: 1.05;
    background: linear-gradient(135deg, #FFFFFF 20%, #34D399 60%, #059669 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 18px;
    filter: drop-shadow(0 15px 30px rgba(16, 185, 129, 0.35));
  }

  /* Subtitle */
  .subtitle {
    font-size: 24px;
    font-weight: 600;
    color: #CBD5E1;
    max-width: 1300px;
    line-height: 1.4;
    margin-bottom: 40px;
    letter-spacing: -0.01em;
  }

  .subtitle strong {
    color: #10B981;
    font-weight: 700;
  }

  /* Divider */
  .divider {
    width: 90%;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(16, 185, 129, 0.5), transparent);
    margin-bottom: 35px;
  }

  /* Core Pillars */
  .pillars-container {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 18px;
  }

  .pillar-chip {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(71, 85, 105, 0.6);
    padding: 12px 24px;
    border-radius: 16px;
    font-size: 15px;
    font-weight: 700;
    color: #F1F5F9;
    letter-spacing: 0.02em;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  }

  .pillar-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 10px #10B981;
  }

  /* Bottom Ministry Footer */
  .bottom-footer {
    position: absolute;
    bottom: 35px;
    display: flex;
    align-items: center;
    gap: 30px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #64748B;
  }
</style>
</head>
<body>
  <div class="grid-pattern"></div>
  <div class="glow-orb"></div>

  <div class="card">
    <!-- Top Badges -->
    <div class="top-badges">
      <div class="badge-tag badge-sih">
        <span>Smart India Hackathon 2026</span>
      </div>
      <div class="badge-tag badge-mofpi">
        <span>Ministry of Food Processing Industries (MoFPI)</span>
      </div>
      <div class="badge-tag badge-ps">
        <span>PS ID: SIH26236</span>
      </div>
    </div>

    <!-- Header line -->
    <div class="header-line">
      Government of India • PMFME & ODOP Sustainable Packaging Acceleration
    </div>

    <!-- Team Katsuro -->
    <div class="team-title">
      Team Katsuro Presents
    </div>

    <!-- Project Name -->
    <h1 class="project-title">
      PackAI India
    </h1>

    <!-- Subtitle -->
    <p class="subtitle">
      AI-Based Intelligent Food Packaging Material Recommendation System
    </p>

    <!-- Divider -->
    <div class="divider"></div>

    <!-- Core Pillars -->
    <div class="pillars-container">
      <div class="pillar-chip">
        <div class="pillar-dot"></div>
        <span>Biophysical Barrier Kinetics</span>
      </div>
      <div class="pillar-chip">
        <div class="pillar-dot" style="background: #3B82F6; box-shadow: 0 0 10px #3B82F6;"></div>
        <span>FSSAI & BIS Statutory Shield</span>
      </div>
      <div class="pillar-chip">
        <div class="pillar-dot" style="background: #8B5CF6; box-shadow: 0 0 10px #8B5CF6;"></div>
        <span>SHA-256 Digital Product Passport</span>
      </div>
      <div class="pillar-chip">
        <div class="pillar-dot" style="background: #F59E0B; box-shadow: 0 0 10px #F59E0B;"></div>
        <span>Pre-Print Label Artwork Auditor</span>
      </div>
    </div>
  </div>

  <div class="bottom-footer">
    <span>Offline-First Architecture</span>
    <span>•</span>
    <span>100% Deterministic Biophysics</span>
    <span>•</span>
    <span>IS 10146 & IS 9845 Certified</span>
  </div>
</body>
</html>
"""


async def render_intro_slate(output_path: Path):
    from playwright.async_api import async_playwright

    print("Rendering high-resolution intro slate (1920x1080)...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1
        )
        await page.set_content(HTML_TEMPLATE)
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(output_path), type="png")
        await browser.close()

    print(f"[OK] Intro slate saved to: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")
    return str(output_path)


def main():
    SLATE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    asyncio.run(render_intro_slate(SLATE_OUTPUT))


if __name__ == "__main__":
    main()
