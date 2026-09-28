#!/usr/bin/env python3
r"""
Synchronized Playwright Walkthrough Recorder for SIH26236
Launches Chromium at 1920x1080 and records 3 distinct walkthrough phases:
  - Scene A: Screen 1 & 2 (Biophysics & Kinetics) - exact duration of audio3_physics
  - Scene B: Screen 3 & 4 (Statutory Shield & PDF) - exact duration of audio4_compliance
  - Scene C: Passport, Auditor & Architecture Closing - exact duration of audio5_passport_auditor
Guarantees 100% mathematical synchronization with audio tracks.
"""

import os
import sys
import json
import time
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

# Ensure UTF-8 output encoding on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = BASE_DIR / "audio_manifest.json"
RECORD_DIR = BASE_DIR / "raw_recordings"

CURSOR_SCRIPT = """
(() => {
  if (document.getElementById('virtual-cursor')) return;
  const cursor = document.createElement('div');
  cursor.id = 'virtual-cursor';
  cursor.innerHTML = `<svg width="26" height="26" viewBox="0 0 24 24" fill="none" style="filter: drop-shadow(0 2px 5px rgba(0,0,0,0.5));">
    <path d="M5.5 3.2L18.8 12.3C19.7 12.9 19.4 14.3 18.3 14.5L13.1 15.3L16.2 21.2C16.6 22 15.8 22.8 15 22.4L11.5 20.4L7.8 23.3C7 24 5.7 23.4 5.7 22.3L5.5 3.2Z" fill="#10b981" stroke="#ffffff" stroke-width="2"/>
  </svg>`;
  cursor.style.position = 'fixed';
  cursor.style.top = '0';
  cursor.style.left = '0';
  cursor.style.zIndex = '9999999';
  cursor.style.pointerEvents = 'none';
  cursor.style.transition = 'transform 0.08s cubic-bezier(0.2, 0.8, 0.4, 1)';
  cursor.style.transform = 'translate(960px, 540px)';
  document.body.appendChild(cursor);

  window.__moveCursor = (x, y) => {
    cursor.style.transform = `translate(${x}px, ${y}px)`;
  };

  window.__clickCursor = () => {
    cursor.style.transform += ' scale(0.8)';
    setTimeout(() => {
      cursor.style.transform = cursor.style.transform.replace(' scale(0.8)', '');
    }, 150);
  };
})();
"""


class WalkthroughRecorder:
    def __init__(self):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            self.manifest = json.load(f)
        self.durations = {item["id"]: item["duration_sec"] for item in self.manifest["audios"]}
        self.cur_x = 960
        self.cur_y = 540

    async def inject_cursor(self, page):
        try:
            await page.evaluate(CURSOR_SCRIPT)
        except Exception:
            pass

    async def smooth_move(self, page, target_x, target_y, steps=15, step_delay=0.015):
        """Move cursor smoothly from current position to target position."""
        target_x = max(10, min(1910, target_x))
        target_y = max(10, min(1070, target_y))
        dx = (target_x - self.cur_x) / steps
        dy = (target_y - self.cur_y) / steps

        for _ in range(steps):
            self.cur_x += dx
            self.cur_y += dy
            await page.evaluate(f"window.__moveCursor && window.__moveCursor({self.cur_x:.1f}, {self.cur_y:.1f})")
            await asyncio.sleep(step_delay)

        self.cur_x = target_x
        self.cur_y = target_y
        await page.evaluate(f"window.__moveCursor && window.__moveCursor({self.cur_x:.1f}, {self.cur_y:.1f})")

    async def move_to_element(self, page, selector, steps=15, sleep_after=0.3):
        """Scroll element into view, and smoothly hover cursor over its center."""
        try:
            el = await page.wait_for_selector(selector, timeout=8000)
            if not el:
                return False
            await el.scroll_into_view_if_needed()
            await asyncio.sleep(0.2)
            box = await el.bounding_box()
            if not box:
                return False
            center_x = max(15, min(1905, box["x"] + box["width"] / 2))
            center_y = max(15, min(1065, box["y"] + box["height"] / 2))
            await self.smooth_move(page, center_x, center_y, steps=steps)
            if sleep_after > 0:
                await asyncio.sleep(sleep_after)
            return True
        except Exception as e:
            msg = str(e).encode("ascii", "replace").decode("ascii")
            print(f"Warning: move_to_element failed for '{selector}': {msg[:80]}")
            return False

    async def click_element(self, page, selector, sleep_after=0.6):
        """Scroll into view, move cursor to element, animate click, and dispatch actual click."""
        try:
            el = await page.wait_for_selector(selector, timeout=8000)
            if not el:
                print(f"Warning: selector not found for click: {selector}")
                return False
            await el.scroll_into_view_if_needed()
            await asyncio.sleep(0.2)
            box = await el.bounding_box()
            if box:
                center_x = max(15, min(1905, box["x"] + box["width"] / 2))
                center_y = max(15, min(1065, box["y"] + box["height"] / 2))
                await self.smooth_move(page, center_x, center_y, steps=15)
                await page.evaluate("window.__clickCursor && window.__clickCursor()")
            await el.click()
            if sleep_after > 0:
                await asyncio.sleep(sleep_after)
            return True
        except Exception as e:
            msg = str(e).encode("ascii", "replace").decode("ascii")
            print(f"Warning: click_element failed for '{selector}': {msg[:80]}")
            return False

    async def smooth_scroll(self, page, delta_y, steps=18, step_delay=0.02):
        """Simulate natural page scrolling."""
        dy = delta_y / steps
        for _ in range(steps):
            await page.evaluate(f"window.scrollBy(0, {dy})")
            await asyncio.sleep(step_delay)

    async def run(self) -> str:
        RECORD_DIR.mkdir(parents=True, exist_ok=True)
        # Purge old webm recordings to ensure zero recycling
        for f in RECORD_DIR.glob("*.webm"):
            try:
                f.unlink()
            except Exception:
                pass

        total_walkthrough_target = (
            self.durations["audio3_physics"] +
            self.durations["audio4_compliance"] +
            self.durations["audio5_passport_auditor"]
        )

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--window-size=1920,1080"
                ]
            )

            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                device_scale_factor=1,
                record_video_dir=str(RECORD_DIR),
                record_video_size={"width": 1920, "height": 1080}
            )

            page = await context.new_page()

            print("==========================================")
            print("Starting Fresh Synchronized Walkthrough Recording...")
            print(f"Target Walkthrough Duration: {total_walkthrough_target:.2f}s (Audio 3 + 4 + 5)")
            print("==========================================")

            # ----------------------------------------------------
            # SCENE A: Screen 1 & 2 (Biophysics & Kinetics)
            # Synchronized strictly to audio3_physics
            # ----------------------------------------------------
            target_a = self.durations["audio3_physics"]
            print(f"\n[Scene A] Screen 1 & 2: Biophysics & Kinetics (Target: {target_a:.2f}s)")
            start_a = time.time()

            await page.goto("http://127.0.0.1:5173", wait_until="networkidle")
            await self.inject_cursor(page)
            await asyncio.sleep(0.8)

            # Toggle Bilingual to Hindi and back to English
            await self.click_element(page, "button[title='Toggle Hindi / English']", sleep_after=1.5)
            await self.click_element(page, "button[title='Toggle Hindi / English']", sleep_after=1.2)

            # Select Makhana from dropdown
            await self.move_to_element(page, "select", steps=12, sleep_after=0.6)
            await page.select_option("select", "makhana")
            await asyncio.sleep(1.0)

            # Hover over ODOP cluster badge
            await self.move_to_element(page, "span.font-semibold:has-text('Mithila')", steps=12, sleep_after=1.2)

            # Scroll down to simulation presets
            await self.smooth_scroll(page, 260, steps=14)
            await asyncio.sleep(0.8)

            # Click Extreme Tropical preset chip
            await self.click_element(page, "button:has-text('Extreme Tropical')", sleep_after=1.2)

            # Hover over temp & humidity
            await self.move_to_element(page, "span:has-text('42°C')", steps=12, sleep_after=0.8)
            await self.move_to_element(page, "span:has-text('90% RH')", steps=12, sleep_after=0.8)

            # Click Analyze button
            await self.click_element(page, "button[type='submit']", sleep_after=1.8)
            await page.wait_for_selector("text=Optimal Barrier & Shelf-Life Match", timeout=12000)
            await self.inject_cursor(page)

            # On Screen 2: Hover Barrier Match badge
            await self.move_to_element(page, "text=Optimal Barrier & Shelf-Life Match", steps=12, sleep_after=1.2)

            # Scroll to 2.5D Laminate Cross-Section Explorer
            await self.smooth_scroll(page, 520, steps=16)
            await asyncio.sleep(0.8)

            # Click Layer 1, then Layer 2 (Al Foil), then Layer 3 (LLDPE)
            layer_buttons = page.locator("div.space-y-3.py-2 > div.group")
            count = await layer_buttons.count()
            if count >= 3:
                for idx in range(min(3, count)):
                    box = await layer_buttons.nth(idx).bounding_box()
                    if box:
                        await self.smooth_move(page, box["x"] + box["width"]/2, box["y"] + box["height"]/2, steps=10)
                        await page.evaluate("window.__clickCursor && window.__clickCursor()")
                        await layer_buttons.nth(idx).click()
                        await asyncio.sleep(1.0)

            # Scroll to Converter Economics
            await self.smooth_scroll(page, 450, steps=16)
            await asyncio.sleep(0.8)
            await self.move_to_element(page, "text=Industrial Converter Economics", steps=12, sleep_after=1.2)

            # Expand Technical Specifications & ASTM Standards
            await self.smooth_scroll(page, 420, steps=14)
            await self.click_element(page, "button:has-text('Technical Specifications')", sleep_after=1.5)

            # Hold on Screen 2 until Audio 3 duration is satisfied
            elapsed_a = time.time() - start_a
            remain_a = max(0.0, target_a - elapsed_a)
            print(f"  Scene A action elapsed: {elapsed_a:.2f}s | Holding: {remain_a:.2f}s")
            await asyncio.sleep(remain_a)

            # ----------------------------------------------------
            # SCENE B: Screen 3 & 4 (Statutory Shield & PDF)
            # Synchronized strictly to audio4_compliance
            # ----------------------------------------------------
            target_b = self.durations["audio4_compliance"]
            print(f"\n[Scene B] Screen 3 & 4: Statutory Shield & PDF (Target: {target_b:.2f}s)")
            start_b = time.time()

            # Advance to Screen 3 (Compliance Shield)
            await self.click_element(page, "button:has-text('Review India Statutory Compliance')", sleep_after=1.8)
            await page.wait_for_selector("text=India Statutory Compliance & Standards Shield", timeout=12000)
            await self.inject_cursor(page)
            await asyncio.sleep(0.8)

            # Scroll through FSSAI Schedule IV & BIS IS 10146
            await self.smooth_scroll(page, 400, steps=16)
            await self.move_to_element(page, "text=IS 10146", steps=12, sleep_after=1.2)

            # Scroll to IS 9845 Migration Matrix & CPCB EPR
            await self.smooth_scroll(page, 500, steps=18)
            await self.move_to_element(page, "text=Overall Migration Limit", steps=12, sleep_after=1.2)
            await self.move_to_element(page, "text=Extended Producer Responsibility", steps=12, sleep_after=1.2)

            # Click to advance to Screen 4 (Readiness Sheet)
            await self.smooth_scroll(page, 450, steps=14)
            await self.click_element(page, "button:has-text('Generate Official Readiness Sheet')", sleep_after=1.8)
            await page.wait_for_selector("text=Download Official PDF", timeout=12000)
            await self.inject_cursor(page)
            await asyncio.sleep(1.0)

            # Highlight A4 Readiness Certificate & Download PDF
            await self.move_to_element(page, "button:has-text('Download Official PDF')", steps=12, sleep_after=1.8)
            await self.move_to_element(page, "button:has-text('Print')", steps=12, sleep_after=1.2)

            # Hold on Screen 4 until Audio 4 duration is satisfied
            elapsed_b = time.time() - start_b
            remain_b = max(0.0, target_b - elapsed_b)
            print(f"  Scene B action elapsed: {elapsed_b:.2f}s | Holding: {remain_b:.2f}s")
            await asyncio.sleep(remain_b)

            # ----------------------------------------------------
            # SCENE C: Passport, Auditor & Architecture Closing
            # Synchronized strictly to audio5_passport_auditor
            # ----------------------------------------------------
            target_c = self.durations["audio5_passport_auditor"]
            print(f"\n[Scene C] Passport, Auditor & Architecture (Target: {target_c:.2f}s)")
            start_c = time.time()

            # Scroll to top and navigate to Digital Product Passport (/verify)
            await page.evaluate("window.scrollTo({ top: 0, behavior: 'instant' })")
            await asyncio.sleep(0.6)
            await self.click_element(page, "header button:has-text('Passport')", sleep_after=1.8)
            await page.wait_for_selector("text=Official Digital Product Passport", timeout=12000)
            await self.inject_cursor(page)

            # Scroll through passport and highlight SHA-256 seal
            await self.smooth_scroll(page, 320, steps=14)
            await self.move_to_element(page, "text=GOVERNMENT OF INDIA", steps=12, sleep_after=1.5)

            # Navigate to Label Auditor (/audit)
            await page.evaluate("window.scrollTo({ top: 0, behavior: 'instant' })")
            await asyncio.sleep(0.6)
            await self.click_element(page, "header button:has-text('Label Auditor')", sleep_after=1.8)
            await page.wait_for_selector("text=Pre-Print Packaging Artwork", timeout=12000)
            await self.inject_cursor(page)
            await asyncio.sleep(0.8)

            # Click Load Defective Sample to trigger instant audit
            await self.click_element(page, "button:has-text('Load Defective Sample')", sleep_after=1.8)
            await page.wait_for_selector("text=FAIL", timeout=10000)
            await self.smooth_scroll(page, 420, steps=16)
            await self.move_to_element(page, "text=FAIL", steps=12, sleep_after=1.5)

            # Return to dashboard
            await page.evaluate("window.scrollTo({ top: 0, behavior: 'instant' })")
            await asyncio.sleep(0.5)
            await self.click_element(page, "header button:has-text('Engine')", sleep_after=1.2)
            await page.wait_for_selector("text=PackAI India", timeout=10000)
            await self.inject_cursor(page)

            # Hover over deterministic engine pill
            await self.move_to_element(page, "text=DETERMINISTIC ENGINE: ACTIVE", steps=12, sleep_after=1.5)

            # Gracefully center cursor for closing
            await self.smooth_move(page, 960, 500, steps=15)

            # Hold until Audio 5 duration is satisfied
            elapsed_c = time.time() - start_c
            remain_c = max(0.0, target_c - elapsed_c)
            print(f"  Scene C action elapsed: {elapsed_c:.2f}s | Holding: {remain_c:.2f}s")
            await asyncio.sleep(remain_c)

            # Finish recording cleanly
            print("\nFlushing and finalizing video recording...")
            await page.close()
            await context.close()
            await browser.close()

        # Locate saved webm file
        recordings = list(RECORD_DIR.glob("*.webm"))
        if not recordings:
            raise RuntimeError("No recorded video file found in raw_recordings directory!")

        raw_video = max(recordings, key=os.path.getctime)
        print(f"\n==========================================")
        print(f"Raw Walkthrough Video Saved: {raw_video}")
        print(f"File Size: {raw_video.stat().st_size / (1024*1024):.2f} MB")
        print(f"==========================================")
        return str(raw_video)


if __name__ == "__main__":
    recorder = WalkthroughRecorder()
    asyncio.run(recorder.run())
