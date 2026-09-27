import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_api():
    print("[*] Testing GET /api/health...")
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"
    print("    -> Passed!")

    print("[*] Testing GET /api/commodities...")
    r = client.get("/api/commodities")
    assert r.status_code == 200
    data = r.json()
    assert data["count"] == 18
    assert len(data["commodities"]) == 18
    print(f"    -> Passed! Found {data['count']} seed commodities.")

    print("[*] Testing GET /api/translations...")
    r = client.get("/api/translations")
    assert r.status_code == 200
    trans = r.json()
    assert "en" in trans and "hi" in trans
    print("    -> Passed! Found bilingual en/hi dictionaries.")

    print("[*] Testing POST /api/recommend (Makhana with T=30C, RH=70%)...")
    payload = {
        "commodity_id": "makhana",
        "moisture_pct": 7.0,
        "fat_oil_pct": 0.1,
        "ph_value": 6.5,
        "shelf_life_days": 180,
        "storage_type": "ambient",
        "storage_temp_c": 30.0,
        "ambient_rh": 70.0
    }
    r = client.post("/api/recommend", json=payload)
    if r.status_code != 200:
        print("ERROR RESPONSE:", r.status_code, r.text)
    assert r.status_code == 200
    rec = r.json()
    assert "primary_material" in rec
    assert "barrier_profile" in rec
    assert "technical_specs" in rec
    assert "physics_metrics" in rec
    assert "target_wvtr_req" in rec["physics_metrics"]
    assert "target_otr_req" in rec["physics_metrics"]
    assert "ps_sat_pa" in rec["physics_metrics"]
    assert "shelf_life_decay" in rec
    assert "curve_recommended" in rec["shelf_life_decay"]
    assert len(rec["shelf_life_decay"]["curve_recommended"]) >= 20
    assert "days_to_failure" in rec["shelf_life_decay"]
    assert "simulant_protocol" in rec
    assert len(rec["simulant_protocol"]["simulants"]) == 4
    assert "primary_structure" in rec
    assert len(rec["primary_structure"]["layers"]) >= 2
    print(f"    -> Passed! Recommended: {rec['primary_material']}")
    print(f"    -> Target WVTR: {rec['physics_metrics']['target_wvtr_req']} g/m2/day, Allowable OTR: {rec['physics_metrics']['target_otr_req']} cc/m2/day")

    print("[*] Testing GET /api/compliance/makhana...")
    r = client.get("/api/compliance/makhana")
    assert r.status_code == 200
    comp = r.json()
    assert "fssai" in comp
    assert "bis" in comp
    assert "migration" in comp
    assert "epr" in comp
    assert "labelling_checklist" in comp
    assert "simulant_protocol" in comp
    print(f"    -> Passed! BIS Code: {comp['bis']['is_code']}")

    print("[*] Testing POST /api/export-pdf...")
    r = client.post("/api/export-pdf", json=rec)
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"
    assert len(r.content) > 1000
    print(f"    -> Passed! Generated PDF size: {len(r.content)} bytes.")

    print("\n[OK] ALL 6 BACKEND API TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_api()
