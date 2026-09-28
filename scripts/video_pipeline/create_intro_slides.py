#!/usr/bin/env python3
r"""
Dual Intro Slides Generator for SIH26236
Generates two 1920x1080 broadcast-quality slides:
  1. slide1_team.png - Team KATSURO & PackAI India Title Slate (6.0s display)
  2. slide2_problem_statement.png - Problem Statement SIH26236 3-Card Breakdown (12.0s display)
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
SLIDE1_PATH = BASE_DIR / "slide1_team.png"
SLIDE2_PATH = BASE_DIR / "slide2_problem_statement.png"

SLIDE1_HTML = r"""<!DOCTYPE html>
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
      radial-gradient(ellipse 900px 600px at 50% 50%, rgba(16, 185, 129, 0.18) 0%, rgba(11, 15, 23, 0) 75%),
      radial-gradient(circle 500px at 15% 15%, rgba(245, 158, 11, 0.1) 0%, rgba(11, 15, 23, 0) 65%),
      radial-gradient(circle 500px at 85% 85%, rgba(6, 182, 212, 0.1) 0%, rgba(11, 15, 23, 0) 65%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
    color: #F8FAFC;
  }

  .grid-pattern {
    position: absolute;
    inset: 0;
    background-size: 60px 60px;
    background-image: 
      linear-gradient(to right, rgba(255, 255, 255, 0.02) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
    pointer-events: none;
  }

  .glow-orb {
    position: absolute;
    width: 650px;
    height: 650px;
    background: radial-gradient(circle, rgba(16, 185, 129, 0.25) 0%, transparent 70%);
    filter: blur(80px);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 1;
    pointer-events: none;
  }

  .card {
    position: relative;
    z-index: 10;
    width: 1680px;
    padding: 70px 80px;
    background: rgba(15, 23, 42, 0.78);
    border: 1.5px solid rgba(16, 185, 129, 0.35);
    border-radius: 36px;
    backdrop-filter: blur(24px);
    box-shadow: 
      0 30px 100px -20px rgba(0, 0, 0, 0.8),
      0 0 60px -10px rgba(16, 185, 129, 0.25),
      inset 0 1px 2px rgba(255, 255, 255, 0.15);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

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
    padding: 8px 22px;
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

  .header-line {
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #94A3B8;
    margin-bottom: 28px;
  }

  .team-title {
    font-size: 28px;
    font-weight: 900;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #F59E0B;
    margin-bottom: 16px;
    text-shadow: 0 0 35px rgba(245, 158, 11, 0.5);
    display: flex;
    align-items: center;
    gap: 18px;
  }
  .team-title::before, .team-title::after {
    content: '';
    display: inline-block;
    width: 70px;
    height: 2px;
    background: linear-gradient(to right, transparent, #F59E0B);
  }
  .team-title::after {
    background: linear-gradient(to left, transparent, #F59E0B);
  }

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

  .subtitle {
    font-size: 24px;
    font-weight: 600;
    color: #CBD5E1;
    max-width: 1300px;
    line-height: 1.4;
    margin-bottom: 40px;
    letter-spacing: -0.01em;
  }

  .divider {
    width: 90%;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(16, 185, 129, 0.5), transparent);
    margin-bottom: 35px;
  }

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
    <div class="top-badges">
      <div class="badge-tag badge-sih">Smart India Hackathon 2026</div>
      <div class="badge-tag badge-mofpi">Ministry of Food Processing Industries (MoFPI)</div>
      <div class="badge-tag badge-ps">PS ID: SIH26236</div>
    </div>

    <div class="header-line">
      Government of India • PMFME & ODOP Sustainable Packaging Acceleration
    </div>

    <div class="team-title">
      Team Katsuro Presents
    </div>

    <h1 class="project-title">
      PackAI India
    </h1>

    <p class="subtitle">
      AI-Based Intelligent Food Packaging Material Recommendation System
    </p>

    <div class="divider"></div>

    <div class="pillars-container">
      <div class="pillar-chip">
        <div class="pillar-dot"></div>
        <span>Deterministic Biophysics</span>
      </div>
      <div class="pillar-chip">
        <div class="pillar-dot" style="background: #3B82F6; box-shadow: 0 0 10px #3B82F6;"></div>
        <span>India Statutory Shield</span>
      </div>
      <div class="pillar-chip">
        <div class="pillar-dot" style="background: #8B5CF6; box-shadow: 0 0 10px #8B5CF6;"></div>
        <span>SHA-256 Digital Passport</span>
      </div>
      <div class="pillar-chip">
        <div class="pillar-dot" style="background: #F59E0B; box-shadow: 0 0 10px #F59E0B;"></div>
        <span>Pre-Print Label Auditor</span>
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

SLIDE2_HTML = r"""<!DOCTYPE html>
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
      radial-gradient(ellipse 1000px 700px at 50% 50%, rgba(30, 41, 59, 0.4) 0%, rgba(11, 15, 23, 0) 80%),
      radial-gradient(circle 500px at 10% 20%, rgba(239, 68, 68, 0.08) 0%, rgba(11, 15, 23, 0) 60%),
      radial-gradient(circle 500px at 90% 80%, rgba(16, 185, 129, 0.08) 0%, rgba(11, 15, 23, 0) 60%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
    color: #F8FAFC;
    padding: 60px 80px;
  }

  .grid-pattern {
    position: absolute;
    inset: 0;
    background-size: 60px 60px;
    background-image: 
      linear-gradient(to right, rgba(255, 255, 255, 0.02) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
    pointer-events: none;
  }

  /* Header Section */
  .header-section {
    text-align: center;
    margin-bottom: 42px;
    position: relative;
    z-index: 10;
  }

  .top-banner {
    display: inline-flex;
    align-items: center;
    gap: 12px;
    padding: 8px 24px;
    background: rgba(245, 158, 11, 0.12);
    border: 1px solid rgba(245, 158, 11, 0.4);
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #FBBF24;
    margin-bottom: 14px;
  }

  .slide-title {
    font-size: 44px;
    font-weight: 900;
    letter-spacing: -0.02em;
    color: #FFFFFF;
    margin-bottom: 8px;
  }

  .slide-subtitle {
    font-size: 17px;
    font-weight: 600;
    color: #94A3B8;
    letter-spacing: 0.05em;
  }

  /* 3 Cards Container */
  .cards-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 28px;
    width: 1760px;
    position: relative;
    z-index: 10;
  }

  .comp-card {
    background: rgba(15, 23, 42, 0.85);
    border-radius: 28px;
    padding: 42px 36px;
    backdrop-filter: blur(20px);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.7);
    position: relative;
    overflow: hidden;
  }

  /* Card A: Ministry */
  .card-a {
    border: 1.5px solid rgba(59, 130, 246, 0.4);
    box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.7), 0 0 35px rgba(59, 130, 246, 0.15);
  }
  .card-a .card-badge {
    background: rgba(59, 130, 246, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.4);
    color: #60A5FA;
  }
  .card-a .card-indicator {
    background: #3B82F6;
  }

  /* Card B: Reality */
  .card-b {
    border: 1.5px solid rgba(239, 68, 68, 0.45);
    box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.7), 0 0 35px rgba(239, 68, 68, 0.15);
  }
  .card-b .card-badge {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #F87171;
  }
  .card-b .card-indicator {
    background: #EF4444;
  }

  /* Card C: Solution */
  .card-c {
    border: 2px solid rgba(16, 185, 129, 0.55);
    box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.7), 0 0 45px rgba(16, 185, 129, 0.25);
    background: rgba(15, 23, 42, 0.92);
  }
  .card-c .card-badge {
    background: rgba(16, 185, 129, 0.18);
    border: 1px solid rgba(16, 185, 129, 0.5);
    color: #34D399;
  }
  .card-c .card-indicator {
    background: #10B981;
  }

  .card-header {
    margin-bottom: 22px;
  }

  .card-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 16px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 14px;
  }

  .card-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }

  .card-title {
    font-size: 26px;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.25;
    margin-bottom: 8px;
  }

  .card-tag {
    font-size: 13px;
    font-weight: 700;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .card-body {
    font-size: 17px;
    line-height: 1.6;
    color: #CBD5E1;
    font-weight: 500;
    margin-top: 10px;
    margin-bottom: 24px;
  }

  .card-body strong {
    color: #FFFFFF;
    font-weight: 700;
  }

  .card-highlight {
    padding: 16px 20px;
    border-radius: 14px;
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(71, 85, 105, 0.4);
    font-size: 14px;
    font-weight: 600;
    line-height: 1.45;
  }

  .card-a .card-highlight {
    color: #93C5FD;
    border-color: rgba(59, 130, 246, 0.3);
  }
  .card-b .card-highlight {
    color: #FCA5A5;
    border-color: rgba(239, 68, 68, 0.3);
  }
  .card-c .card-highlight {
    color: #6EE7B7;
    border-color: rgba(16, 185, 129, 0.4);
    background: rgba(6, 78, 59, 0.3);
  }

  /* Bottom Pill Bar */
  .footer-pills {
    margin-top: 36px;
    display: flex;
    align-items: center;
    gap: 24px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #64748B;
    z-index: 10;
  }
</style>
</head>
<body>
  <div class="grid-pattern"></div>

  <div class="header-section">
    <div class="top-banner">
      Problem Statement &bull; SIH26236 (Software / Agri-FoodTech)
    </div>
    <h1 class="slide-title">
      Bridging Grassroots Food Processing &amp; Industrial Packaging Law
    </h1>
    <p class="slide-subtitle">
      Ministry of Food Processing Industries (MoFPI) &bull; National PMFME &amp; ODOP Digital Acceleration
    </p>
  </div>

  <div class="cards-grid">
    <!-- Card A: Ministry Ask -->
    <div class="comp-card card-a">
      <div>
        <div class="card-header">
          <div class="card-badge">
            <div class="card-indicator"></div>
            <span>Card A &bull; The Ministry Ask</span>
          </div>
          <h2 class="card-title">Institutional Mandate</h2>
          <div class="card-tag">MoFPI PMFME &amp; ODOP Mission</div>
        </div>
        <p class="card-body">
          Direct mandate to support <strong>2 Lakh+ micro-processors</strong>: Scientifically recommend food-grade packaging polymers, laminate thickness, OTR/WVTR barrier thresholds, and MAP gas mixtures based on crop chemistry.
        </p>
      </div>
      <div class="card-highlight">
        &bull; Objective: Zero guesswork in food-contact packaging material selection for rural SHGs &amp; FPOs.
      </div>
    </div>

    <!-- Card B: Grassroots Reality -->
    <div class="comp-card card-b">
      <div>
        <div class="card-header">
          <div class="card-badge">
            <div class="card-indicator"></div>
            <span>Card B &bull; Grassroots Reality</span>
          </div>
          <h2 class="card-title">Severe Spoilage &amp; Penalties</h2>
          <div class="card-tag">Up to 30% Post-Harvest Loss</div>
        </div>
        <p class="card-body">
          Rural food enterprises lose <strong>up to 30% of agricultural produce</strong> due to empirical packaging. They face severe <strong>FSSAI regulatory penalties and export rejections</strong> because professional packaging consultants are unaffordable.
        </p>
      </div>
      <div class="card-highlight">
        &bull; Bottleneck: High post-harvest losses &amp; FSSAI non-compliance due to lack of accessible tools.
      </div>
    </div>

    <!-- Card C: PackAI Solution -->
    <div class="comp-card card-c">
      <div>
        <div class="card-header">
          <div class="card-badge">
            <div class="card-indicator"></div>
            <span>Card C &bull; The PackAI Solution</span>
          </div>
          <h2 class="card-title">PackAI India Engine</h2>
          <div class="card-tag">Deterministic &bull; Offline &bull; Compliant</div>
        </div>
        <p class="card-body">
          India's first <strong>offline-first, bilingual decision engine</strong> bridging biophysical shelf-life kinetics directly with mandatory <strong>FSSAI 2018, BIS IS 10146, and CPCB-EPR</strong> statutory compliance with instant 1-click A4 PDF certificates.
        </p>
      </div>
      <div class="card-highlight">
        &bull; Breakthrough: Instant scientific laminate synthesis &amp; pre-print label auditing for any rural processor.
      </div>
    </div>
  </div>

  <div class="footer-pills">
    <span>100% Deterministic Biophysics</span>
    <span>&bull;</span>
    <span>Zero Cloud Dependency</span>
    <span>&bull;</span>
    <span>Complete Legal &amp; Migration Traceability</span>
  </div>
</body>
</html>
"""


async def render_slides():
    from playwright.async_api import async_playwright

    print("Rendering high-resolution intro slides (1920x1080)...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )

        # 1. Slide 1 (Team & Project Slate)
        page1 = await browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        await page1.set_content(SLIDE1_HTML)
        await page1.wait_for_timeout(300)
        await page1.screenshot(path=str(SLIDE1_PATH), type="png")
        await page1.close()
        print(f"[OK] Slide 1 (Team Slate) saved to: {SLIDE1_PATH} ({SLIDE1_PATH.stat().st_size / 1024:.1f} KB)")

        # 2. Slide 2 (Problem Statement Breakdown)
        page2 = await browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        await page2.set_content(SLIDE2_HTML)
        await page2.wait_for_timeout(300)
        await page2.screenshot(path=str(SLIDE2_PATH), type="png")
        await page2.close()
        print(f"[OK] Slide 2 (Problem Statement) saved to: {SLIDE2_PATH} ({SLIDE2_PATH.stat().st_size / 1024:.1f} KB)")

        await browser.close()


def main():
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    asyncio.run(render_slides())


if __name__ == "__main__":
    main()
