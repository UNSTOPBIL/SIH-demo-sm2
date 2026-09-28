import math
from typing import Dict, Any, List, Optional

# Standard Industrial Converter Polymer Densities (g/cm³)
# Note: 1 µm thickness over 1 m² area = 1.0 cm³ volume.
# Therefore, Layer GSM (g/m²) = thickness_um * density (g/cm³).
POLYMER_DENSITIES: Dict[str, float] = {
    "pet": 1.40,
    "boppet": 1.40,
    "bopp": 0.91,
    "opp": 0.91,
    "metbopp": 0.92,
    "ldpe": 0.92,
    "lldpe": 0.92,
    "pe": 0.92,
    "hdpe": 0.95,
    "foil": 2.70,
    "alu": 2.70,
    "aluminium": 2.70,
    "aluminum": 2.70,
    "evoh": 1.17,
    "bopa": 1.14,
    "pa": 1.14,
    "nylon": 1.14,
    "pla": 1.25,
    "pbs": 1.26,
    "paper": 0.80,
    "kraft": 0.80,
    "tinplate": 7.85,
    "default": 1.05
}

# Current Indian Industrial Converter Benchmark Polymer Prices (₹ / kg)
POLYMER_PRICES_INR_PER_KG: Dict[str, float] = {
    "bopp": 145.0,
    "pet": 125.0,
    "lldpe": 110.0,
    "ldpe": 110.0,
    "hdpe": 115.0,
    "foil": 380.0,
    "evoh": 420.0,
    "nylon": 290.0,
    "bopa": 290.0,
    "pla": 260.0,
    "pbs": 275.0,
    "paper": 85.0,
    "kraft": 85.0,
    "tinplate": 95.0,
    "adhesive": 220.0,
    "default": 135.0
}

# Conversion cost margin (₹ / kg) covering gravure printing, lamination, slitting & pouching
DEFAULT_CONVERSION_MARGIN_INR_PER_KG = 35.0

# Solventless adhesive GSM per lamination nip (g/m²)
DEFAULT_ADHESIVE_GSM_PER_NIP = 2.5


def detect_layer_polymer_key(layer_name: str, short_name: str = "") -> str:
    """Detects polymer resin keyword from layer text for density and cost matching."""
    text = f"{layer_name} {short_name}".lower()
    if "foil" in text or "alu" in text:
        return "foil"
    if "evoh" in text:
        return "evoh"
    if "tinplate" in text or "canister" in text:
        return "tinplate"
    if "pla" in text or "polylactic" in text:
        return "pla"
    if "pbs" in text:
        return "pbs"
    if "nylon" in text or "bopa" in text or "polyamide" in text:
        return "nylon"
    if "met-bopp" in text or "metallized bopp" in text or "metbopp" in text:
        return "metbopp"
    if "bopp" in text or "opp" in text:
        return "bopp"
    if "bopet" in text or "pet" in text or "polyester" in text:
        return "pet"
    if "hdpe" in text:
        return "hdpe"
    if "lldpe" in text:
        return "lldpe"
    if "ldpe" in text or " pe" in text or "polyethylene" in text or "punched tray" in text:
        return "ldpe"
    if "kraft" in text or "paper" in text:
        return "paper"
    return "default"


def calculate_laminate_gsm(
    structure: Dict[str, Any],
    adhesive_gsm_per_nip: float = DEFAULT_ADHESIVE_GSM_PER_NIP
) -> Dict[str, Any]:
    """
    Calculates exact composite Grams per Square Meter (GSM) and film yield (m²/kg).
    GSM = sum(thickness_um * density) + adhesive_gsm.
    Yield (m²/kg) = 1000 / GSM_total.
    """
    layers = structure.get("layers", [])
    if not layers:
        # Fallback to total thickness if layers array not present
        tot_um = float(structure.get("total_thickness_um", 65.0))
        tot_gsm = round(tot_um * 1.05, 2)
        return {
            "total_gsm": tot_gsm,
            "film_yield_m2_per_kg": round(1000.0 / max(0.1, tot_gsm), 2),
            "layers_gsm_breakdown": [],
            "adhesive_gsm": 0.0,
            "layer_count": 0
        }

    layer_breakdown = []
    pure_layers_gsm = 0.0

    for idx, layer in enumerate(layers):
        um = float(layer.get("thickness_um", 20.0))
        poly_key = detect_layer_polymer_key(layer.get("name", ""), layer.get("short_name", ""))
        density = POLYMER_DENSITIES.get(poly_key, POLYMER_DENSITIES["default"])
        layer_gsm = round(um * density, 2)
        pure_layers_gsm += layer_gsm

        unit_price = POLYMER_PRICES_INR_PER_KG.get(poly_key, POLYMER_PRICES_INR_PER_KG["default"])

        layer_breakdown.append({
            "layer_index": idx + 1,
            "name": layer.get("short_name") or layer.get("name", f"Layer {idx+1}"),
            "polymer_key": poly_key,
            "thickness_um": um,
            "density_g_cm3": density,
            "gsm": layer_gsm,
            "material_price_inr_kg": unit_price
        })

    # Adhesive GSM = (Number of layers - 1) * adhesive_gsm_per_nip
    num_nips = max(0, len(layers) - 1)
    total_adhesive_gsm = round(num_nips * adhesive_gsm_per_nip, 2)
    total_composite_gsm = round(pure_layers_gsm + total_adhesive_gsm, 2)

    # Calculate weight percentages for weighted polymer cost calculation
    for item in layer_breakdown:
        item["weight_pct"] = round((item["gsm"] / max(0.1, total_composite_gsm)) * 100.0, 1)

    film_yield = round(1000.0 / max(0.1, total_composite_gsm), 2)

    return {
        "total_gsm": total_composite_gsm,
        "pure_polymer_gsm": round(pure_layers_gsm, 2),
        "adhesive_gsm": total_adhesive_gsm,
        "film_yield_m2_per_kg": film_yield,
        "layers_gsm_breakdown": layer_breakdown,
        "layer_count": len(layers)
    }


def calculate_pouch_cost(
    gsm_result: Dict[str, Any],
    pouch_area_m2: float = 0.045,
    conversion_margin_per_kg: float = DEFAULT_CONVERSION_MARGIN_INR_PER_KG,
    retail_pack_price_inr: float = 200.0
) -> Dict[str, Any]:
    """
    Computes industrial packaging cost per pouch, per 1,000 pouches,
    and packaging expense percentage relative to consumer retail value.
    """
    total_gsm = gsm_result["total_gsm"]
    breakdown = gsm_result["layers_gsm_breakdown"]
    adhesive_gsm = gsm_result["adhesive_gsm"]

    # Weighted base material cost per kg
    material_cost_acc = 0.0
    for item in breakdown:
        material_cost_acc += item["gsm"] * item["material_price_inr_kg"]

    if adhesive_gsm > 0:
        material_cost_acc += adhesive_gsm * POLYMER_PRICES_INR_PER_KG["adhesive"]

    base_material_cost_per_kg = round(material_cost_acc / max(0.1, total_gsm), 2)
    total_laminate_cost_per_kg = round(base_material_cost_per_kg + conversion_margin_per_kg, 2)

    # Pouch weight (g) = Pouch Area (m²) * Total GSM (g/m²)
    pouch_weight_grams = round(pouch_area_m2 * total_gsm, 2)
    pouch_weight_kg = pouch_weight_grams / 1000.0

    # Unit cost per individual pouch
    cost_per_pouch_inr = round(pouch_weight_kg * total_laminate_cost_per_kg, 2)
    cost_per_1000_pouches_inr = round(cost_per_pouch_inr * 1000.0, 2)

    # Packaging cost % relative to consumer retail pack price
    packaging_cost_ratio_pct = round((cost_per_pouch_inr / max(1.0, retail_pack_price_inr)) * 100.0, 2)

    return {
        "pouch_area_m2": pouch_area_m2,
        "pouch_weight_grams": pouch_weight_grams,
        "base_material_cost_per_kg": base_material_cost_per_kg,
        "conversion_margin_per_kg": conversion_margin_per_kg,
        "total_laminate_cost_per_kg": total_laminate_cost_per_kg,
        "cost_per_pouch_inr": cost_per_pouch_inr,
        "cost_per_1000_pouches_inr": cost_per_1000_pouches_inr,
        "retail_pack_price_inr": retail_pack_price_inr,
        "packaging_cost_ratio_pct": packaging_cost_ratio_pct
    }


def calculate_spoilage_roi(
    commodity_name: str,
    retail_pack_price_inr: float = 200.0,
    batch_pouches: int = 4000,
    unlaminated_cost_per_pouch: float = 0.50,
    barrier_cost_per_pouch: float = 1.35,
    unlaminated_spoilage_pct: float = 18.0,
    barrier_spoilage_pct: float = 1.2
) -> Dict[str, Any]:
    """
    Quantifies the economic return on investment (ROI) of upgrading to the
    recommended high-barrier packaging structure versus an unlaminated monolayer bag.
    """
    batch_gross_retail_value = batch_pouches * retail_pack_price_inr

    # Inventory loss under unlaminated storage
    unlaminated_lost_pouches = int(batch_pouches * (unlaminated_spoilage_pct / 100.0))
    unlaminated_financial_loss = round(unlaminated_lost_pouches * retail_pack_price_inr, 2)

    # Inventory loss under recommended barrier laminate
    barrier_lost_pouches = int(batch_pouches * (barrier_spoilage_pct / 100.0))
    barrier_financial_loss = round(barrier_lost_pouches * retail_pack_price_inr, 2)

    # Net inventory value saved
    net_spoilage_savings = round(unlaminated_financial_loss - barrier_financial_loss, 2)

    # Additional packaging material investment
    unlaminated_total_packaging_cost = batch_pouches * unlaminated_cost_per_pouch
    barrier_total_packaging_cost = batch_pouches * barrier_cost_per_pouch
    incremental_packaging_investment = round(barrier_total_packaging_cost - unlaminated_total_packaging_cost, 2)

    # Net financial gain & ROI percentage
    net_gain = round(net_spoilage_savings - incremental_packaging_investment, 2)
    roi_pct = round((net_gain / max(1.0, incremental_packaging_investment)) * 100.0, 1)

    # Payback pouches (number of pouches needed to cover the packaging upgrade)
    pouches_to_breakeven = math.ceil(incremental_packaging_investment / max(1.0, retail_pack_price_inr))

    return {
        "commodity_name": commodity_name,
        "batch_pouches": batch_pouches,
        "batch_gross_retail_value": batch_gross_retail_value,
        "unlaminated_spoilage_pct": unlaminated_spoilage_pct,
        "barrier_spoilage_pct": barrier_spoilage_pct,
        "unlaminated_financial_loss_inr": unlaminated_financial_loss,
        "barrier_financial_loss_inr": barrier_financial_loss,
        "net_spoilage_savings_inr": net_spoilage_savings,
        "incremental_packaging_investment_inr": incremental_packaging_investment,
        "net_financial_gain_inr": net_gain,
        "roi_percentage": roi_pct,
        "pouches_to_breakeven": pouches_to_breakeven,
        "economic_verdict": f"Upgrading packaging saves ₹{net_spoilage_savings:,.0f} in spoiled inventory per {batch_pouches:,} pouches with a {roi_pct}% net financial ROI."
    }


def evaluate_converter_economics(
    structure: Dict[str, Any],
    commodity_name: str = "Agri-Commodity",
    pack_weight_g: float = 250.0,
    retail_pack_price_inr: float = 200.0,
    batch_pouches: int = 4000
) -> Dict[str, Any]:
    """
    Unified entry point computing total GSM, yield, pouch unit cost,
    and spoilage ROI index for a given packaging laminate.
    """
    # 250g pack typically uses ~0.045 m² pouch area; scale reasonably with pack_weight_g
    area_m2 = round(0.045 * math.pow(max(50.0, pack_weight_g) / 250.0, 0.65), 3)

    gsm_data = calculate_laminate_gsm(structure)
    cost_data = calculate_pouch_cost(
        gsm_result=gsm_data,
        pouch_area_m2=area_m2,
        retail_pack_price_inr=retail_pack_price_inr
    )
    roi_data = calculate_spoilage_roi(
        commodity_name=commodity_name,
        retail_pack_price_inr=retail_pack_price_inr,
        batch_pouches=batch_pouches,
        barrier_cost_per_pouch=cost_data["cost_per_pouch_inr"]
    )

    return {
        "laminate_id": structure.get("id", "custom_laminate"),
        "laminate_name": structure.get("name", "Multi-Layer Composite"),
        "gsm_metrics": gsm_data,
        "unit_cost_metrics": cost_data,
        "spoilage_roi": roi_data
    }
