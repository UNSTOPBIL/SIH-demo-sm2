import json
import os
from typing import Dict, Any, List, Optional
try:
    from backend.engine.physics_engine import get_is9845_simulant_matrix
except (ImportError, ModuleNotFoundError):
    from engine.physics_engine import get_is9845_simulant_matrix

def load_seed_commodities() -> List[Dict[str, Any]]:
    seed_path = os.path.join(os.path.dirname(__file__), "..", "data", "commodities_seed.json")
    with open(seed_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_compliance_details(
    commodity_id: str,
    ph_value: Optional[float] = None,
    fat_oil_pct: Optional[float] = None,
    moisture_pct: Optional[float] = None,
    commodity_name: Optional[str] = None
) -> Dict[str, Any]:
    commodities = load_seed_commodities()
    matched = next((c for c in commodities if c["id"] == commodity_id), None)

    if matched:
        c_id = matched["id"]
        c_name_en = matched["name_en"]
        c_name_hi = matched["name_hi"]
        c_region = matched["odop_region"]
        c_primary_mat = matched["primary_material"]
        c_ph = float(ph_value if ph_value is not None else matched.get("ph_value", 6.5))
        c_fat = float(fat_oil_pct if fat_oil_pct is not None else matched.get("fat_oil_pct", 1.0))
        c_moist = float(moisture_pct if moisture_pct is not None else matched.get("moisture_pct", 10.0))
        c_sched = matched["fssai_schedule"].split("&")[0].strip()
        c_bis = matched["bis_code"]
        c_epr = matched["epr_category"]
        c_mig_lim = matched.get("migration_limit", "10 mg/dm2 or 60 mg/kg max (IS 9845:1998)")
        c_category = matched.get("category", "")
    else:
        # Dynamic statutory heuristics for custom/unseeded commodities
        c_id = commodity_id
        clean_title = (commodity_name or commodity_id).replace("_", " ").replace("-", " ").title()
        c_name_en = f"Custom: {clean_title}"
        c_name_hi = clean_title
        c_region = "Self-Declared Custom Processing Enterprise"
        c_ph = float(ph_value if ph_value is not None else 6.5)
        c_fat = float(fat_oil_pct if fat_oil_pct is not None else 2.0)
        c_moist = float(moisture_pct if moisture_pct is not None else 10.0)
        c_primary_mat = "Multi-Layer Barrier Composite (Food Contact Grade)"

        # Statutory FSSAI Schedule IV Mapping
        if c_ph < 4.5:
            c_sched = "Schedule IV (Acidic Foods, Pickles & Preserves)"
            c_category = "Acidic Preserves"
        elif c_fat > 15.0:
            c_sched = "Schedule IV (Oils, Fats, Emulsions & Confectionery)"
            c_category = "Oils, Fats & Emulsions"
        elif c_moist >= 80.0:
            c_sched = "Schedule IV (Fresh Fruits, Horticultural & Perishable Produce)"
            c_category = "Fresh Produce"
        else:
            c_sched = "Schedule IV (General Processed Foods, Cereals & Powders)"
            c_category = "General Processed Food"

        c_bis = "IS 10146:2021 (PE Contact Layer) & IS 12252:2018 (BOPP/PET)"
        c_epr = "Category III Multilayer Flexible Plastic (Five Layers or Below)"
        c_mig_lim = "10 mg/dm2 or 60 mg/kg max (IS 9845:1998)"

    is_plastic = any(p in c_primary_mat.lower() for p in ["ldpe", "hdpe", "pet", "bopp", "poly", "pa", "evoh", "cpp", "film", "composite", "barrier"])
    is_metal = any(m in c_primary_mat.lower() for m in ["foil", "tin", "aluminium", "metal"])

    fssai_reg = {
        "regulation_name": "Food Safety and Standards (Packaging) Regulations, 2018",
        "schedule_iv_category": c_sched,
        "material_schedule": "Schedule III (Plastics in contact with food)" if is_plastic else ("Schedule II (Metals and alloys)" if is_metal else "Schedule I (Paper and paperboard)"),
        "compliance_status": "Mandatory Clearance Required"
    }

    bis_standard = {
        "is_code": c_bis,
        "title": "Indian Standard Specification for Materials in Food Contact Applications",
        "jurisdiction": "Bureau of Indian Standards (BIS)",
        "certification_mark": "ISI Mark / Certificate of Conformity"
    }

    simulant_protocol = get_is9845_simulant_matrix(
        ph_value=c_ph,
        fat_oil_pct=c_fat,
        category=c_category
    )

    migration_data = {
        "overall_migration_limit": c_mig_lim,
        "testing_method": "IS 9845 (Methods of analysis for overall migration of constituents of plastic materials into food simulants)",
        "simulants_prescribed": "Distilled Water (aqueous), 3% Acetic Acid (acidic), 15% Ethanol (sweet/alcoholic), n-Heptane / Olive oil (fatty foods)",
        "limit_value": "60 mg/kg or 10 mg/dm²",
        "simulant_matrix": simulant_protocol
    }

    epr_compliance = {
        "mandatory": True if is_plastic else False,
        "framework": "Plastic Waste Management Rules, 2016 (as amended 2022/2024)",
        "category": c_epr,
        "registration_portal": "CPCB Central EPR Portal (eprplastic.cpcb.gov.in)",
        "target_obligation": "Annual recycling & reuse target reporting required for Brand Owners / PIBOs"
    }

    labelling_checklist = [
        {"id": "fssai_logo", "key": "label_fssai_logo", "mandatory": True, "checked": True},
        {"id": "veg_mark", "key": "label_veg_mark", "mandatory": True, "checked": True},
        {"id": "net_quantity", "key": "label_net_quantity", "mandatory": True, "checked": True},
        {"id": "mrp", "key": "label_mrp", "mandatory": True, "checked": True},
        {"id": "batch_no", "key": "label_batch_no", "mandatory": True, "checked": True},
        {"id": "dates", "key": "label_dates", "mandatory": True, "checked": True},
        {"id": "ingredients", "key": "label_ingredients", "mandatory": True, "checked": True},
        {"id": "nutrition", "key": "label_nutrition", "mandatory": True, "checked": True},
        {"id": "consumer_care", "key": "label_consumer_care", "mandatory": True, "checked": True}
    ]

    nabl_protocol = {
        "standard": "ISO/IEC 17025 Accredited Laboratory Testing",
        "scope": "Batch-wise verification of overall and specific migration limits, heavy metal screening (Pb, Cd, Hg, Cr VI < 100 ppm)",
        "frequency": "Mandatory prior to commercial dispatch or batch packaging change"
    }

    return {
        "commodity_id": c_id,
        "commodity_name_en": c_name_en,
        "commodity_name_hi": c_name_hi,
        "odop_region": c_region,
        "primary_material": c_primary_mat,
        "moisture_pct": c_moist,
        "fat_oil_pct": c_fat,
        "ph_value": c_ph,
        "fssai": fssai_reg,
        "bis": bis_standard,
        "migration": migration_data,
        "simulant_protocol": simulant_protocol,
        "epr": epr_compliance,
        "labelling_checklist": labelling_checklist,
        "nabl": nabl_protocol
    }
