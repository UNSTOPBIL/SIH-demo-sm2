import sys
import os
import math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
import fitz  # PyMuPDF
from backend.main import app
from backend.engine.physics_engine import (
    calculate_target_wvtr,
    calculate_target_otr,
    solve_optimal_laminate,
    get_is9845_simulant_matrix
)
from backend.engine.pdf_generator import generate_packaging_readiness_pdf

client = TestClient(app)

def run_stress_test_suite():
    print("=" * 70)
    print("SIH26236 FULL-SYSTEM STRESS TEST & RESILIENCE RUNNER")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. Hyper-Tropical Climate Stress (48°C, 98% RH, 730 days)
    # -------------------------------------------------------------
    print("\n[TEST 1] Hyper-Tropical Climate Stress (48°C, 98% RH, 730 days)...")
    wvtr_res = calculate_target_wvtr(
        moisture_pct=6.5,
        shelf_life_days=730,
        storage_temp_c=48.0,
        ambient_rh=0.98
    )
    assert wvtr_res["target_wvtr"] > 0, "WVTR must be positive"
    assert math.isfinite(wvtr_res["target_wvtr"]), "WVTR must be finite"
    assert wvtr_res["saturation_pressure_kpa"] > 10.0, "ps(48C) must exceed 10 kPa"
    
    sol = solve_optimal_laminate(
        target_wvtr=wvtr_res["target_wvtr"],
        target_otr=1.0,
        commodity_id="makhana",
        moisture_pct=6.5,
        fat_oil_pct=0.2,
        ph_value=6.5,
        storage_type="ambient",
        respiration_class="Very Low"
    )
    assert sol["primary_structure"] is not None, "Primary structure must resolve"
    assert sol["alt_structure"] is not None, "Alt structure must resolve"
    assert "foil" in sol["primary_structure"]["id"] or sol["primary_structure"]["wvtr"] <= 0.5, "Must select highest barrier"
    print(f"    -> Passed! Target WVTR: {wvtr_res['target_wvtr']} g/m2/day. Solved: {sol['primary_structure']['name']}")
    if sol.get("warning_flag"):
        print(f"    -> Structured Warning Triggered: {sol['warning_flag'][:65]}...")

    # -------------------------------------------------------------
    # 2. Inverted / Equal Moisture Boundary (M0 >= Mc)
    # -------------------------------------------------------------
    print("\n[TEST 2] Inverted / Equal Moisture Boundary (M0 >= Mc)...")
    # Initial moisture = 16.0% which triggers Mc = min(0.20, (16+3.5)/100) = 19.5%
    # Test equal: moisture_pct = 15.0 vs 15.0
    wvtr_inverted = calculate_target_wvtr(
        moisture_pct=15.0,
        shelf_life_days=180,
        storage_temp_c=30.0,
        ambient_rh=0.45  # ambient RH equals internal aw (45%)
    )
    assert wvtr_inverted["target_wvtr"] >= 0.02, "Target WVTR must have a safe lower clamp floor"
    assert math.isfinite(wvtr_inverted["target_wvtr"]), "Must be finite, no zero-division"
    assert wvtr_inverted["delta_m_water_g"] > 0, "Moisture delta must be guarded > 0"
    print(f"    -> Passed! Target WVTR safely guarded: {wvtr_inverted['target_wvtr']} g/m2/day (Delta: {wvtr_inverted['delta_m_water_g']}g)")

    # -------------------------------------------------------------
    # 3. Extreme Lipid Oxidation (99.9% fat at 45°C)
    # -------------------------------------------------------------
    print("\n[TEST 3] Extreme Lipid Oxidation (99.9% fat at 45°C)...")
    otr_extreme_fat = calculate_target_otr(
        fat_oil_pct=99.9,
        shelf_life_days=365,
        respiration_class="Very Low",
        storage_temp_c=45.0
    )
    assert otr_extreme_fat["target_otr"] <= 1.5, f"Pure lipid fat target OTR must be < 1.5 cc/m2/day, got {otr_extreme_fat['target_otr']}"
    assert otr_extreme_fat["target_otr"] >= 0.05, "Target OTR lower clamp floor intact"
    
    sol_fat = solve_optimal_laminate(
        target_wvtr=0.1,
        target_otr=otr_extreme_fat["target_otr"],
        commodity_id="ghee",
        moisture_pct=0.2,
        fat_oil_pct=99.9,
        ph_value=6.5,
        storage_type="ambient",
        respiration_class="Very Low"
    )
    # Prioritizes Al-foil or tinplate canister
    assert any(k in sol_fat["primary_structure"]["id"] for k in ["foil", "tinplate", "evoh"]), "High-barrier laminate must be selected"
    print(f"    -> Passed! Target OTR: {otr_extreme_fat['target_otr']} cc/m2/day. Selected: {sol_fat['primary_structure']['name']}")

    # -------------------------------------------------------------
    # 4. Respiration & Perishability Edge Cases (High Respiration at 35°C)
    # -------------------------------------------------------------
    print("\n[TEST 4] Respiration & Perishability Edge Cases (Produce at 35°C)...")
    otr_resp = calculate_target_otr(
        fat_oil_pct=0.4,
        shelf_life_days=14,
        respiration_class="Extremely High",
        storage_temp_c=35.0
    )
    assert otr_resp["is_produce"] is True, "Must be flagged as fresh produce"
    assert math.isfinite(otr_resp["target_otr"]), "Q10 rate must not overflow"
    assert otr_resp["target_otr"] >= 2500.0, "Must require breathable film"
    
    sol_resp = solve_optimal_laminate(
        target_wvtr=50.0,
        target_otr=otr_resp["target_otr"],
        commodity_id="button_mushroom",
        moisture_pct=92.0,
        fat_oil_pct=0.4,
        ph_value=6.2,
        storage_type="ambient",
        respiration_class="Extremely High"
    )
    assert any(k in sol_resp["primary_structure"]["id"] for k in ["microperf", "vented", "tray"]), "Must select breathable EMAP format"
    print(f"    -> Passed! Respiration rate: {otr_resp['respiration_rate_mg_kg_hr']} mg CO2/kg-hr. Selected: {sol_resp['primary_structure']['name']}")

    # -------------------------------------------------------------
    # 5. Unseeded / Arbitrary Custom Commodities (API endpoints)
    # -------------------------------------------------------------
    print("\n[TEST 5] Unseeded / Arbitrary Custom Commodities via API...")
    custom_payload = {
        "commodity_id": "custom_dragonfruit",
        "commodity_name": "Exotic Pitaya / Dragonfruit",
        "moisture_pct": 87.0,
        "fat_oil_pct": 25.0,
        "ph_value": 3.2,
        "shelf_life_days": 60,
        "storage_type": "chilled",
        "storage_temp_c": 8.0,
        "ambient_rh": 85.0
    }
    # 5a: Recommend endpoint
    r_rec = client.post("/api/recommend", json=custom_payload)
    assert r_rec.status_code == 200, f"Recommend endpoint failed: {r_rec.text}"
    rec_json = r_rec.json()
    assert "Custom: Custom Dragonfruit" in rec_json["name_en"]
    assert rec_json["primary_material"] is not None
    assert "physics_metrics" in rec_json
    print(f"    -> /api/recommend 200 OK! Assigned Primary: {rec_json['primary_material']}")

    # 5b: Compliance endpoint
    r_comp = client.get("/api/compliance/custom_dragonfruit?ph_value=3.2&fat_oil_pct=25.0&moisture_pct=87.0")
    assert r_comp.status_code == 200, f"Compliance endpoint failed: {r_comp.text}"
    comp_json = r_comp.json()
    assert "Acidic" in comp_json["fssai"]["schedule_iv_category"] or "Preserves" in comp_json["fssai"]["schedule_iv_category"], "Must map acidic schedule"
    # Check that Simulant B is applicable (pH 3.2 < 4.5)
    sims = comp_json["simulant_protocol"]["simulants"]
    sim_b = next((s for s in sims if "Simulant B" in s["code"]), None)
    assert sim_b is not None and sim_b["applicable"] is True, "Simulant B must be mandatory for pH 3.2"
    # Check that Simulant D is applicable (Fat 25% > 5%)
    sim_d = next((s for s in sims if "Simulant D" in s["code"]), None)
    assert sim_d is not None and sim_d["applicable"] is True, "Simulant D must be mandatory for 25% fat"
    print(f"    -> /api/compliance 200 OK! Mapped: {comp_json['fssai']['schedule_iv_category']}")

    # -------------------------------------------------------------
    # 6. ReportLab 1-Page Constraint Under Extreme Text Overflow
    # -------------------------------------------------------------
    print("\n[TEST 6] ReportLab 1-Page Constraint Under Extreme Text Overflow (300+ chars)...")
    massive_text_payload = {
        "commodity_id": "test_massive_overflow",
        "name_en": "Super Ultra Premium Extra Virgin Cold-Pressed Micro-Encapsulated Nutritive Functional Snack Bar " * 4, # 400+ chars
        "odop_region": "International Export Quality Special Agricultural Economic Zone Cluster Division " * 3, # 250+ chars
        "category": "High-Value Value-Added Export-Oriented Nutrient-Dense Organic Agro-Commodity Cluster",
        "primary_material": "Bio-Composite Multi-Layer Nano-Cellulose EVOH Co-Extruded Laminate Web " * 2,
        "alternative_material": "100% Industrially Compostable Marine-Degradable Bio-PBS/PLA Barrier Polymer",
        "moisture_pct": 14.5,
        "fat_oil_pct": 18.2,
        "ph_value": 4.1,
        "shelf_life_days": 365,
        "storage_type": "ambient",
        "storage_temp_c": 35.0,
        "ambient_rh": 80.0,
        "why_material_en": "This revolutionary food packaging solution is engineered to mitigate extreme auto-oxidation kinetics, moisture vapor ingress, and microbial proliferation under aggressive tropical supply chain environments with complete circular recyclability. " * 3, # 650+ chars
        "fssai_schedule": "Schedule IV (Confectionery, Ready-to-Eat Savouries & Packaged Snacks with Lipid Emulsions) & Schedule III",
        "bis_code": "IS 10146:2021 (PE Contact Layer) & IS 12252:2018 (BOPP/PET) & IS 15392:2003",
        "epr_category": "Category III Multi-Layer Flexible Plastic Under Plastic Waste Management Rules 2016",
        "technical_specs": {
            "otr_range": "< 0.5 cc/m2/day (ASTM D3985)",
            "wvtr_range": "< 0.3 g/m2/day (ASTM F1249)",
            "thickness_um": 95,
            "map_gas_mix": "98% N2 + 2% Residual O2"
        },
        "physics_metrics": {
            "target_wvtr_allowable": 0.45,
            "target_otr_allowable": 0.85
        },
        "safety_factor": 2.4
    }

    pdf_buffer = generate_packaging_readiness_pdf(massive_text_payload)
    pdf_bytes = pdf_buffer.getvalue()
    assert len(pdf_bytes) > 2000, "PDF must generate valid byte stream"

    # Open with PyMuPDF to count exact pages
    pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    num_pages = len(pdf_doc)
    print(f"    -> Generated PDF byte size: {len(pdf_bytes)} bytes.")
    print(f"    -> PyMuPDF Verified Page Count: {num_pages} Page(s).")
    assert num_pages == 1, f"CRITICAL: PDF exceeded 1-page budget! Rendered {num_pages} pages."
    print("    -> Passed! PDF strictly fits on 1 A4 page despite massive 650+ character strings!")

    print("\n" + "=" * 70)
    print("[SUCCESS] ALL 6 ADVERSARIAL STRESS TEST SCENARIOS PASSED WITH ZERO FAILURES!")
    print("=" * 70)

if __name__ == "__main__":
    run_stress_test_suite()
