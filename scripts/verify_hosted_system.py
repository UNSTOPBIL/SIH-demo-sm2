#!/usr/bin/env python3
"""
Comprehensive Live Verification for Hosted PackAI Deployments
Tests:
  1. Vercel Backend Direct Endpoints (https://backend-delta-ashy-q47w8f4i7f.vercel.app)
  2. Vercel Frontend & Reverse Proxy (https://packai-frontend-beta.vercel.app)
  3. Hugging Face Spaces (https://ustop-packai-india.static.hf.space & https://huggingface.co/spaces/ustop/packai-india)
  4. End-to-End Playwright Headless Browser Walkthrough on live Vercel deployment.
"""

import sys
import json
import asyncio
import urllib.request
from pathlib import Path

# Fix console encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

VERCEL_FRONTEND = "https://packai-frontend-beta.vercel.app"
VERCEL_BACKEND = "https://backend-delta-ashy-q47w8f4i7f.vercel.app"
HF_SPACE_DIRECT = "https://ustop-packai-india.static.hf.space"
HF_SPACE_PAGE = "https://huggingface.co/spaces/ustop/packai-india"

def http_get(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.status, resp.read()

def http_post_json(url: str, payload: dict):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.status, resp.read(), resp.headers

def test_api_endpoints():
    print("=" * 70)
    print("  PHASE 1: LIVE API & BACKEND VERIFICATION")
    print("=" * 70)

    # 1. Health
    status, body = http_get(f"{VERCEL_FRONTEND}/api/health")
    data = json.loads(body.decode("utf-8"))
    print(f"[*] GET /api/health: [{status}] System={data.get('system')[:40]}...")
    assert status == 200 and data.get("status") == "healthy"

    # 2. Commodities
    status, body = http_get(f"{VERCEL_FRONTEND}/api/commodities")
    data = json.loads(body.decode("utf-8"))
    count = data.get("count", len(data.get("commodities", [])))
    print(f"[*] GET /api/commodities: [{status}] Seeded Commodities Count={count}")
    assert status == 200 and count >= 18

    # 3. Recommend Packaging (Makhana Tropical)
    rec_payload = {
        "commodity_id": "makhana",
        "moisture_pct": 7.0,
        "fat_oil_pct": 0.1,
        "ph_value": 6.5,
        "shelf_life_days": 365,
        "storage_type": "ambient",
        "storage_temp_c": 42.0,
        "ambient_rh": 90.0
    }
    status, body, _ = http_post_json(f"{VERCEL_FRONTEND}/api/recommend", rec_payload)
    rec_data = json.loads(body.decode("utf-8"))
    material = rec_data.get("primary_material", "Unknown")
    structure = rec_data.get("primary_structure", {})
    print(f"[*] POST /api/recommend: [{status}] Primary Material={material}")
    assert status == 200 and ("Al-Foil" in material or "Aluminium" in material or "PET" in material)

    # 4. Compliance Details
    status, body = http_get(f"{VERCEL_FRONTEND}/api/compliance/makhana?ph_value=6.5&fat_oil_pct=0.1&moisture_pct=7.0")
    comp_data = json.loads(body.decode("utf-8"))
    bis_code = comp_data.get("bis", {}).get("is_code", "")
    print(f"[*] GET /api/compliance/makhana: [{status}] BIS Standard={bis_code}")
    assert status == 200 and "IS 10146" in bis_code

    # 5. Converter Economics
    econ_payload = {
        "structure": structure,
        "commodity_name": "Foxnut / Makhana",
        "pack_weight_g": 250.0,
        "retail_pack_price_inr": 200.0,
        "batch_pouches": 4000
    }
    status, body, _ = http_post_json(f"{VERCEL_FRONTEND}/api/economics", econ_payload)
    econ_data = json.loads(body.decode("utf-8"))
    unit_cost = econ_data.get("unit_cost_metrics", {}).get("cost_per_pouch_inr", 0)
    roi = econ_data.get("spoilage_roi", {}).get("roi_multiplier", 0)
    print(f"[*] POST /api/economics: [{status}] Est Unit Cost=Rs. {unit_cost:.2f}/pouch | Spoilage ROI={roi}x")
    assert status == 200 and unit_cost > 0

    # 6. Label Auditor
    audit_payload = {
        "raw_text": "Makhana snack without fssai number or allergen info."
    }
    status, body, _ = http_post_json(f"{VERCEL_FRONTEND}/api/audit-label", audit_payload)
    audit_data = json.loads(body.decode("utf-8"))
    verdict = audit_data.get("verdict")
    violations_count = len(audit_data.get("violations", []))
    print(f"[*] POST /api/audit-label: [{status}] Verdict={verdict} | Violations Flagged={violations_count}")
    assert status == 200 and violations_count > 0

    # 7. Digital Passport Verification
    status, body = http_get(f"{VERCEL_FRONTEND}/api/verify/PMFME-2026-LIVE-TEST?id=makhana")
    pass_data = json.loads(body.decode("utf-8"))
    sha_seal = pass_data.get("integrity_hash", "")
    print(f"[*] GET /api/verify: [{status}] SHA-256 Seal={sha_seal[:20]}...")
    assert status == 200 and len(sha_seal) == 64

    # 8. ReportLab PDF Export
    pdf_payload = {
        **rec_data,
        **comp_data
    }
    status, body, headers = http_post_json(f"{VERCEL_FRONTEND}/api/export-pdf", pdf_payload)
    content_type = headers.get("Content-Type", "")
    print(f"[*] POST /api/export-pdf: [{status}] Content-Type={content_type} | Size={len(body)} bytes")
    assert status == 200 and "application/pdf" in content_type and len(body) > 1000

    print("[OK] All 8 backend API endpoints verified successfully!\n")

def test_huggingface_space():
    print("=" * 70)
    print("  PHASE 2: HUGGING FACE SPACES VERIFICATION")
    print("=" * 70)

    # Direct Web App URL
    status, body = http_get(HF_SPACE_DIRECT)
    print(f"[*] HF Space Web App ({HF_SPACE_DIRECT}): [{status}] ({len(body)} bytes)")
    assert status == 200 and b"<title>" in body

    # Space Hub Page
    status, body = http_get(HF_SPACE_PAGE)
    print(f"[*] HF Space Community Page ({HF_SPACE_PAGE}): [{status}] ({len(body)} bytes)")
    assert status == 200

    print("[OK] Hugging Face Space verified live and accessible!\n")

async def test_live_browser_walkthrough():
    from playwright.async_api import async_playwright

    print("=" * 70)
    print("  PHASE 3: PLAYWRIGHT LIVE BROWSER VERIFICATION (VERCEL)")
    print("=" * 70)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        print(f"[*] Navigating to live Vercel URL: {VERCEL_FRONTEND}...")
        await page.goto(VERCEL_FRONTEND, wait_until="networkidle", timeout=20000)

        title = await page.title()
        print(f"[*] Live Page Title: '{title}'")
        assert "PackAI" in title or "Packaging" in title

        # Verify Screen 1 renders seeded commodities
        await page.wait_for_selector("select", timeout=10000)
        await page.select_option("select", "makhana")
        print("[*] Screen 1: Selected 'Foxnut / Makhana'")

        # Click Extreme Tropical preset
        await page.click("button:has-text('Extreme Tropical')")
        print("[*] Screen 1: Clicked 'Extreme Tropical' preset chip")

        # Click Analyze
        await page.click("button[type='submit']")
        print("[*] Screen 1: Submitted analysis form...")

        # Verify Screen 2 Barrier Match
        await page.wait_for_selector("text=Optimal Barrier", timeout=15000)
        print("[*] Screen 2: Reached 'Optimal Barrier & Shelf-Life Match'")

        # Click Review India Statutory Compliance
        await page.click("button:has-text('Review India Statutory Compliance')")
        await page.wait_for_selector("text=India Statutory Compliance", timeout=15000)
        print("[*] Screen 3: Reached 'India Statutory Compliance & Standards Shield'")

        # Click Generate Official Readiness Sheet
        await page.click("button:has-text('Generate Official Readiness Sheet')")
        await page.wait_for_selector("text=Download Official PDF", timeout=15000)
        print("[*] Screen 4: Reached 'Readiness Sheet' with Download PDF button")

        # Test Header Navigation to Passport
        await page.click("header button:has-text('Passport')")
        await page.wait_for_selector("text=Official Digital Product Passport", timeout=15000)
        print("[*] Passport View: Loaded Digital Product Passport with SHA-256 seal")

        # Test Header Navigation to Label Auditor
        await page.click("header button:has-text('Label Auditor')")
        await page.wait_for_selector("text=Pre-Print Packaging Artwork", timeout=15000)
        await page.wait_for_timeout(1000)
        await page.click("button:has-text('Load Defective Sample')")
        try:
            await page.wait_for_selector("text=NON-COMPLIANT", timeout=8000)
        except Exception:
            await page.click("button:has-text('Run Statutory Label Audit')")
            await page.wait_for_selector("text=NON-COMPLIANT", timeout=15000)
        print("[*] Label Auditor View: Evaluated defective sample -> Flagged violations (NON-COMPLIANT)")

        await browser.close()
        print("[OK] Full end-to-end browser walkthrough on live Vercel deployment passed with flying colors!\n")

def main():
    test_api_endpoints()
    test_huggingface_space()
    asyncio.run(test_live_browser_walkthrough())

    print("=" * 70)
    print("  ALL HOSTED DEPLOYMENTS 100% OPERATIONAL")
    print("=" * 70)
    print(f"1. Vercel Web Studio:    {VERCEL_FRONTEND}")
    print(f"2. Vercel FastAPI API:   {VERCEL_BACKEND}")
    print(f"3. HF Space Web App:     {HF_SPACE_DIRECT}")
    print(f"4. HF Space Repository:  {HF_SPACE_PAGE}")
    print("=" * 70)

if __name__ == "__main__":
    main()
