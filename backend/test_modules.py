"""
Comprehensive Unit Test Suite for PackAI India (SIH26236)
Testing all 4 Enterprise Engineering Modules:
1. Industrial Converter Economics (GSM, Yield, Pouch Unit Cost, Spoilage ROI)
2. CPCB EPR Financial Liability & Carbon LCA (Carbon Footprint, Categories I-IV, Circularity Grade)
3. Reverse FSSAI Label Compliance Auditor (10 Statutory Rules, Score, Remedies)
4. Live Digital Product Passport (SHA-256 Seal, Batch Integrity, NABL/BIS standards)
5. FastAPI Integration & Recommendation Payload Validation
"""

import sys
import os
import unittest
from fastapi.testclient import TestClient

# Ensure root is on path so backend package can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
for p in [parent_dir, current_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

from backend.engine.economics_engine import (
    calculate_laminate_gsm,
    calculate_pouch_cost,
    calculate_spoilage_roi,
    evaluate_converter_economics
)
from backend.engine.sustainability_engine import (
    determine_cpcb_epr_category,
    determine_circularity_rating,
    calculate_carbon_and_epr_footprint
)
from backend.engine.audit_engine import (
    audit_packaging_label,
    SAMPLE_COMPLIANT_LABEL,
    SAMPLE_NON_COMPLIANT_LABEL
)
from backend.engine.passport_engine import (
    generate_passport_hash,
    get_digital_product_passport
)
from backend.main import app


class TestEconomicsEngine(unittest.TestCase):
    """Test Industrial Converter Economics & GSM calculations"""

    def test_gsm_and_yield_single_substrate(self):
        # 50 micron LDPE (0.92 g/cm3) -> 46.0 GSM (no adhesive)
        structure = {
            "id": "single_pe",
            "name": "50um LDPE Monolayer",
            "layers": [{"name": "LDPE", "thickness_um": 50.0}]
        }
        res = calculate_laminate_gsm(structure)
        self.assertAlmostEqual(res["total_gsm"], 46.0, places=1)
        self.assertAlmostEqual(res["film_yield_m2_per_kg"], 1000.0 / 46.0, places=1)

    def test_gsm_and_yield_multi_layer(self):
        # 12 micron PET (1.40) + 12 micron MET-PET (1.40) + 70 micron LDPE (0.92)
        # Layers: 16.8 + 16.8 + 64.4 = 98.0
        # Adhesive: 2 interfaces * 2.5 = 5.0
        # Total GSM: 103.0
        structure = {
            "id": "pet_metpet_pe",
            "name": "Triplex Barrier",
            "layers": [
                {"name": "BOPET", "thickness_um": 12.0},
                {"name": "Metallized BOPET", "thickness_um": 12.0},
                {"name": "LDPE", "thickness_um": 70.0}
            ]
        }
        res = calculate_laminate_gsm(structure, adhesive_gsm_per_nip=2.5)
        self.assertAlmostEqual(res["total_gsm"], 103.0, places=1)
        self.assertAlmostEqual(res["film_yield_m2_per_kg"], 1000.0 / 103.0, places=1)
        self.assertEqual(len(res["layers_gsm_breakdown"]), 3)

    def test_pouch_unit_cost(self):
        gsm_result = {
            "total_gsm": 100.0,
            "adhesive_gsm": 2.5,
            "layers_gsm_breakdown": [
                {"gsm": 30.0, "material_price_inr_kg": 145.0},
                {"gsm": 67.5, "material_price_inr_kg": 110.0}
            ]
        }
        costing = calculate_pouch_cost(
            gsm_result=gsm_result,
            pouch_area_m2=0.045,
            conversion_margin_per_kg=35.0,
            retail_pack_price_inr=200.0
        )
        self.assertGreater(costing["cost_per_pouch_inr"], 0.3)
        self.assertLess(costing["cost_per_pouch_inr"], 5.0)
        self.assertGreater(costing["cost_per_1000_pouches_inr"], 300.0)
        self.assertLess(costing["packaging_cost_ratio_pct"], 5.0)

    def test_spoilage_roi(self):
        roi = calculate_spoilage_roi(
            commodity_name="Foxnut / Makhana",
            retail_pack_price_inr=200.0,
            batch_pouches=4000,
            barrier_cost_per_pouch=1.25,
            unlaminated_spoilage_pct=15.0,
            barrier_spoilage_pct=1.5
        )
        self.assertGreater(roi["net_spoilage_savings_inr"], 0)
        self.assertGreater(roi["roi_percentage"], 100.0)
        self.assertIn("economic_verdict", roi)

    def test_evaluate_converter_economics(self):
        structure = {
            "id": "bopp_cpp",
            "name": "BOPP / CPP Recyclable",
            "layers": [
                {"name": "BOPP Film", "thickness_um": 20.0},
                {"name": "CPP Sealant", "thickness_um": 30.0}
            ]
        }
        res = evaluate_converter_economics(
            structure=structure,
            commodity_name="Roasted Peanuts",
            pack_weight_g=200.0,
            retail_pack_price_inr=100.0
        )
        self.assertIn("gsm_metrics", res)
        self.assertIn("unit_cost_metrics", res)
        self.assertIn("spoilage_roi", res)
        self.assertEqual(res["gsm_metrics"]["layer_count"], 2)


class TestSustainabilityEngine(unittest.TestCase):
    """Test CPCB EPR Financial Liability & Carbon LCA Engine"""

    def test_cpcb_category_classification(self):
        # Category III: Multi-Layered Plastic with foil
        foil_struct = {
            "id": "pet_alu_pe",
            "name": "12µm PET / 9µm Foil / 70µm PE",
            "epr_category": "Category III"
        }
        c3 = determine_cpcb_epr_category(foil_struct)
        self.assertEqual(c3["code"], "category_iii")
        self.assertEqual(c3["rate_per_ton"], 5800.0)

        # Category II: Single polymer mono-material PE/PE
        mono_struct = {
            "id": "bopp_bopp",
            "name": "BOPP / Metallized BOPP Mono",
            "epr_category": "Category II"
        }
        c2 = determine_cpcb_epr_category(mono_struct)
        self.assertEqual(c2["code"], "category_ii")
        self.assertEqual(c2["rate_per_ton"], 3200.0)

        # Category IV: Compostable PLA
        compost_struct = {
            "id": "compostable_pla",
            "name": "Bio-film PLA / PBS",
            "epr_category": "Category IV"
        }
        c4 = determine_cpcb_epr_category(compost_struct)
        self.assertEqual(c4["code"], "category_iv")
        self.assertEqual(c4["rate_per_ton"], 0.0)
        self.assertTrue(c4["is_exempt"])

    def test_circularity_grading(self):
        compost_struct = {"id": "compostable_pla", "name": "PLA Film"}
        circ_iv = determine_circularity_rating(compost_struct, "category_iv")
        self.assertEqual(circ_iv["grade"], "Grade A+")

        mono_struct = {"id": "pe_pe", "name": "PE / PE Mono"}
        circ_ii = determine_circularity_rating(mono_struct, "category_ii")
        self.assertEqual(circ_ii["grade"], "Grade A")

        foil_struct = {"id": "pet_foil_pe", "name": "PET / Foil / PE"}
        circ_iii = determine_circularity_rating(foil_struct, "category_iii")
        self.assertEqual(circ_iii["grade"], "Grade C")

    def test_carbon_and_epr_footprint(self):
        structure = {
            "id": "triplex_foil",
            "name": "PET / Foil / PE Triplex",
            "layers": [
                {"name": "PET", "thickness_um": 12.0},
                {"name": "Aluminium Foil", "thickness_um": 9.0},
                {"name": "LDPE", "thickness_um": 70.0}
            ]
        }
        res = calculate_carbon_and_epr_footprint(
            structure=structure,
            pouch_area_m2=0.045,
            annual_pouches_volume=100000
        )
        self.assertGreater(res["embodied_carbon"]["carbon_per_pouch_g_co2e"], 5.0)
        self.assertGreater(res["cpcb_epr_compliance"]["estimated_annual_epr_liability_inr"], 0)
        self.assertEqual(res["cpcb_epr_compliance"]["category_code"], "category_iii")


class TestAuditEngine(unittest.TestCase):
    """Test Reverse FSSAI Label Compliance Auditor"""

    def test_compliant_sample_audit(self):
        res = audit_packaging_label(SAMPLE_COMPLIANT_LABEL)
        self.assertGreaterEqual(res["score"], 90)
        self.assertEqual(res["verdict"], "COMPLIANT")
        self.assertEqual(len(res["violations"]), 0)

    def test_non_compliant_sample_audit(self):
        res = audit_packaging_label(SAMPLE_NON_COMPLIANT_LABEL)
        self.assertLess(res["score"], 50)
        self.assertEqual(res["verdict"], "NON-COMPLIANT")
        self.assertGreaterEqual(len(res["violations"]), 3)

    def test_individual_statutory_rules(self):
        # Label without FSSAI Lic
        text = "Delicious Crispy Chips Net Qty: 200g MRP Rs. 50 (incl. of all taxes) Best before 6 months 100% Vegetarian"
        res = audit_packaging_label(text)
        fssai_violation = next((v for v in res["violations"] if v["rule_id"] == "FSSAI_LIC"), None)
        self.assertIsNotNone(fssai_violation)
        self.assertIn("FSSAI", fssai_violation["remedy"])

        # Label with invalid/short FSSAI Lic
        bad_fssai = "fssai Lic. No: 12345678"
        res2 = audit_packaging_label(bad_fssai)
        fssai_violation2 = next((v for v in res2["violations"] if v["rule_id"] == "FSSAI_LIC"), None)
        self.assertIsNotNone(fssai_violation2)


class TestDigitalProductPassport(unittest.TestCase):
    """Test Live Digital Product Passport engine"""

    def test_passport_hash_reproducibility(self):
        h1 = generate_passport_hash("BATCH-100", "makhana", "pet_metpet_pe")
        h2 = generate_passport_hash("BATCH-100", "makhana", "pet_metpet_pe")
        h3 = generate_passport_hash("BATCH-101", "makhana", "pet_metpet_pe")
        self.assertEqual(h1, h2)
        self.assertNotEqual(h1, h3)
        self.assertEqual(len(h1), 64)

    def test_passport_generation(self):
        passport = get_digital_product_passport(
            batch_id="TEST-BATCH-2026",
            commodity_id="makhana"
        )
        self.assertEqual(passport["batch_id"], "TEST-BATCH-2026")
        self.assertEqual(passport["status"], "VERIFIED & VALID")
        self.assertIn("integrity_hash", passport)
        self.assertIn("issuing_authority", passport)
        self.assertIn("safety_and_conformity", passport)
        self.assertIn("nabl_accreditation", passport["safety_and_conformity"])
        self.assertIn("certified_packaging", passport)


class TestFastAPIIntegration(unittest.TestCase):
    """Test API routes and endpoints via TestClient"""

    def setUp(self):
        self.client = TestClient(app)

    def test_economics_endpoint(self):
        payload = {
            "structure": {
                "id": "bopp_cpp",
                "name": "BOPP / CPP Recyclable",
                "layers": [
                    {"name": "BOPP Film", "thickness_um": 20.0},
                    {"name": "CPP Sealant", "thickness_um": 30.0}
                ]
            },
            "commodity_name": "Foxnut / Makhana",
            "pack_weight_g": 200.0,
            "retail_pack_price_inr": 200.0
        }
        res = self.client.post("/api/economics", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("gsm_metrics", data)
        self.assertIn("unit_cost_metrics", data)
        self.assertIn("spoilage_roi", data)

    def test_sustainability_endpoint(self):
        payload = {
            "structure": {
                "id": "pet_metpet_pe",
                "name": "BOPET / MET-PET / PE",
                "layers": [
                    {"name": "PET", "thickness_um": 12.0},
                    {"name": "MET-PET", "thickness_um": 12.0},
                    {"name": "LDPE", "thickness_um": 70.0}
                ]
            },
            "pouch_area_m2": 0.045,
            "annual_pouches_volume": 100000
        }
        res = self.client.post("/api/sustainability", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("embodied_carbon", data)
        self.assertIn("cpcb_epr_compliance", data)
        self.assertIn("circularity_rating", data)

    def test_audit_label_endpoint(self):
        res = self.client.get("/api/audit-samples")
        self.assertEqual(res.status_code, 200)
        samples = res.json()
        self.assertIn("compliant_sample", samples)
        self.assertIn("non_compliant_sample", samples)

        audit_res = self.client.post("/api/audit-label", json={"raw_text": samples["compliant_sample"]})
        self.assertEqual(audit_res.status_code, 200)
        data = audit_res.json()
        self.assertEqual(data["verdict"], "COMPLIANT")
        self.assertGreaterEqual(data["score"], 90)

    def test_verify_passport_endpoint(self):
        res = self.client.get("/api/verify/PMFME-BATCH-999?id=makhana")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["batch_id"], "PMFME-BATCH-999")
        self.assertEqual(data["status"], "VERIFIED & VALID")
        self.assertIn("integrity_hash", data)

    def test_recommend_endpoint_includes_modules(self):
        payload = {
            "commodity_id": "makhana",
            "commodity_name": "Foxnut / Makhana",
            "category": "dry_expanded_snacks",
            "moisture_pct": 5.0,
            "fat_oil_pct": 0.5,
            "ph_value": 6.8,
            "target_shelf_life_days": 180,
            "storage_temp_c": 27.0,
            "rh_ambient_pct": 65.0,
            "pack_size_g": 200.0,
            "cost_sensitivity": "balanced",
            "sustainability_priority": "standard"
        }
        res = self.client.post("/api/recommend", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("economics", data)
        self.assertIn("sustainability", data)
        self.assertIn("alt_economics", data)
        self.assertIn("alt_sustainability", data)
        self.assertGreater(data["economics"]["unit_cost_metrics"]["cost_per_pouch_inr"], 0)
        self.assertIn("circularity_rating", data["sustainability"])

    def test_export_pdf_with_new_economics(self):
        payload = {
            "commodity_id": "makhana",
            "name_en": "Foxnut / Makhana",
            "name_hi": "मखाना",
            "category": "dry_expanded_snacks",
            "moisture_pct": 5.0,
            "fat_oil_pct": 0.5,
            "ph_value": 6.8,
            "shelf_life_days": 180,
            "storage_type": "ambient",
            "odop_region": "Madhubani, Bihar",
            "primary_material": "12µm PET / 12µm MET-PET / 70µm LDPE",
            "target_wvtr": 0.35,
            "target_otr": 1.2,
            "fssai_standards": "FSSAI Packaging Regulations 2018",
            "bis_specification": "IS 10171:2020",
            "cpcb_epr_category": "Category III (Multi-layered Plastic)",
            "mandatory_declaration": "Best Before 6 months from packaging. Store in a cool, dry place.",
            "overall_migration_limit": "< 60 mg/kg (IS 9845 with 3% acetic acid)",
            "economics": {
                "gsm_metrics": {"total_gsm": 103.0, "film_yield_m2_per_kg": 9.71},
                "unit_cost_metrics": {"cost_per_pouch_inr": 1.15, "packaging_cost_ratio_pct": 0.77},
                "spoilage_roi": {"roi_percentage": 730.0}
            },
            "sustainability": {
                "cpcb_epr_compliance": {"estimated_annual_epr_liability_inr": 1854.0},
                "circularity_rating": {"grade": "Grade B"}
            }
        }
        res = self.client.post("/api/export-pdf", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers["content-type"], "application/pdf")
        self.assertGreater(len(res.content), 5000)


if __name__ == "__main__":
    unittest.main()
