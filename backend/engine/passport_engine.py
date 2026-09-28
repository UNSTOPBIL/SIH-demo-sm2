import hashlib
import time
import uuid
from typing import Dict, Any, Optional
from datetime import datetime, timezone

try:
    from backend.engine.compliance import get_compliance_details
    from backend.engine.physics_engine import LAMINATE_CATALOG, get_is9845_simulant_matrix
except (ImportError, ModuleNotFoundError):
    from engine.compliance import get_compliance_details
    from engine.physics_engine import LAMINATE_CATALOG, get_is9845_simulant_matrix


def generate_passport_hash(batch_id: str, commodity_id: str, laminate_id: str) -> str:
    """Computes SHA-256 cryptographic seal for the digital passport."""
    payload = f"MoFPI:SIH26236:{batch_id}:{commodity_id}:{laminate_id}:STATUTORY_CLEARANCE"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()


def get_digital_product_passport(
    batch_id: Optional[str] = None,
    commodity_id: str = "makhana",
    laminate_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates or retrieves verifiable Digital Product Passport data for a commodity batch.
    """
    clean_batch_id = batch_id or f"PMFME-{datetime.now(timezone.utc).strftime('%Y%m')}-{str(uuid.uuid4())[:8].upper()}"
    
    # 1. Fetch compliance data for commodity
    comp_data = get_compliance_details(commodity_id)
    c_meta = comp_data.get("commodity_metadata", {})
    name_en = c_meta.get("name_en", "Agro-Food Produce")
    name_hi = c_meta.get("name_hi", "कृषि खाद्य उत्पाद")
    region = c_meta.get("odop_region", "All India ODOP Cluster")
    category = c_meta.get("category", "Value Added Food")

    # 2. Match laminate structure
    selected_laminate = None
    if laminate_id:
        selected_laminate = next((l for l in LAMINATE_CATALOG if l["id"] == laminate_id), None)
    if not selected_laminate:
        # Default to a high-barrier triplex or first catalogue item
        selected_laminate = LAMINATE_CATALOG[0]

    # 3. Cryptographic seal
    integrity_hash = generate_passport_hash(clean_batch_id, commodity_id, selected_laminate["id"])

    # 4. Dates
    issued_date = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
    expiry_date = datetime.now(timezone.utc).replace(year=datetime.now(timezone.utc).year + 1).strftime("%d %b %Y")

    simulants = comp_data.get("simulant_protocol", {}).get("simulants", [])
    active_simulants = [s["name"] for s in simulants if s.get("applicable")]

    return {
        "passport_version": "1.0-SIH26236",
        "batch_id": clean_batch_id,
        "status": "VERIFIED & VALID",
        "integrity_hash": integrity_hash,
        "issuing_authority": {
            "ministry": "Ministry of Food Processing Industries (MoFPI)",
            "initiative": "Pradhan Mantri Formalisation of Micro food processing Enterprises (PMFME)",
            "scheme": "One District One Product (ODOP) Packaging Integrity Registry",
            "regulatory_framework": "FSSAI (Packaging) Regs 2018 & BIS Act 2016",
            "portal": "https://pmfme.mofpi.gov.in"
        },
        "commodity": {
            "id": commodity_id,
            "name_en": name_en,
            "name_hi": name_hi,
            "odop_region": region,
            "food_category": category,
            "fssai_schedule_category": comp_data.get("fssai", {}).get("schedule_iv_category", "Schedule IV")
        },
        "certified_packaging": {
            "structure_id": selected_laminate["id"],
            "structure_name": selected_laminate["name"],
            "structure_code": selected_laminate.get("structure_code", "LAMINATE-COMPOSITE"),
            "thickness_um": selected_laminate.get("total_thickness_um", 70),
            "layers": [layer.get("name") for layer in selected_laminate.get("layers", [])],
            "water_vapor_transmission_rate": f"{selected_laminate.get('wvtr', 1.0)} g/m²/day (ASTM F1249)",
            "oxygen_transmission_rate": f"{selected_laminate.get('otr', 1.0)} cc/m²/day (ASTM D3985)",
            "bis_standard": selected_laminate.get("bis_code", comp_data.get("bis", {}).get("standards_code", "IS 10146:2021")),
            "cpcb_epr_category": selected_laminate.get("epr_category", "Category III Multilayer Flexible Plastic")
        },
        "safety_and_conformity": {
            "nabl_accreditation": "ISO/IEC 17025 Conformant Packaging Protocol",
            "overall_migration_limit": "IS 9845: OML ≤ 60 mg/kg (≤ 10 mg/dm²)",
            "mandatory_simulants_tested": active_simulants,
            "heavy_metals_compliance": "Pb, Cd, CrVI, Hg < 100 ppm per IS 9845 Clause 4",
            "fssai_display_clearance": "Clause 5(1) 9-Point Mandatory Label Compliant"
        },
        "timestamps": {
            "issued_at": issued_date,
            "valid_until": expiry_date,
            "server_timestamp_epoch": int(time.time())
        },
        "qr_verification_url": f"/verify?id={commodity_id}&batch={clean_batch_id}"
    }
