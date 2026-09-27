import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import math
from backend.engine.physics_engine import (
    calculate_saturation_vapor_pressure_kpa,
    calculate_target_wvtr,
    calculate_target_otr,
    solve_optimal_laminate,
    generate_shelf_life_decay_curves,
    get_is9845_simulant_matrix,
    LAMINATE_CATALOG
)

def test_physics_calculations():
    print("[*] 1. Testing Tetens Saturation Vapor Pressure Formula...")
    ps_0 = calculate_saturation_vapor_pressure_kpa(0.0)
    ps_25 = calculate_saturation_vapor_pressure_kpa(25.0)
    ps_38 = calculate_saturation_vapor_pressure_kpa(38.0)
    assert 0.60 <= ps_0 <= 0.63, f"Expected ps(0C) ~0.61 kPa, got {ps_0}"
    assert 3.10 <= ps_25 <= 3.25, f"Expected ps(25C) ~3.17 kPa, got {ps_25}"
    assert 6.50 <= ps_38 <= 6.80, f"Expected ps(38C) ~6.63 kPa, got {ps_38}"
    print(f"    -> Passed! ps(0C)={ps_0:.2f} kPa, ps(25C)={ps_25:.2f} kPa, ps(38C)={ps_38:.2f} kPa")

    print("[*] 2. Testing Moisture Sorption Kinetics (Target WVTR)...")
    # Case A: Crisp Makhana (7% moisture, 180 days shelf life)
    wvtr_res = calculate_target_wvtr(moisture_pct=7.0, shelf_life_days=180, storage_temp_c=30.0)
    assert 0.1 <= wvtr_res["target_wvtr"] <= 3.0, f"Makhana WVTR should be strict, got {wvtr_res['target_wvtr']}"
    print(f"    -> Makhana Target WVTR: {wvtr_res['target_wvtr']} g/m2/day (Delta M: {wvtr_res['delta_m_water_g']}g)")

    # Case B: High Moisture Button Mushroom (91% moisture, 7 days)
    wvtr_mush = calculate_target_wvtr(moisture_pct=91.0, shelf_life_days=7, storage_temp_c=4.0)
    assert wvtr_mush["target_wvtr"] >= 25.0, f"Fresh produce should have breathable WVTR, got {wvtr_mush['target_wvtr']}"
    print(f"    -> Mushroom Target WVTR: {wvtr_mush['target_wvtr']} g/m2/day (Breathable)")

    print("[*] 3. Testing Lipid Oxidation & Respiration (Target OTR)...")
    # Case A: High Fat Ghee (99.5% fat, 365 days)
    otr_ghee = calculate_target_otr(fat_oil_pct=99.5, shelf_life_days=365)
    assert otr_ghee["target_otr"] <= 1.0, f"Ghee should require near-zero OTR, got {otr_ghee['target_otr']}"
    print(f"    -> Ghee Target OTR: {otr_ghee['target_otr']} cc/m2/day (Foil/Tinplate grade)")

    # Case B: Respiration of Mushroom (Extremely High Respiration)
    otr_mush = calculate_target_otr(fat_oil_pct=0.3, shelf_life_days=7, respiration_class="Extremely High", storage_temp_c=4.0)
    assert otr_mush["target_otr"] >= 2500.0, f"Mushroom OTR must be breathable, got {otr_mush['target_otr']}"
    assert otr_mush["is_produce"] is True
    print(f"    -> Mushroom Respiration OTR: {otr_mush['target_otr']} cc/m2/day (Active Respiration: {otr_mush['respiration_rate_mg_kg_hr']} mg/kg-hr)")

    print("[*] 4. Testing Multi-Layer Laminate Structure Solver...")
    assert len(LAMINATE_CATALOG) == 12, f"Expected 12 catalog formulations, got {len(LAMINATE_CATALOG)}"
    
    # Solve for Makhana
    sol_makhana = solve_optimal_laminate(
        target_wvtr=wvtr_res["target_wvtr"],
        target_otr=150.0,
        commodity_id="makhana",
        moisture_pct=7.0,
        fat_oil_pct=0.1,
        ph_value=6.5,
        storage_type="ambient",
        respiration_class="Very Low"
    )
    assert sol_makhana["primary_structure"]["id"] in ["bopp_metbopp_ldpe", "pet_metbopp_pe", "pet_foil_ldpe"]
    assert sol_makhana["primary_safety_factor"] >= 1.0
    print(f"    -> Makhana Solved Primary Structure: {sol_makhana['primary_structure']['name']} (Safety Factor: {sol_makhana['primary_safety_factor']}x)")

    # Solve for Fresh Mushroom
    sol_mush = solve_optimal_laminate(
        target_wvtr=wvtr_mush["target_wvtr"],
        target_otr=otr_mush["target_otr"],
        commodity_id="mushroom",
        moisture_pct=91.0,
        fat_oil_pct=0.3,
        ph_value=6.5,
        storage_type="chilled",
        respiration_class="Extremely High"
    )
    assert "microperf" in sol_mush["primary_structure"]["id"]
    print(f"    -> Mushroom Solved Primary Structure: {sol_mush['primary_structure']['name']}")

    print("[*] 5. Testing Dynamic Shelf-Life Decay Curves...")
    decay = generate_shelf_life_decay_curves(
        commodity_id="makhana",
        moisture_pct=7.0,
        fat_oil_pct=0.1,
        shelf_life_days=180,
        primary_laminate=sol_makhana["primary_structure"],
        respiration_class="Very Low"
    )
    assert len(decay["days"]) == 25
    assert decay["days_to_failure"]["unpackaged"] < decay["days_to_failure"]["monolayer"] < decay["days_to_failure"]["recommended"]
    print(f"    -> Days to Failure: Unpackaged={decay['days_to_failure']['unpackaged']}d, Monolayer={decay['days_to_failure']['monolayer']}d, Recommended={decay['days_to_failure']['recommended']}d")

    print("[*] 6. Testing IS 9845 Simulant Mapping...")
    sim_pickle = get_is9845_simulant_matrix(ph_value=3.2, fat_oil_pct=22.0, category="Acidic & Oily Preserves")
    sim_codes = [s["simulant_code"] for s in sim_pickle["simulants"]]
    assert "Simulant A" in sim_codes
    assert "Simulant B" in sim_codes  # Acidic (pH 3.2)
    assert "Simulant D" in sim_codes  # Fatty (22% fat)
    print(f"    -> Mango Pickle Simulants Mapped: {sim_codes}")

    print("\n[OK] ALL BIOPHYSICAL & KINETICS UNIT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_physics_calculations()
