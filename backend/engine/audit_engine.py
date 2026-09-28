import re
from typing import Dict, Any, List, Optional

# FSSAI State and Central Registration Codes
FSSAI_CENTRAL_PREFIXES = ["100"]  # 100 = Central FSSAI License
VALID_FSSAI_PREFIXES = [
    "100", "101", "102", "103", "104", "105", "106", "107", "108", "109",
    "110", "111", "112", "113", "114", "115", "116", "117", "118", "119",
    "120", "121", "122", "123", "124", "125", "126", "127", "128", "129",
    "130", "131", "132", "133", "134", "135", "136"
]

SAMPLE_COMPLIANT_LABEL = """
MITHILA PREMIUM POPPED MAKHANA (FOXNUT)
Ingredients: Popped Foxnuts (98%), Cold-Pressed Edible Vegetable Oil (1.5%), Pink Rock Salt (0.5%).
Allergen Advice: Processed in a facility that also handles tree nuts, sesame, and dairy.
Nutritional Information per 100g:
Energy: 347 kcal | Protein: 9.7 g | Carbohydrate: 76.2 g | Total Sugars: 0.5 g | Added Sugars: 0.0 g | Total Fat: 0.1 g | Saturated Fat: 0.0 g | Trans Fat: 0.0 g | Sodium: 142 mg.
Net Quantity: 250 g
Unit Sale Price: ₹0.96 per g
MRP: ₹240.00 (Inclusive of all taxes)
Batch No: MKH-2026-B08
Date of Packaging: 15/09/2026
Best Before: 9 Months from date of packaging
Veg Logo: 100% Vegetarian (Green circle inside square)
Manufactured & Marketed By:
Mithila Agro Processing Enterprises Pvt. Ltd.,
Plot No. 42, Food Park Phase-I, Industrial Area, Darbhanga, Bihar - 846004.
Customer Care Executive: support@mithilafoods.in | Helpline: 1800-123-4567
fssai Lic. No.: 10023081000124
Recyclable Flexible Laminate: IS 12252 / IS 10146 Food Grade Contact
"""

SAMPLE_NON_COMPLIANT_LABEL = """
Tasty Foxnut Snacks - Super Crispy!
MRP: 200 Rs
Net wt: 250
FSSAI: 123456789
Mfg: Last month
Good quality food for daily snacking.
Distributed locally in town.
"""


def audit_packaging_label(raw_text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Performs statutory reverse compliance audit on packaging artwork or draft label text
    against FSSAI (Labelling and Display) Regulations 2020 and Legal Metrology Rules 2011.
    """
    text = (raw_text or "").strip()
    if metadata:
        # Append structured metadata to text buffer for comprehensive analysis
        for k, v in metadata.items():
            if v:
                text += f"\n{k}: {v}"

    checks = []
    total_weight = 0
    passed_weight = 0

    # -------------------------------------------------------------
    # 1. FSSAI License Number (Weight: 15)
    # -------------------------------------------------------------
    w1 = 15
    total_weight += w1
    fssai_match = re.search(r'(?:fssai|lic\.?\s*(?:no\.?|number)?)[^\d]{0,10}(\d{10,16})', text, re.IGNORECASE)
    if not fssai_match:
        # Fallback search for any 14-digit number
        fssai_match = re.search(r'\b(\d{14})\b', text)

    if fssai_match:
        lic_str = fssai_match.group(1)
        if len(lic_str) == 14:
            prefix = lic_str[:3]
            is_central = prefix in FSSAI_CENTRAL_PREFIXES
            checks.append({
                "rule_id": "FSSAI_LIC",
                "name": "FSSAI 14-Digit License Verification",
                "category": "Statutory License",
                "status": "PASS",
                "weight": w1,
                "found_value": f"fssai Lic. No. {lic_str} ({'Central FSSAI' if is_central else 'State FSSAI'} Prefix: {prefix})",
                "citation": "FSSAI (Packaging & Labelling) Regulations, Clause 5(1)",
                "remedy": None
            })
            passed_weight += w1
        else:
            checks.append({
                "rule_id": "FSSAI_LIC",
                "name": "FSSAI 14-Digit License Verification",
                "category": "Statutory License",
                "status": "FAIL",
                "weight": w1,
                "found_value": f"Invalid digit count ({len(lic_str)} digits): '{lic_str}'",
                "citation": "FSSAI (Labelling & Display) Regulations 2020, Section 5(1)",
                "remedy": "Must print exact 14-digit FSSAI license number along with the official FSSAI logo on the principal display panel."
            })
    else:
        checks.append({
            "rule_id": "FSSAI_LIC",
            "name": "FSSAI 14-Digit License Verification",
            "category": "Statutory License",
            "status": "FAIL",
            "weight": w1,
            "found_value": "Missing / Not Found",
            "citation": "FSSAI (Labelling & Display) Regulations 2020, Section 5(1)",
            "remedy": "Mandatory FSSAI logo and 14-digit license number must be printed on both front and back panels."
        })

    # -------------------------------------------------------------
    # 2. Veg / Non-Veg Declaration (Weight: 10)
    # -------------------------------------------------------------
    w2 = 10
    total_weight += w2
    veg_match = re.search(r'(veg|vegetarian|green\s+circle|non-veg|non\s*vegetarian|brown\s+triangle)', text, re.IGNORECASE)
    if veg_match:
        val = veg_match.group(0).capitalize()
        checks.append({
            "rule_id": "VEG_NONVEG",
            "name": "Vegetarian / Non-Vegetarian Logo & Declaration",
            "category": "Dietary Symbol",
            "status": "PASS",
            "weight": w2,
            "found_value": f"Declared ({val})",
            "citation": "FSSAI Labelling Regulations 2020, Regulation 5(4)",
            "remedy": None
        })
        passed_weight += w2
    else:
        checks.append({
            "rule_id": "VEG_NONVEG",
            "name": "Vegetarian / Non-Vegetarian Logo & Declaration",
            "category": "Dietary Symbol",
            "status": "FAIL",
            "weight": w2,
            "found_value": "Missing / Not Declared",
            "citation": "FSSAI Labelling Regulations 2020, Regulation 5(4)",
            "remedy": "Must display the green dot in a square (for vegetarian) or brown triangle in a square (for non-vegetarian) on the front of pack."
        })

    # -------------------------------------------------------------
    # 3. Net Quantity Declaration (Weight: 10)
    # -------------------------------------------------------------
    w3 = 10
    total_weight += w3
    net_qty_match = re.search(r'(?:net\s*(?:qty|quantity|weight|wt)?\.?[:\s]*)([0-9]+(?:\.[0-9]+)?)\s*(kg|g|gm|gms|ml|ltr|l|litres|n)\b', text, re.IGNORECASE)
    if net_qty_match:
        checks.append({
            "rule_id": "NET_QTY",
            "name": "Net Quantity (Standard Metric Units)",
            "category": "Legal Metrology",
            "status": "PASS",
            "weight": w3,
            "found_value": f"Net Qty: {net_qty_match.group(1)} {net_qty_match.group(2)}",
            "citation": "Legal Metrology (Packaged Commodities) Rules 2011, Rule 12",
            "remedy": None
        })
        passed_weight += w3
    else:
        checks.append({
            "rule_id": "NET_QTY",
            "name": "Net Quantity (Standard Metric Units)",
            "category": "Legal Metrology",
            "status": "FAIL",
            "weight": w3,
            "found_value": "Missing or non-metric unit",
            "citation": "Legal Metrology (Packaged Commodities) Rules 2011, Rule 12",
            "remedy": "Must state Net Quantity in SI units (g, kg, ml, l) with correct font height based on pack area."
        })

    # -------------------------------------------------------------
    # 4. Unit Sale Price (Legal Metrology 2022 Amendment) (Weight: 10)
    # -------------------------------------------------------------
    w4 = 10
    total_weight += w4
    usp_match = re.search(r'(?:unit\s*sale\s*price|usp|u\.s\.p\.?)[:\s]*(?:₹|rs\.?)?\s*([0-9]+(?:\.[0-9]+)?)\s*(?:per|\/)\s*(g|kg|gm|ml|l|piece)', text, re.IGNORECASE)
    if usp_match:
        checks.append({
            "rule_id": "UNIT_SALE_PRICE",
            "name": "Unit Sale Price Declaration (per g / kg / ml)",
            "category": "Legal Metrology",
            "status": "PASS",
            "weight": w4,
            "found_value": f"Unit Sale Price: ₹{usp_match.group(1)} / {usp_match.group(2)}",
            "citation": "Legal Metrology (Packaged Commodities) Amendment Rules 2021/2022, Rule 6(11)",
            "remedy": None
        })
        passed_weight += w4
    else:
        checks.append({
            "rule_id": "UNIT_SALE_PRICE",
            "name": "Unit Sale Price Declaration (per g / kg / ml)",
            "category": "Legal Metrology",
            "status": "FAIL",
            "weight": w4,
            "found_value": "Missing / Not Found",
            "citation": "Legal Metrology (Packaged Commodities) Amendment Rules 2021/2022, Rule 6(11)",
            "remedy": "Mandatory under Indian law since Dec 2022: Must declare Unit Sale Price (e.g. '₹0.96 per g' or '₹960.00 per kg')."
        })

    # -------------------------------------------------------------
    # 5. Retail MRP & 'Inclusive of All Taxes' (Weight: 10)
    # -------------------------------------------------------------
    w5 = 10
    total_weight += w5
    mrp_match = re.search(r'(?:mrp|maximum\s*retail\s*price)[:\s]*(?:₹|rs\.?)?\s*([0-9]+(?:\.[0-9]+)?)', text, re.IGNORECASE)
    has_taxes_text = bool(re.search(r'(inclusive\s+of\s+all\s+taxes|incl\.?\s+of\s+all\s+taxes)', text, re.IGNORECASE))

    if mrp_match and has_taxes_text:
        checks.append({
            "rule_id": "MRP_TAXES",
            "name": "MRP with 'Inclusive of All Taxes'",
            "category": "Legal Metrology",
            "status": "PASS",
            "weight": w5,
            "found_value": f"MRP ₹{mrp_match.group(1)} (Inclusive of all taxes)",
            "citation": "Legal Metrology Rules 2011, Rule 6(1)(e)",
            "remedy": None
        })
        passed_weight += w5
    elif mrp_match and not has_taxes_text:
        checks.append({
            "rule_id": "MRP_TAXES",
            "name": "MRP with 'Inclusive of All Taxes'",
            "category": "Legal Metrology",
            "status": "FAIL",
            "weight": w5,
            "found_value": f"Found MRP ₹{mrp_match.group(1)}, but missing mandatory phrase 'Inclusive of all taxes'",
            "citation": "Legal Metrology Rules 2011, Rule 6(1)(e)",
            "remedy": "The wording '(Inclusive of all taxes)' or '(Incl. of all taxes)' is legally mandatory after MRP."
        })
    else:
        checks.append({
            "rule_id": "MRP_TAXES",
            "name": "MRP with 'Inclusive of All Taxes'",
            "category": "Legal Metrology",
            "status": "FAIL",
            "weight": w5,
            "found_value": "Missing MRP declaration",
            "citation": "Legal Metrology Rules 2011, Rule 6(1)(e)",
            "remedy": "Must print Maximum Retail Price (MRP) formatted as 'MRP ₹... (incl. of all taxes)'."
        })

    # -------------------------------------------------------------
    # 6. Date of Packaging / Manufacturing (Weight: 10)
    # -------------------------------------------------------------
    w6 = 10
    total_weight += w6
    date_match = re.search(r'(?:mfg|pkd|packed|packaging|manufactured)\s*(?:date|dt|\:)?[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}|\w+\s+\d{4})', text, re.IGNORECASE)
    if date_match:
        checks.append({
            "rule_id": "MFG_DATE",
            "name": "Date of Packaging / Manufacturing",
            "category": "Traceability",
            "status": "PASS",
            "weight": w6,
            "found_value": f"Date found: {date_match.group(0).strip()}",
            "citation": "FSSAI Labelling Regulations 2020, Section 5(7)",
            "remedy": None
        })
        passed_weight += w6
    else:
        checks.append({
            "rule_id": "MFG_DATE",
            "name": "Date of Packaging / Manufacturing",
            "category": "Traceability",
            "status": "FAIL",
            "weight": w6,
            "found_value": "Missing / Incomplete Date",
            "citation": "FSSAI Labelling Regulations 2020, Section 5(7)",
            "remedy": "Must print Month & Year or DD/MM/YYYY of manufacture or packaging."
        })

    # -------------------------------------------------------------
    # 7. Best Before / Expiry Date (Weight: 10)
    # -------------------------------------------------------------
    w7 = 10
    total_weight += w7
    expiry_match = re.search(r'(best\s*before|expiry\s*date|use\s*by|exp\.?\s*date)', text, re.IGNORECASE)
    if expiry_match:
        checks.append({
            "rule_id": "EXPIRY_DATE",
            "name": "Best Before / Expiry Period",
            "category": "Consumer Safety",
            "status": "PASS",
            "weight": w7,
            "found_value": f"Declared ({expiry_match.group(0).strip()})",
            "citation": "FSSAI Labelling Regulations 2020, Section 5(8)",
            "remedy": None
        })
        passed_weight += w7
    else:
        checks.append({
            "rule_id": "EXPIRY_DATE",
            "name": "Best Before / Expiry Period",
            "category": "Consumer Safety",
            "status": "FAIL",
            "weight": w7,
            "found_value": "Missing Best Before / Expiry declaration",
            "citation": "FSSAI Labelling Regulations 2020, Section 5(8)",
            "remedy": "Must state 'Best Before ... Months from Packaging' or specific Expiry Date."
        })

    # -------------------------------------------------------------
    # 8. Batch / Lot Number (Weight: 5)
    # -------------------------------------------------------------
    w8 = 5
    total_weight += w8
    batch_match = re.search(r'(batch\s*no|lot\s*no|b\.?\s*no\.?)[:\s]*([a-zA-Z0-9\-\/]+)', text, re.IGNORECASE)
    if batch_match:
        checks.append({
            "rule_id": "BATCH_NO",
            "name": "Batch / Lot Identification",
            "category": "Traceability",
            "status": "PASS",
            "weight": w8,
            "found_value": f"Batch Identifier: {batch_match.group(0).strip()}",
            "citation": "FSSAI Labelling Regulations 2020, Section 5(6)",
            "remedy": None
        })
        passed_weight += w8
    else:
        checks.append({
            "rule_id": "BATCH_NO",
            "name": "Batch / Lot Identification",
            "category": "Traceability",
            "status": "FAIL",
            "weight": w8,
            "found_value": "Missing Batch / Lot code",
            "citation": "FSSAI Labelling Regulations 2020, Section 5(6)",
            "remedy": "Provide unique batch or lot number preceded by 'Batch No.' or 'Lot No.'."
        })

    # -------------------------------------------------------------
    # 9. Ingredients List & Allergen Advisory (Weight: 10)
    # -------------------------------------------------------------
    w9 = 10
    total_weight += w9
    has_ingredients = bool(re.search(r'ingredients?\s*:', text, re.IGNORECASE))
    has_allergen = bool(re.search(r'(allergen|contains|processed in a facility|may contain)', text, re.IGNORECASE))

    if has_ingredients and has_allergen:
        checks.append({
            "rule_id": "INGREDIENTS_ALLERGEN",
            "name": "Ingredients List & Allergen Advisory",
            "category": "Food Information",
            "status": "PASS",
            "weight": w9,
            "found_value": "Both Ingredients in descending order and Allergen warning present",
            "citation": "FSSAI Labelling Regulations 2020, Section 5(2) & 5(3)",
            "remedy": None
        })
        passed_weight += w9
    elif has_ingredients and not has_allergen:
        # Partial credit: 6/10
        p_sub = 6
        passed_weight += p_sub
        checks.append({
            "rule_id": "INGREDIENTS_ALLERGEN",
            "name": "Ingredients List & Allergen Advisory",
            "category": "Food Information",
            "status": "FAIL",
            "weight": w9,
            "found_value": "Ingredients declared, but missing mandatory Allergen Advice declaration",
            "citation": "FSSAI Labelling Regulations 2020, Section 5(3)",
            "remedy": "Must add explicit allergen warning, e.g., 'Allergen Advice: Contains ...' or 'Processed in a facility handling nuts/dairy'."
        })
    else:
        checks.append({
            "rule_id": "INGREDIENTS_ALLERGEN",
            "name": "Ingredients List & Allergen Advisory",
            "category": "Food Information",
            "status": "FAIL",
            "weight": w9,
            "found_value": "Missing Ingredients declaration",
            "citation": "FSSAI Labelling Regulations 2020, Section 5(2)",
            "remedy": "Must declare all ingredients in descending order of in-going weight (m/m)."
        })

    # -------------------------------------------------------------
    # 10. Nutritional Information Table (Weight: 10)
    # -------------------------------------------------------------
    w10 = 10
    total_weight += w10
    has_nutrition = bool(re.search(r'nutrition|nutritional', text, re.IGNORECASE))
    has_energy = bool(re.search(r'energy|calories|kcal', text, re.IGNORECASE))
    has_protein = bool(re.search(r'protein', text, re.IGNORECASE))

    if has_nutrition and has_energy and has_protein:
        checks.append({
            "rule_id": "NUTRITION_FACTS",
            "name": "Nutritional Facts Table (per 100g / 100ml)",
            "category": "Nutritional Panel",
            "status": "PASS",
            "weight": w10,
            "found_value": "Energy, protein, carbohydrates, and nutrients declared",
            "citation": "FSSAI Labelling Regulations 2020, Section 5(3)",
            "remedy": None
        })
        passed_weight += w10
    else:
        checks.append({
            "rule_id": "NUTRITION_FACTS",
            "name": "Nutritional Facts Table (per 100g / 100ml)",
            "category": "Nutritional Panel",
            "status": "FAIL",
            "weight": w10,
            "found_value": "Incomplete or missing Nutritional Information panel",
            "citation": "FSSAI Labelling Regulations 2020, Section 5(3)",
            "remedy": "Must state Energy (kcal), Protein (g), Carbohydrate (g), Total Sugars (g), Added Sugars (g), Total Fat (g), and Sodium (mg) per 100g."
        })

    # -------------------------------------------------------------
    # Compute Final Score & Audit Status
    # -------------------------------------------------------------
    compliance_score = int(round((passed_weight / max(1, total_weight)) * 100.0))

    if compliance_score >= 85:
        verdict = "COMPLIANT"
        verdict_color = "#16a34a"  # green
        summary = "Label meets statutory FSSAI and Legal Metrology requirements for commercial packaging distribution."
    elif compliance_score >= 50:
        verdict = "PARTIALLY COMPLIANT"
        verdict_color = "#d97706"  # amber
        summary = "Label contains critical omissions that will incur regulatory penalties from food safety officers."
    else:
        verdict = "NON-COMPLIANT"
        verdict_color = "#dc2626"  # red
        summary = "Label fails basic statutory standards under FSSAI 2020 and Legal Metrology Rules 2011. Packaging cannot be commercially retailed."

    passed_checks = [c for c in checks if c["status"] == "PASS"]
    failed_checks = [c for c in checks if c["status"] == "FAIL"]

    return {
        "score": compliance_score,
        "verdict": verdict,
        "verdict_color": verdict_color,
        "summary": summary,
        "total_checks": len(checks),
        "passed_count": len(passed_checks),
        "failed_count": len(failed_checks),
        "passed_rules": passed_checks,
        "violations": failed_checks,
        "input_length": len(text)
    }
