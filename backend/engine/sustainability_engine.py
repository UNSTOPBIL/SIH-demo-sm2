import math
from typing import Dict, Any, List, Optional
from backend.engine.economics_engine import (
    calculate_laminate_gsm,
    detect_layer_polymer_key
)

# Cradle-to-Gate Embodied Carbon Footprint Intensities (kg CO2e / kg resin)
# Sources: Ecoinvent 3.8 / PlasticsEurope Eco-profiles / Defra Carbon Factors
CARBON_INTENSITY_FACTORS: Dict[str, float] = {
    "foil": 11.5,      # Virgin primary aluminium foil
    "alu": 11.5,
    "aluminum": 11.5,
    "nylon": 6.8,       # Polyamide 6 (BOPA)
    "bopa": 6.8,
    "evoh": 3.8,        # Ethylene vinyl alcohol barrier resin
    "pet": 2.4,         # Virgin BOPET film
    "tinplate": 2.1,    # Steel with tin electroplate & lacquer
    "lldpe": 1.9,       # Low-density polyethylene sealant
    "ldpe": 1.9,
    "pe": 1.9,
    "hdpe": 1.8,        # High-density polyethylene
    "bopp": 1.8,        # Biaxially-oriented polypropylene
    "metbopp": 1.9,     # Metallized BOPP (sub-micron aluminium vapor)
    "paper": 1.1,       # Bleached/unbleached kraft paper
    "kraft": 1.1,
    "pbs": 1.1,         # Polybutylene succinate
    "pla": 0.8,         # Corn-derived polylactic acid (IS 17088)
    "adhesive": 2.8,    # Solventless polyurethane adhesive
    "default": 2.1
}

# CPCB EPR Fee Benchmarks under Plastic Waste Management Rules 2016 / 2022 (₹ / Metric Ton)
CPCB_EPR_FEES_INR_PER_TON: Dict[str, float] = {
    "category_i": 2400.0,    # Rigid Plastics
    "category_ii": 3200.0,   # Flexible Monolayer / Single-polymer
    "category_iii": 5800.0,  # Multi-Layered Plastic (MLP)
    "category_iv": 0.0,      # Compostable (IS 17088 Certified Exempt)
    "default": 5800.0
}


def determine_cpcb_epr_category(structure: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classifies a flexible or rigid structure into official CPCB EPR categories:
    - Category I: Rigid packaging (e.g. tinplate canister, rigid tub)
    - Category II: Flexible plastic packaging of single polymer (e.g. PE/PE, BOPP/PP)
    - Category III: Multi-layered plastic packaging (at least one non-plastic layer like Al-foil, paper, or dissimilar polymers)
    - Category IV: Compostable plastics confirming to IS/ISO 17088
    """
    laminate_id = structure.get("id", "").lower()
    name = structure.get("name", "").lower()
    structure_code = structure.get("structure_code", "").lower()
    epr_declared = structure.get("epr_category", "").lower()

    # Check Category IV first (Compostable)
    if "pla" in laminate_id or "compostable" in laminate_id or "compostable" in name or "category iv" in epr_declared or "category 4" in epr_declared:
        return {
            "code": "category_iv",
            "name": "Category IV (Compostable Plastics per IS 17088)",
            "rate_per_ton": CPCB_EPR_FEES_INR_PER_TON["category_iv"],
            "is_exempt": True,
            "statutory_note": "100% EPR Fee Exemption under MoEFCC PWM Rules Schedule II, provided valid CPCB/SPCB certificate exists."
        }

    # Check for multi-layer / dissimilar materials (Al-Foil, PET+PE, BOPA+PE, MetBOPP+PE, Category III)
    has_foil = "foil" in laminate_id or "al" in structure_code or "foil" in name
    has_evoh = "evoh" in laminate_id or "evoh" in name
    has_bopa = "bopa" in laminate_id or "nylon" in name
    has_paper = "paper" in laminate_id or "kraft" in name
    is_multi_polymer = ("pet" in laminate_id and "pe" in laminate_id) or ("bopp" in laminate_id and "pe" in laminate_id)

    if "category iii" in epr_declared or "category 3" in epr_declared or has_foil or has_evoh or has_bopa or has_paper or is_multi_polymer:
        return {
            "code": "category_iii",
            "name": "Category III (Multi-Layered Plastic / MLP)",
            "rate_per_ton": CPCB_EPR_FEES_INR_PER_TON["category_iii"],
            "is_exempt": False,
            "statutory_note": "Highest EPR fee tier due to mechanical separation difficulty. Requires end-of-life coprocessing or waste-to-energy credit offset."
        }

    # Check for Category I (Rigid Plastics / Tinplate / Canister)
    if "tinplate" in laminate_id or "canister" in laminate_id or "tub" in laminate_id or "category i " in epr_declared or epr_declared == "category i":
        return {
            "code": "category_i",
            "name": "Category I (Rigid Packaging)",
            "rate_per_ton": CPCB_EPR_FEES_INR_PER_TON["category_i"],
            "is_exempt": False,
            "statutory_note": "Recycling target: 60-80% of registered plastic footprint."
        }

    # Single polymer mono-material flexible (e.g., pure PE or pure PP)
    return {
        "code": "category_ii",
        "name": "Category II (Single-Polymer Flexible Plastic)",
        "rate_per_ton": CPCB_EPR_FEES_INR_PER_TON["category_ii"],
        "is_exempt": False,
        "statutory_note": "100% mechanically recyclable into secondary PCR granules. Lower compliance fee tier."
    }


def determine_circularity_rating(structure: Dict[str, Any], epr_category_code: str) -> Dict[str, Any]:
    """
    Assigns an A+ to F circularity & recyclability grade with actionable guidance.
    """
    if epr_category_code == "category_iv":
        return {
            "grade": "Grade A+",
            "label": "Certified Compostable & Circular",
            "badge_color": "#16a34a",
            "recycling_stream": "Industrial & Home Composting (IS/ISO 17088)",
            "circularity_index": 9.5,
            "guidance_en": "Zero plastic waste footprint; biodegrades into water, CO2, and biomass within 180 days in commercial facilities.",
            "guidance_hi": "शून्य प्लास्टिक अपशिष्ट; 180 दिनों के भीतर पूरी तरह से खाद में परिवर्तित हो जाता है।"
        }

    if epr_category_code == "category_ii":
        return {
            "grade": "Grade A",
            "label": "Mono-Material High Recyclability",
            "badge_color": "#0d9488",
            "recycling_stream": "Rigid/Flexible PE/PP Mechanical Re-granulation (Code 2/4/5)",
            "circularity_index": 8.5,
            "guidance_en": "Can be directly baled and processed into high-quality PCR granules without delamination.",
            "guidance_hi": "बिना अलग किए सीधे पुनर्चक्रण योग्य; उच्च गुणवत्ता वाले द्वितीयक प्लास्टिक में बदला जा सकता है।"
        }

    # For Category III, differentiate metallized films from Al-foil triplex
    laminate_id = structure.get("id", "").lower()
    if "foil" in laminate_id or "al" in structure.get("structure_code", "").lower():
        return {
            "grade": "Grade C",
            "label": "Multi-Material Foil Barrier (Difficult to Separate)",
            "badge_color": "#f59e0b",
            "recycling_stream": "Cement Kiln Co-Processing / Pyrolysis Chemical Recycling",
            "circularity_index": 4.5,
            "guidance_en": "Aluminium foil bonded to plastics cannot be mechanically separated. Brand owner must purchase Category III EPR credits or coprocess.",
            "guidance_hi": "एल्युमिनियम फॉयल को प्लास्टिक से अलग करना कठिन है; सीमेंट भट्टी सह-प्रसंस्करण अनिवार्य है।"
        }

    return {
        "grade": "Grade B",
        "label": "Metallized / Multi-Polymer Barrier",
        "badge_color": "#2563eb",
        "recycling_stream": "Advanced Mechanical Recycling with Compatibilizers",
        "circularity_index": 6.5,
        "guidance_en": "Sub-micron metallization layer enables compatibilized extrusion for secondary industrial products.",
        "guidance_hi": "सूक्ष्म मेटलाइज्ड परत; द्वितीयक औद्योगिक उत्पादों के लिए पुनर्चक्रण संभव है।"
    }


def calculate_carbon_and_epr_footprint(
    structure: Dict[str, Any],
    pouch_area_m2: float = 0.045,
    annual_pouches_volume: int = 500000
) -> Dict[str, Any]:
    """
    Computes embodied cradle-to-gate carbon footprint and statutory CPCB EPR financial liability.
    """
    gsm_data = calculate_laminate_gsm(structure)
    total_gsm = gsm_data["total_gsm"]
    layers_breakdown = gsm_data["layers_gsm_breakdown"]
    adhesive_gsm = gsm_data["adhesive_gsm"]

    # 1. Carbon footprint calculation
    carbon_factor_acc = 0.0
    for layer in layers_breakdown:
        p_key = layer["polymer_key"]
        factor = CARBON_INTENSITY_FACTORS.get(p_key, CARBON_INTENSITY_FACTORS["default"])
        layer["carbon_intensity_kg_co2_kg"] = factor
        carbon_factor_acc += layer["gsm"] * factor

    if adhesive_gsm > 0:
        carbon_factor_acc += adhesive_gsm * CARBON_INTENSITY_FACTORS["adhesive"]

    weighted_carbon_intensity_per_kg = round(carbon_factor_acc / max(0.1, total_gsm), 3)

    # Pouch weight in kg = pouch_area_m2 * total_gsm / 1000.0
    pouch_weight_grams = round(pouch_area_m2 * total_gsm, 2)
    pouch_weight_kg = pouch_weight_grams / 1000.0

    # Carbon per pouch (g CO2e) = pouch_weight_kg * weighted_carbon_intensity_per_kg * 1000
    carbon_per_pouch_g_co2e = round(pouch_weight_kg * weighted_carbon_intensity_per_kg * 1000.0, 2)
    carbon_per_10k_pouches_kg_co2e = round((carbon_per_pouch_g_co2e * 10000.0) / 1000.0, 2)

    # 2. CPCB EPR Financial Liability Calculation
    epr_category = determine_cpcb_epr_category(structure)
    circularity = determine_circularity_rating(structure, epr_category["code"])

    # Annual packaging tonnage (Metric Tons)
    annual_tonnage = round((annual_pouches_volume * pouch_weight_kg) / 1000.0, 3)

    # Annual EPR obligation (₹) = annual_tonnage * rate_per_ton
    annual_epr_liability_inr = round(annual_tonnage * epr_category["rate_per_ton"], 2)
    epr_fee_per_10k_pouches_inr = round((annual_epr_liability_inr / max(1, annual_pouches_volume)) * 10000.0, 2)

    return {
        "laminate_id": structure.get("id", "custom_laminate"),
        "laminate_name": structure.get("name", "Multi-Layer Composite"),
        "total_gsm": total_gsm,
        "pouch_area_m2": pouch_area_m2,
        "pouch_weight_grams": pouch_weight_grams,
        "embodied_carbon": {
            "weighted_carbon_intensity_kg_co2e_per_kg": weighted_carbon_intensity_per_kg,
            "carbon_per_pouch_g_co2e": carbon_per_pouch_g_co2e,
            "carbon_per_10k_pouches_kg_co2e": carbon_per_10k_pouches_kg_co2e,
            "benchmark_context": f"Generates {carbon_per_pouch_g_co2e}g CO2e per pack (~{(carbon_per_pouch_g_co2e / 14.0) * 100:.0f}% of typical food item embodied carbon)."
        },
        "cpcb_epr_compliance": {
            "category_code": epr_category["code"],
            "category_name": epr_category["name"],
            "fee_rate_per_ton_inr": epr_category["rate_per_ton"],
            "is_exempt": epr_category["is_exempt"],
            "statutory_note": epr_category["statutory_note"],
            "assumed_annual_pouches": annual_pouches_volume,
            "annual_plastic_tonnage_mt": annual_tonnage,
            "estimated_annual_epr_liability_inr": annual_epr_liability_inr,
            "epr_fee_per_10k_pouches_inr": epr_fee_per_10k_pouches_inr
        },
        "circularity_rating": circularity
    }
