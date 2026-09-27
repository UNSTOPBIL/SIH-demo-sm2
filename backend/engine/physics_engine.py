import math
from typing import Dict, Any, List, Tuple

# 12 Industrial Real-World Multi-Layer Substrate Formulations
LAMINATE_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "pet_foil_ldpe",
        "name": "12µm PET / 9µm Al-Foil / 50µm Food-Grade LDPE",
        "structure_code": "PET12 / AL9 / PE50",
        "description": "Ultra-hermetic triplex foil laminate with true zero-transmission barrier against oxygen, vapor, and photolytic oxidation.",
        "layers": [
            {
                "layer_type": "outer",
                "name": "12µm Biaxially-Oriented Polyethylene Terephthalate (BOPET)",
                "short_name": "12µm BOPET",
                "thickness_um": 12,
                "color": "#3b82f6",  # blue
                "role_en": "Reverse-print surface, high tensile strength, dimensional and thermal stability (ASTM D882)",
                "role_hi": "प्रिंटिंग सतह, उच्च तन्य शक्ति एवं तापीय स्थिरता",
                "standards": "IS 12252:2018 / ASTM D882"
            },
            {
                "layer_type": "barrier",
                "name": "9µm Ultra-Pure Aluminium Foil (Alloy 8011 / 1235)",
                "short_name": "9µm Al-Foil",
                "thickness_um": 9,
                "color": "#94a3b8",  # silver/grey
                "role_en": "Absolute zero transmission barrier to O2, water vapor, and UV light (pinhole-tested per ASTM F1249)",
                "role_hi": "ऑक्सीजन, जलवाष्प और प्रकाश के विरुद्ध शून्य-पारगम्यता बैरियर",
                "standards": "IS 8970:1991 / ASTM D3985 (OTR ≈ 0.05 cc)"
            },
            {
                "layer_type": "sealant",
                "name": "50µm Food-Grade Linear Low-Density Polyethylene (LLDPE)",
                "short_name": "50µm LLDPE",
                "thickness_um": 50,
                "color": "#10b981",  # green
                "role_en": "Hermetic heat seal, high hot-tack strength, virgin food-contact compliance per IS 10146:2021",
                "role_hi": "एयर-टाइट हीट सीलिंग, मजबूत वेल्ड और खाद्य संपर्क शुद्धता",
                "standards": "IS 10146:2021 (Food Contact PE) / IS 9845"
            }
        ],
        "otr": 0.05,        # cc/m2/day at 23C
        "wvtr": 0.05,       # g/m2/day at 38C/90% RH
        "total_thickness_um": 71,
        "cost_index": 4.2,  # out of 5
        "sustainability_index": 2.0,  # difficult to recycle multilayer
        "fssai_schedule": "Schedule IV & Schedule II (Aluminium) / Schedule III (Plastics)",
        "bis_code": "IS 8970:1991 (Al-Foil) & IS 10146:2021 (PE)",
        "epr_category": "Category III Multilayer Flexible Plastic",
        "typical_uses": ["moringa", "garam_masala", "ghee", "nutraceuticals", "infant_food"]
    },
    {
        "id": "bopp_metbopp_ldpe",
        "name": "20µm BOPP / 15µm Metallized BOPP / 40µm LDPE",
        "structure_code": "BOPP20 / MetBOPP15 / PE40",
        "description": "High-barrier metallized triplex film engineered for lipid oxidation protection and moisture exclusion in crisp snacks.",
        "layers": [
            {
                "layer_type": "outer",
                "name": "20µm Biaxially-Oriented Polypropylene (BOPP)",
                "short_name": "20µm BOPP",
                "thickness_um": 20,
                "color": "#60a5fa",
                "role_en": "Optical gloss, surface clarity, flex-crack resistance (ASTM D1922)",
                "role_hi": "उच्च चमक, स्पष्टता और लचीलापन",
                "standards": "IS 12252:2018"
            },
            {
                "layer_type": "barrier",
                "name": "15µm Vacuum Metallized BOPP (Optical Density 2.4)",
                "short_name": "15µm Met-BOPP",
                "thickness_um": 15,
                "color": "#cbd5e1",
                "role_en": "Vapor deposition aluminium barrier blocking 98% light and water vapor (ASTM F1249)",
                "role_hi": "98% प्रकाश और नमी रोकने वाला धातुयुक्त अवरोधक",
                "standards": "IS 12252:2018 (WVTR 0.5 - 1.2 g/m2/day)"
            },
            {
                "layer_type": "sealant",
                "name": "40µm Heat-Sealable Polyethylene (LDPE)",
                "short_name": "40µm LDPE",
                "thickness_um": 40,
                "color": "#34d399",
                "role_en": "Low seal initiation temperature (SIT 105°C), puncture resistance",
                "role_hi": "कम तापमान पर मजबूत हीट सीलिंग और पंचर सुरक्षा",
                "standards": "IS 10146:2021 (PE Contact Layer)"
            }
        ],
        "otr": 45.0,
        "wvtr": 0.8,
        "total_thickness_um": 75,
        "cost_index": 2.8,
        "sustainability_index": 2.5,
        "fssai_schedule": "Schedule IV & Schedule III (Plastics)",
        "bis_code": "IS 10146:2021 (PE Contact Layer) & IS 12252:2018 (BOPP)",
        "epr_category": "Category III Multilayer Flexible Plastic",
        "typical_uses": ["makhana", "chikki", "bajra_cookies", "chips", "crisps"]
    },
    {
        "id": "pet_metbopp_pe",
        "name": "12µm PET / 15µm Metallized BOPP / 40µm LDPE",
        "structure_code": "PET12 / MetBOPP15 / PE40",
        "description": "High-stiffness spice and powder barrier pouch preventing aroma volatility and UV light bleaching.",
        "layers": [
            {
                "layer_type": "outer",
                "name": "12µm High-Clarity BOPET Film",
                "short_name": "12µm BOPET",
                "thickness_um": 12,
                "color": "#3b82f6",
                "role_en": "High tensile strength, gas tightness, print protection",
                "role_hi": "उच्च मजबूती एवं प्रिंट सुरक्षा",
                "standards": "IS 12252:2018"
            },
            {
                "layer_type": "barrier",
                "name": "15µm Metallized BOPP Barrier Layer",
                "short_name": "15µm Met-BOPP",
                "thickness_um": 15,
                "color": "#cbd5e1",
                "role_en": "UV and visible light blocker preserving curcumin and essential aroma oils",
                "role_hi": "करक्यूमिन और सुगंधित तेलों को सुरक्षित रखने वाला यूवी ब्लॉकर",
                "standards": "ASTM D3985 / ASTM F1249"
            },
            {
                "layer_type": "sealant",
                "name": "40µm Coextruded Food-Grade PE Sealant",
                "short_name": "40µm PE",
                "thickness_um": 40,
                "color": "#10b981",
                "role_en": "Hermetic seal integrity preventing oil leaching into package seals",
                "role_hi": "तेल रिसाव को रोकने वाली मजबूत सील",
                "standards": "IS 10146:2021"
            }
        ],
        "otr": 1.5,
        "wvtr": 1.0,
        "total_thickness_um": 67,
        "cost_index": 3.0,
        "sustainability_index": 2.5,
        "fssai_schedule": "Schedule IV & Schedule III (Plastics)",
        "bis_code": "IS 12252:2018 (PET) & IS 10146:2021 (PE Contact Layer)",
        "epr_category": "Category III Multilayer Flexible Plastic",
        "typical_uses": ["turmeric", "apricot", "spices", "dry_herbs"]
    },
    {
        "id": "bopa_evoh_pe",
        "name": "15µm BOPA (Nylon) / 5µm EVOH / 50µm PE Thermoform Film",
        "structure_code": "PA15 / EVOH5 / PE50",
        "description": "High puncture-resistant thermoforming vacuum pouch with EVOH gas barrier for dairy, cheese, and moist preserves.",
        "layers": [
            {
                "layer_type": "outer",
                "name": "15µm Biaxially-Oriented Polyamide (BOPA / Nylon-6)",
                "short_name": "15µm Nylon",
                "thickness_um": 15,
                "color": "#8b5cf6",  # purple
                "role_en": "Extreme flex-crack and puncture resistance, deep draw thermoformability",
                "role_hi": "अत्यधिक पंचर और खिंचाव प्रतिरोध",
                "standards": "ASTM F1306 (Puncture Resistance)"
            },
            {
                "layer_type": "barrier",
                "name": "5µm Ethylene Vinyl Alcohol (EVOH 32 mol% Ethylene)",
                "short_name": "5µm EVOH Core",
                "thickness_um": 5,
                "color": "#ec4899",  # pink
                "role_en": "Ultra-high oxygen barrier (OTR < 0.5 cc) stopping aerobic spore growth",
                "role_hi": "ऑक्सीजन को रोककर बैक्टीरिया और मोल्ड रोकने वाला कोर",
                "standards": "ASTM D3985 (OTR < 0.5 cc/m2/day)"
            },
            {
                "layer_type": "sealant",
                "name": "50µm Coextruded Polyethylene (PE) with Metallocene",
                "short_name": "50µm mPE",
                "thickness_um": 50,
                "color": "#10b981",
                "role_en": "High seal integrity through food contamination / grease",
                "role_hi": "नमी और वसा के बावजूद मजबूत सील",
                "standards": "IS 10146:2021"
            }
        ],
        "otr": 0.4,
        "wvtr": 2.2,
        "total_thickness_um": 70,
        "cost_index": 4.0,
        "sustainability_index": 3.0,
        "fssai_schedule": "Schedule IV & Schedule III (Plastics)",
        "bis_code": "IS 10146:2021 (PE) & IS 9845 (Migration Testing)",
        "epr_category": "Category II Flexible Plastic",
        "typical_uses": ["paneer", "dairy", "cheese", "vacuum_meat"]
    },
    {
        "id": "glass_jar_lug",
        "name": "Food-Grade Soda Lime Glass Jar with Lug Cap & Plastisol Liner",
        "structure_code": "Glass Jar + Lug Cap",
        "description": "Chemically inert, 100% impermeable rigid barrier for high-acid, high-oil preserves and viscous syrups.",
        "layers": [
            {
                "layer_type": "outer",
                "name": "Soda-Lime Silica Glass Body (USP Type III)",
                "short_name": "Silica Glass (2.2mm)",
                "thickness_um": 2200,
                "color": "#06b6d4",  # cyan
                "role_en": "Zero chemical migration, impervious to acid, oil, oxygen, and vapor",
                "role_hi": "अम्ल और तेल के विरुद्ध पूर्ण अभेद्यता एवं शून्य प्रवासन",
                "standards": "IS 2837:1997 / IS 1382"
            },
            {
                "layer_type": "barrier",
                "name": "Vacuum Hermetic Headspace (Steam Vac Lug Cap)",
                "short_name": "Vacuum Lug Seal",
                "thickness_um": 200,
                "color": "#f59e0b",
                "role_en": "Safety button pop-up indicator, tamper-evident anaerobic closure",
                "role_hi": "वैक्यूम सुरक्षा बटन और एयर-टाइट ढक्कन",
                "standards": "IS 14887 / ASTM D2063"
            },
            {
                "layer_type": "sealant",
                "name": "Food-Grade PVC-Free Plastisol Gasket",
                "short_name": "Plastisol Gasket",
                "thickness_um": 500,
                "color": "#10b981",
                "role_en": "Acid-resistant, oil-resistant seal compound meeting migration limits",
                "role_hi": "अम्ल-प्रतिरोधी खाद्य-सुरक्षित गैसकेट",
                "standards": "IS 9845 (Simulant B & D compliance)"
            }
        ],
        "otr": 0.01,
        "wvtr": 0.01,
        "total_thickness_um": 2900,
        "cost_index": 3.8,
        "sustainability_index": 4.5,  # 100% infinitely recyclable
        "fssai_schedule": "Schedule IV (Acidic foods & Preserves)",
        "bis_code": "IS 2837:1997 (Glass containers for food industry)",
        "epr_category": "Category I Rigid (Non-Plastic Glass Exempt from PWM Plastic EPR)",
        "typical_uses": ["pickle", "honey", "chutneys", "preserves"]
    },
    {
        "id": "tinplate_canister",
        "name": "Tinplate Canister (220µm) with Food-Grade Epoxy-Phenolic Lacquer",
        "structure_code": "Tinplate E2.8/2.8 + Epoxy Lacquer",
        "description": "Hermetic rigid tin container providing 100% light block and gas exclusion for pure lipids and dairy fat.",
        "layers": [
            {
                "layer_type": "outer",
                "name": "Electrolytic Tinplate Sheet (Base Steel 0.22mm)",
                "short_name": "Tinplate 0.22mm",
                "thickness_um": 220,
                "color": "#64748b",
                "role_en": "Rigid structural crush resistance, absolute opacity to all light",
                "role_hi": "मजबूत धातुई संरचना एवं पूर्ण प्रकाश अवरोधक",
                "standards": "IS 1997:2006 (Tinplate for food packaging)"
            },
            {
                "layer_type": "barrier",
                "name": "Double-Seamed Top/Bottom End Seam",
                "short_name": "Double Seam",
                "thickness_um": 100,
                "color": "#f59e0b",
                "role_en": "Hermetic mechanical interlock preventing micro-leakage",
                "role_hi": "शून्य लीकेज वाली डबल सीम",
                "standards": "IS 9396 / ASTM F2013"
            },
            {
                "layer_type": "sealant",
                "name": "Food-Grade Gold Epoxy-Phenolic Internal Lacquer",
                "short_name": "Epoxy Lacquer (8 g/m2)",
                "thickness_um": 15,
                "color": "#eab308",
                "role_en": "Prevents tin dissolution and sulfur/fat staining, BPA-NI certified",
                "role_hi": "धातु को वसा और रसायनों से सुरक्षित रखने वाला आंतरिक लेप",
                "standards": "IS 9845 (Overall Migration < 60 mg/kg)"
            }
        ],
        "otr": 0.00,
        "wvtr": 0.00,
        "total_thickness_um": 235,
        "cost_index": 4.5,
        "sustainability_index": 4.8,  # Highly recycled metal
        "fssai_schedule": "Schedule IV & Schedule II (Metals and alloys)",
        "bis_code": "IS 1997:2006 (Tinplate containers) & IS 10146:2021",
        "epr_category": "Category I Rigid Metal",
        "typical_uses": ["ghee", "edible_oil", "milk_powder"]
    },
    {
        "id": "bopp_ldpe_pouch",
        "name": "20µm Plain BOPP / 30µm LDPE Heat-Seal Film",
        "structure_code": "BOPP20 / PE30",
        "description": "Cost-effective, high-transparency duplex pouch for moisture control in savouries and ready-to-fry foods.",
        "layers": [
            {
                "layer_type": "outer",
                "name": "20µm Biaxially-Oriented Polypropylene (BOPP)",
                "short_name": "20µm BOPP",
                "thickness_um": 20,
                "color": "#38bdf8",
                "role_en": "High gloss, water barrier, print surface",
                "role_hi": "उच्च पारदर्शिता और नमी अवरोध",
                "standards": "IS 12252:2018"
            },
            {
                "layer_type": "sealant",
                "name": "30µm Food-Grade LDPE Liner",
                "short_name": "30µm LDPE",
                "thickness_um": 30,
                "color": "#34d399",
                "role_en": "Reliable heat sealing, tear resistance",
                "role_hi": "मजबूत सील और फटने से बचाव",
                "standards": "IS 10146:2021"
            }
        ],
        "otr": 1400.0,
        "wvtr": 4.2,
        "total_thickness_um": 50,
        "cost_index": 1.6,
        "sustainability_index": 3.8,  # Polyolefin mono-material design (PP/PE recyclable)
        "fssai_schedule": "Schedule IV & Schedule III (Plastics)",
        "bis_code": "IS 10146:2021 (PE Contact Layer) & IS 12252:2018",
        "epr_category": "Category II Flexible Plastic",
        "typical_uses": ["papad", "dry_snacks", "noodles"]
    },
    {
        "id": "kraft_pe_extrusion",
        "name": "60 GSM Multi-wall Bleached Kraft Paper / 25µm PE Extrusion",
        "structure_code": "Kraft60 / PE25",
        "description": "Breathable, high-puncture paper-poly substrate balancing hygroscopic moisture control and fiber rigidity.",
        "layers": [
            {
                "layer_type": "outer",
                "name": "60 GSM Virgin Bleached Kraft Paper",
                "short_name": "60 GSM Kraft Paper",
                "thickness_um": 75,
                "color": "#d97706",  # brown/amber
                "role_en": "Natural fiber stiffness, biodegradable outer, high burst factor (IS 6615)",
                "role_hi": "प्राकृतिक क्राफ्ट पेपर, उच्च फटने की ताकत और मजबूती",
                "standards": "IS 6615:2020 (Kraft Paper)"
            },
            {
                "layer_type": "sealant",
                "name": "25µm Food-Grade LDPE Extrusion Coating",
                "short_name": "25µm PE Coating",
                "thickness_um": 25,
                "color": "#10b981",
                "role_en": "Moisture barrier preventing paper dampening and sugar caking",
                "role_hi": "नमी अवरोधक जो कागज को सीलने और चीनी/गुड़ को पिघलने से रोकता है",
                "standards": "IS 10146:2021 / IS 9845"
            }
        ],
        "otr": 950.0,
        "wvtr": 4.5,
        "total_thickness_um": 100,
        "cost_index": 2.2,
        "sustainability_index": 4.0,  # 70%+ bio-based paper content
        "fssai_schedule": "Schedule IV & Schedule I (Paper) / Schedule III (PE)",
        "bis_code": "IS 6615:2020 (Paper) & IS 10146:2021 (PE)",
        "epr_category": "Category II Flexible (Paper Composite)",
        "typical_uses": ["mahua", "jaggery", "flour", "grains"]
    },
    {
        "id": "hdpe_woven_sack",
        "name": "50µm Heavy-Duty Woven HDPE Sack with 25µm LDPE Inner Liner",
        "structure_code": "HDPE Woven + LDPE Liner",
        "description": "High tensile bulk storage sack engineered for agricultural commodities, flours, and forest produce transport.",
        "layers": [
            {
                "layer_type": "outer",
                "name": "High-Density Polyethylene (HDPE) Woven Fabric (10x10 mesh)",
                "short_name": "HDPE Woven Fabric",
                "thickness_um": 80,
                "color": "#475569",
                "role_en": "Massive tensile and burst strength for 10-50kg bulk handling",
                "role_hi": "भारी वजन परिवहन के लिए उच्च मजबूती वाली बुनी हुई बोरी",
                "standards": "IS 14887:2014"
            },
            {
                "layer_type": "sealant",
                "name": "25µm Virgin LDPE Loose/Tack-Welded Inner Liner",
                "short_name": "25µm LDPE Liner",
                "thickness_um": 25,
                "color": "#10b981",
                "role_en": "Blocks humidity ingress, dust contamination, and insect infestation",
                "role_hi": "सीलन, धूल और कीड़े-मकोड़ों से सुरक्षा देने वाला आंतरिक लाइनर",
                "standards": "IS 10146:2021"
            }
        ],
        "otr": 1800.0,
        "wvtr": 5.5,
        "total_thickness_um": 105,
        "cost_index": 1.5,
        "sustainability_index": 3.8,  # 100% recyclable polyolefin
        "fssai_schedule": "Schedule IV (Cereals, grains and pulses)",
        "bis_code": "IS 14887:2014 (HDPE Sacks) & IS 10146:2021",
        "epr_category": "Category II Flexible Plastic",
        "typical_uses": ["ragi", "tendu", "grains", "millets", "pulses"]
    },
    {
        "id": "compostable_pla_pbat",
        "name": "45µm Certified Compostable Bio-based PLA / PBAT Barrier Film",
        "structure_code": "PLA / PBAT / Bio-PBS (45µm)",
        "description": "100% industrially compostable bio-polymer film meeting IS 17088 with bio-derived moisture and oxygen control.",
        "layers": [
            {
                "layer_type": "outer",
                "name": "15µm Polylactic Acid (Corn-derived PLA)",
                "short_name": "15µm Bio-PLA",
                "thickness_um": 15,
                "color": "#84cc16",  # lime green
                "role_en": "Renewable plant origin, high transparency, natural UV filtering",
                "role_hi": "पौधों से निर्मित प्राकृतिक पॉलीमर, उच्च स्पष्टता",
                "standards": "IS 17088:2021 (Compostable Plastics)"
            },
            {
                "layer_type": "barrier",
                "name": "15µm Polybutylene Succinate (PBS) Barrier Core",
                "short_name": "15µm Bio-PBS Core",
                "thickness_um": 15,
                "color": "#a3e635",
                "role_en": "Enhanced moisture barrier in biodegradable matrix",
                "role_hi": "बायोडिग्रेडेबल मैट्रिक्स में नमी अवरोधक",
                "standards": "ISO 17088 / ASTM D6400"
            },
            {
                "layer_type": "sealant",
                "name": "15µm Polybutylene Adipate Terephthalate (PBAT) Sealant",
                "short_name": "15µm PBAT Sealant",
                "thickness_um": 15,
                "color": "#4ade80",
                "role_en": "Flexible, low-temperature sealability, 100% biodegradable in 180 days",
                "role_hi": "180 दिनों में खाद में बदलने वाला लचीला सीलेंट",
                "standards": "IS 17088:2021 (CPCB-Certified)"
            }
        ],
        "otr": 450.0,
        "wvtr": 3.8,
        "total_thickness_um": 45,
        "cost_index": 3.6,
        "sustainability_index": 5.0,  # 100% compostable
        "fssai_schedule": "Schedule IV & Schedule III (Biodegradable Polymers)",
        "bis_code": "IS 17088:2021 (Specifications for Compostable Plastics)",
        "epr_category": "Category IV Compostable Plastic (Exempt from PWM recycling targets)",
        "typical_uses": ["jaggery", "organic_snacks", "tea", "dried_apricots"]
    },
    {
        "id": "microperf_antifog_bopp",
        "name": "30µm Micro-Perforated Anti-Fog BOPP / Punched Tray",
        "structure_code": "BOPP-AF 30µm (Laser Micro-Perforated)",
        "description": "Equilibrium Modified Atmosphere Packaging (EMAP) film engineered for ultra-high respiration horticultural produce.",
        "layers": [
            {
                "layer_type": "outer",
                "name": "30µm Laser Micro-perforated Polypropylene (50µm hole dia, 40 holes/pack)",
                "short_name": "30µm Micro-perf BOPP",
                "thickness_um": 30,
                "color": "#0ea5e9",
                "role_en": "Controls O2/CO2 flux preventing anaerobiosis while curbing condensation",
                "role_hi": "गैस संचरण नियंत्रण जिससे उत्पाद बंद पैकेट में सड़े नहीं",
                "standards": "ASTM D3985 / ASTM F1249 Modified"
            },
            {
                "layer_type": "sealant",
                "name": "Food-Contact Hydrophilic Anti-Fog Internal Coating",
                "short_name": "Anti-Fog Coating",
                "thickness_um": 2,
                "color": "#38bdf8",
                "role_en": "Spreads droplets into invisible water sheet; prevents Botrytis mold spotting",
                "role_hi": "भाप की बूंदों को फैलने से रोककर फफूंद से सुरक्षा",
                "standards": "IS 10146:2021"
            }
        ],
        "otr": 4800.0,  # Breathable
        "wvtr": 35.0,   # Permeable
        "total_thickness_um": 32,
        "cost_index": 2.5,
        "sustainability_index": 3.9,
        "fssai_schedule": "Schedule IV (Fresh fruits & vegetables)",
        "bis_code": "IS 10146:2021 (PE/PP Contact) & IS 12252:2018",
        "epr_category": "Category II Flexible Plastic",
        "typical_uses": ["mushroom", "leafy_greens", "broccoli", "fresh_cut"]
    },
    {
        "id": "vented_pet_clamshell",
        "name": "280µm Vented Rigid PET Clamshell with Punched Absorption Pad",
        "structure_code": "APET 280µm + Macro Vents",
        "description": "Rigid crush-proof transparent thermoformed container with convection ventilation slots for soft fruits.",
        "layers": [
            {
                "layer_type": "outer",
                "name": "280µm Amorphous Polyethylene Terephthalate (APET)",
                "short_name": "280µm Rigid APET",
                "thickness_um": 280,
                "color": "#0284c7",
                "role_en": "Impact resistance against bruising during transport; crystal glass clarity",
                "role_hi": "परिवहन में फलों को दबने से बचाने वाला मजबूत पारदर्शी क्लैमशेल",
                "standards": "IS 12252:2018 (PET Rigid)"
            },
            {
                "layer_type": "barrier",
                "name": "Side Wall Slotted Convection Air Vents (4% open area)",
                "short_name": "Convection Vents",
                "thickness_um": 0,
                "color": "#93c5fd",
                "role_en": "Rapid pre-cooling airflow, dissipates field heat and respiratory CO2",
                "role_hi": "ठंडी हवा का बहाव जिससे फल ताजा बने रहें",
                "standards": "ISO 15105"
            },
            {
                "layer_type": "sealant",
                "name": "Food-Grade Cellulose Liquid Absorption Bottom Pad",
                "short_name": "Cellulose Pad",
                "thickness_um": 500,
                "color": "#f1f5f9",
                "role_en": "Absorbs exudate juice; starves surface yeast and grey mold",
                "role_hi": "रिसाव को सोखने वाला फूड-ग्रेड पैड",
                "standards": "IS 6615:2020"
            }
        ],
        "otr": 9500.0,
        "wvtr": 65.0,
        "total_thickness_um": 280,
        "cost_index": 2.4,
        "sustainability_index": 4.2,  # 100% recyclable PET (Category 1)
        "fssai_schedule": "Schedule IV (Fresh Fruits & Vegetables)",
        "bis_code": "IS 12252:2018 (Rigid PET Food Containers)",
        "epr_category": "Category I Rigid Plastic",
        "typical_uses": ["strawberry", "berries", "grapes", "cherry_tomatoes"]
    }
]


# =====================================================================
# BIOPHYSICAL MATHEMATICAL FORMULAS
# =====================================================================

def calculate_saturation_vapor_pressure_kpa(temp_c: float) -> float:
    """
    Computes saturation water vapor pressure ps(T) in kPa using the Tetens Equation.
    """
    return 0.61078 * math.exp((17.27 * temp_c) / (temp_c + 237.3))


def calculate_target_wvtr(
    moisture_pct: float,
    shelf_life_days: float,
    storage_temp_c: float = 30.0,
    ambient_rh: float = 0.70,
    pack_weight_g: float = 250.0,
    pouch_area_m2: float = 0.065
) -> Dict[str, Any]:
    """
    Moisture Sorption Kinetics Model:
    Calculates the maximum permissible WVTR (g/m2/day) required to keep product moisture
    below critical spoilage threshold Mc across target shelf life theta.
    Formula:
        WVTR_req = (Ws * (Mc - M0)) / (A * theta * (R1 - R2) * (ps(T) / ps_std))
    """
    safe_m0 = max(0.1, min(99.0, float(moisture_pct)))
    m0_fraction = safe_m0 / 100.0
    pack_wt = max(10.0, float(pack_weight_g))
    pouch_area = max(0.01, float(pouch_area_m2))
    effective_days = max(1.0, float(shelf_life_days))
    safe_temp = max(-20.0, min(55.0, float(storage_temp_c)))

    # Ambient RH normalization
    safe_rh = float(ambient_rh)
    if safe_rh > 1.0:
        safe_rh = safe_rh / 100.0
    safe_rh = max(0.05, min(0.99, safe_rh))

    dry_solids_g = max(1.0, pack_wt * (1.0 - m0_fraction))

    # Determine critical moisture limit Mc based on commodity moisture regime
    if safe_m0 <= 8.0:
        # Crisp snacks / powders (lose crispiness when moisture rises by 2.5-3.0%)
        mc_fraction = (safe_m0 + 2.5) / 100.0
        internal_aw = 0.22
    elif safe_m0 <= 16.0:
        # Flours / pulses / dried fruit (spoilage / mold risk when moisture rises by 3.5%)
        mc_fraction = min(0.20, (safe_m0 + 3.5) / 100.0)
        internal_aw = 0.45
    elif safe_m0 >= 80.0:
        # Fresh produce (loss of 5% fresh weight through transpiration causes shriveling)
        mc_fraction = max(0.60, (safe_m0 - 5.0) / 100.0)
        internal_aw = 0.98
    else:
        # Intermediate moisture preserves / pastes
        mc_fraction = (safe_m0 + 4.0) / 100.0
        internal_aw = 0.65

    # Guard moisture delta to prevent zero-division or inverted boundary issues (M0 >= Mc)
    moisture_delta_pct = max(0.5, abs(mc_fraction * 100.0 - safe_m0))
    delta_m_water_g = max(0.1, dry_solids_g * (moisture_delta_pct / 100.0))

    ps_actual_kpa = calculate_saturation_vapor_pressure_kpa(safe_temp)
    ps_std_kpa = calculate_saturation_vapor_pressure_kpa(38.0)  # ASTM F1249 test condition: 38C, 90% RH

    # Guard driving RH gradient: rh_gradient = max(0.05, abs(ambient_rh - aw_product))
    delta_rh = max(0.05, abs(safe_rh - internal_aw))

    # Water flux allowable under actual storage conditions
    flux_actual = delta_m_water_g / (pouch_area * effective_days)

    # Convert to ASTM F1249 equivalent at 38C, 90% RH
    # Driving force ratio = (0.90 * ps_std) / (delta_rh * ps_actual)
    driving_force_ratio = (0.90 * ps_std_kpa) / (delta_rh * max(0.1, ps_actual_kpa))
    raw_wvtr = flux_actual * driving_force_ratio

    # Boundary safety clamping: clamp between 0.02 and 1500.0 g/m2/day
    if safe_m0 >= 85.0:
        target_wvtr = max(25.0, min(raw_wvtr, 1500.0))  # Produce must be permeable
    else:
        target_wvtr = max(0.02, min(raw_wvtr, 1500.0))

    return {
        "target_wvtr": round(target_wvtr, 2),
        "delta_m_water_g": round(delta_m_water_g, 2),
        "dry_solids_g": round(dry_solids_g, 1),
        "saturation_pressure_kpa": round(ps_actual_kpa, 2),
        "critical_moisture_pct": round(mc_fraction * 100.0, 1),
        "internal_aw": internal_aw
    }


def calculate_target_otr(
    fat_oil_pct: float,
    shelf_life_days: float,
    respiration_class: str = "Very Low",
    storage_temp_c: float = 30.0,
    pack_weight_g: float = 250.0,
    pouch_area_m2: float = 0.065
) -> Dict[str, Any]:
    """
    Lipid Oxidation Kinetics & Produce Respiration Model:
    Calculates target OTR (cc/m2/day at 23C) based on fat content and peroxide value limits,
    or Kader's Q10 temperature-dependent produce respiration model.
    """
    safe_fat = max(0.0, min(100.0, float(fat_oil_pct)))
    fat_fraction = safe_fat / 100.0
    pack_wt = max(10.0, float(pack_weight_g))
    pouch_area = max(0.01, float(pouch_area_m2))
    fat_mass_kg = (pack_wt * fat_fraction) / 1000.0
    effective_days = max(1.0, float(shelf_life_days))
    rc_lower = (respiration_class or "").lower()

    if any(k in rc_lower for k in ["high", "very high", "extremely high"]):
        # Produce Respiration Model (Kader Q10)
        # R(T) = R0 * Q10 ^ ((T - T0) / 10)
        r0 = 40.0 if "extremely" in rc_lower else 20.0  # mg CO2 / kg-hr at 5C
        q10 = 2.3
        t0 = 5.0
        safe_temp = max(-10.0, min(55.0, float(storage_temp_c)))
        q10_power = max(-2.0, min(5.0, (safe_temp - t0) / 10.0))
        r_actual = r0 * (q10 ** q10_power)
        # O2 consumption: 1 mg CO2 ≈ 0.51 cc O2 consumed
        o2_rate_cc_kg_day = r_actual * 0.51 * 24.0
        total_o2_demand_cc_day = (o2_rate_cc_kg_day * (pack_wt / 1000.0))
        raw_otr = total_o2_demand_cc_day / pouch_area
        target_otr = max(2500.0, min(5000.0, raw_otr))

        return {
            "target_otr": round(target_otr, 1),
            "mechanism": "Active Metabolic Respiration (Kader Q10)",
            "respiration_rate_mg_kg_hr": round(r_actual, 1),
            "map_gas_equilibrium": "O2: 3-5% | CO2: 5-10% | N2: Balance",
            "is_produce": True
        }

    # Lipid Oxidation Mechanism
    # Codex / FSSAI standards:
    # Pure fats (>80% fat like Ghee): Strict PV increase limit <= 1.5 meq O2 / kg fat
    # Moderate / high fats (5-80%): Sensory rancidity threshold <= 8.0 meq O2 / kg fat
    if safe_fat >= 80.0:
        delta_pv_max = 1.5  # meq/kg (FSSAI strict standard for pure milk fat / ghee)
    else:
        delta_pv_max = 8.0  # meq/kg (Confectionery and fried snacks)

    max_o2_absorbed_cc = max(0.01, fat_mass_kg * delta_pv_max * 11.2)

    if safe_fat >= 80.0:
        # Pure lipid fat (ghee, butter oil) - requires hermetic barrier (OTR < 1.0)
        allowable_daily_o2_cc = max_o2_absorbed_cc / effective_days
        raw_otr = allowable_daily_o2_cc / (pouch_area * 0.21)
        target_otr = max(0.05, min(1.0, raw_otr))
    elif safe_fat >= 20.0:
        # High fat product (chikki, namkeen, nuts)
        allowable_daily_o2_cc = max_o2_absorbed_cc / effective_days
        raw_otr = allowable_daily_o2_cc / (pouch_area * 0.21)
        target_otr = max(0.5, min(25.0, raw_otr))
    elif safe_fat >= 5.0:
        # Moderate fat (cookies, flours)
        allowable_daily_o2_cc = max_o2_absorbed_cc / effective_days
        raw_otr = allowable_daily_o2_cc / (pouch_area * 0.21)
        target_otr = max(1.0, min(80.0, raw_otr))
    else:
        # Low fat / lean commodities
        target_otr = 1500.0

    target_otr = max(0.05, min(5000.0, target_otr))

    return {
        "target_otr": round(target_otr, 2),
        "mechanism": "Lipid Peroxidation & Auto-oxidation Prevention",
        "max_permissible_o2_intake_cc": round(max_o2_absorbed_cc, 2),
        "map_gas_equilibrium": "N2 Flush: 95-98% (O2 < 2%)" if safe_fat >= 10.0 else "N/A",
        "is_produce": False
    }


def solve_optimal_laminate(
    target_wvtr: float,
    target_otr: float,
    commodity_id: str,
    moisture_pct: float,
    fat_oil_pct: float,
    ph_value: float,
    storage_type: str,
    respiration_class: str
) -> Dict[str, Any]:
    """
    Multi-objective material science solver:
    Evaluates candidate laminate structures against biophysical demands,
    ranks by safety margin, barrier index, cost index, and sustainability.
    """
    candidates = []
    is_produce = any(k in (respiration_class or "").lower() for k in ["high", "very high", "extremely high"])

    # Determine required packaging format (rigid vs flexible vs breathable tray)
    cid_lower = (commodity_id or "").lower()
    is_liquid_or_paste = any(k in cid_lower for k in ["pickle", "honey", "preserve", "jam"])
    is_pure_fat = any(k in cid_lower for k in ["ghee", "oil"]) or (fat_oil_pct >= 80.0)

    for lam in LAMINATE_CATALOG:
        lam_id = lam["id"]

        # Produce filter: produce requires high breathability
        if is_produce:
            if lam["otr"] < 2000.0:
                continue  # Cannot suffocate fresh produce
        else:
            if lam["otr"] > 3000.0:
                continue  # Cannot use breathable film on dry/fatty food

        # Rigid glass/tin format filtering:
        if lam_id == "glass_jar_lug" and not is_liquid_or_paste:
            continue
        if lam_id == "tinplate_canister" and not is_pure_fat:
            continue

        if is_liquid_or_paste and "pouch" in lam_id and "bopa_evoh" not in lam_id:
            continue

        # Calculate safety margins
        if is_produce:
            margin_wvtr = round(lam["wvtr"] / max(0.1, target_wvtr), 2)
            margin_otr = round(lam["otr"] / max(0.1, target_otr), 2)
            barrier_score = 1.0 / (1.0 + abs(margin_otr - 1.0) + abs(margin_wvtr - 1.0)) * 100.0
        else:
            margin_wvtr = round(target_wvtr / max(0.01, lam["wvtr"]), 2)
            margin_otr = round(target_otr / max(0.01, lam["otr"]), 2)
            eff_margin = min(5.0, margin_wvtr) * 0.5 + min(5.0, margin_otr) * 0.5
            barrier_score = min(100.0, eff_margin * 20.0)

        suitability_bonus = 35.0 if commodity_id in lam.get("typical_uses", []) else 0.0

        if ph_value < 4.0 and "foil" in lam["id"] and "pet_foil" not in lam["id"]:
            acid_penalty = -30.0
        else:
            acid_penalty = 0.0

        total_score = (
            0.40 * barrier_score +
            0.25 * suitability_bonus +
            0.20 * (lam["sustainability_index"] * 20.0) +
            0.15 * ((5.0 - lam["cost_index"]) * 20.0) +
            acid_penalty
        )

        overall_sf = round(min(margin_wvtr, margin_otr) if not is_produce else margin_otr, 2)
        candidates.append({
            "laminate": lam,
            "margin_wvtr": margin_wvtr,
            "margin_otr": margin_otr,
            "overall_safety_factor": overall_sf,
            "score": round(total_score, 1)
        })

    # Sort descending by fitness score
    candidates.sort(key=lambda x: x["score"], reverse=True)

    warning_flag = None

    if candidates:
        primary_candidate = candidates[0]
        # Check if the safety factor is < 1.0 (barrier deficit under severe tropical stress)
        if primary_candidate["overall_safety_factor"] < 1.0 and not is_produce:
            # Fallback to absolute highest barrier substrate in catalog (Foil triplex)
            foil_candidate = next((c for c in candidates if "foil" in c["laminate"]["id"]), primary_candidate)
            primary_candidate = foil_candidate
            warning_flag = "CRITICAL_BARRIER_WARNING: Target shelf life exceeds standard flexible packaging barrier limits under tropical conditions. Vacuum seal or nitrogen flush mandatory."
    else:
        # Ultimate resilient fallback if all candidates filtered out
        primary_candidate = {
            "laminate": LAMINATE_CATALOG[0],  # pet_al_pe (highest barrier)
            "overall_safety_factor": 0.85,
            "score": 75.0
        }
        warning_flag = "CRITICAL_BARRIER_WARNING: Target shelf life exceeds standard flexible packaging barrier limits under tropical conditions. Vacuum seal or nitrogen flush mandatory."

    # Find best sustainable alternative (sustainability >= 4.0)
    alt_candidates = [c for c in candidates if c["laminate"]["id"] != primary_candidate["laminate"]["id"]]
    alt_candidates.sort(key=lambda x: (x["laminate"]["sustainability_index"], x["score"]), reverse=True)
    alt_candidate = alt_candidates[0] if alt_candidates else primary_candidate

    return {
        "primary_structure": primary_candidate["laminate"],
        "primary_safety_factor": primary_candidate["overall_safety_factor"],
        "primary_score": primary_candidate["score"],
        "alt_structure": alt_candidate["laminate"],
        "alt_safety_factor": alt_candidate["overall_safety_factor"],
        "candidate_count": len(candidates),
        "warning_flag": warning_flag
    }


def generate_shelf_life_decay_curves(
    commodity_id: str,
    moisture_pct: float,
    fat_oil_pct: float,
    shelf_life_days: float,
    primary_laminate: Dict[str, Any],
    respiration_class: str
) -> Dict[str, Any]:
    """
    Generates dynamic 0 to 365 days shelf-life degradation curve points:
      - Curve A: Unpackaged Control (rapid decay in 3-15 days)
      - Curve B: Generic Monolayer Plastic (25µ LDPE - suboptimal barrier)
      - Curve C: Recommended Multi-Layer Barrier (preserves quality past target shelf life)
    """
    days_range = list(range(0, 366, 15))
    is_produce = any(k in respiration_class.lower() for k in ["high", "very high", "extremely high"])
    threshold_value = 100.0  # Quality index starts at 100%, failure at threshold (e.g. 50%)

    curve_unpackaged = []
    curve_monolayer = []
    curve_recommended = []

    # Decay rate constants (k_loss in days^-1)
    if is_produce:
        k_un = 0.25   # Unpackaged produce wilts in 4 days
        k_mono = 0.08 # Generic bag rots in 10-12 days due to anaerobic condensation
        k_rec = 0.025 # Breathable MAP maintains freshness 25-30 days
    elif fat_oil_pct >= 15.0:
        k_un = 0.09   # Lipid rancidity in 10-15 days
        k_mono = 0.022# Monolayer LDPE rancid in 45 days (OTR 2000)
        k_rec = 0.002 # High barrier foil/EVOH preserves 365+ days
    elif moisture_pct <= 10.0:
        k_un = 0.12   # Crisp snacks go soggy in 7 days
        k_mono = 0.018# Monolayer goes soggy in 50 days
        k_rec = 0.0015# Metallized/foil barrier preserves 365+ days
    else:
        k_un = 0.08
        k_mono = 0.015
        k_rec = 0.003

    for day in days_range:
        # Quality retention exponential decay: Q(t) = 100 * exp(-k * t)
        q_un = round(max(0.0, 100.0 * math.exp(-k_un * day)), 1)
        q_mono = round(max(0.0, 100.0 * math.exp(-k_mono * day)), 1)
        q_rec = round(max(0.0, 100.0 * math.exp(-k_rec * day)), 1)

        curve_unpackaged.append({"day": day, "quality_pct": q_un})
        curve_monolayer.append({"day": day, "quality_pct": q_mono})
        curve_recommended.append({"day": day, "quality_pct": q_rec})

    # Find days to reach failure threshold (quality < 50%)
    days_to_fail_un = round(math.log(2.0) / k_un, 1)
    days_to_fail_mono = round(math.log(2.0) / k_mono, 1)
    days_to_fail_rec = round(math.log(2.0) / k_rec, 1)

    return {
        "days": days_range,
        "curve_unpackaged": curve_unpackaged,
        "curve_monolayer": curve_monolayer,
        "curve_recommended": curve_recommended,
        "critical_threshold_pct": 50.0,
        "days_to_failure": {
            "unpackaged": days_to_fail_un,
            "monolayer": days_to_fail_mono,
            "recommended": days_to_fail_rec
        }
    }


def get_is9845_simulant_matrix(ph_value: float, fat_oil_pct: float, category: str) -> Dict[str, Any]:
    """
    Determines mandatory migration testing simulants and protocols per IS 9845:1998.
    Table 1 prescribed simulants:
      - Simulant A: Distilled Water (Aqueous foods pH > 4.5)
      - Simulant B: 3% Acetic Acid (Acidic foods pH <= 4.5)
      - Simulant C: 15% Ethanol (Alcoholic / high sugar solutions)
      - Simulant D: n-Heptane / Olive Oil (Fatty foods & edible oils)
    """
    cat_lower = (category or "").lower()
    is_acidic = ph_value <= 4.5 or any(k in cat_lower for k in ["pickle", "fruit", "preserve", "citrus"])
    is_fatty = fat_oil_pct >= 5.0 or any(k in cat_lower for k in ["oil", "fat", "dairy", "pickle", "snack", "bakery", "chikki", "ghee", "nut"])
    is_alcoholic_or_sweet = any(k in cat_lower for k in ["syrup", "juice", "beverage", "jaggery", "honey"])

    if is_fatty:
        food_class = "Class IV: Fatty Foods & Edible Oils"
        primary_simulant = "Simulant D"
    elif is_acidic:
        food_class = "Class II: Acidic Foods & Preserves"
        primary_simulant = "Simulant B"
    elif is_alcoholic_or_sweet:
        food_class = "Class III: Moist Sugary & Alcoholic Products"
        primary_simulant = "Simulant C"
    else:
        food_class = "Class I: Neutral Aqueous & Dry Solids"
        primary_simulant = "Simulant A"

    simulants = [
        {
            "code": "Simulant A",
            "simulant_code": "Simulant A",
            "name": "Distilled Water (Pure Neutral Medium)",
            "description": "Distilled Water (Neutral Aqueous Foods)",
            "target_food": "Aqueous / neutral foods (pH > 4.5, pulses, cereals, spices)",
            "applies_to": "All neutral aqueous and dry contact food products",
            "condition": "40°C ± 2°C for 10 Days (or 70°C for 2 Hours)",
            "limit": "≤ 60 mg/kg or ≤ 10 mg/dm²",
            "applicable": True if not is_fatty else False
        },
        {
            "code": "Simulant B",
            "simulant_code": "Simulant B",
            "name": "3% w/v Acetic Acid in Distilled Water",
            "description": "3% w/v Acetic Acid (Acidic Foods)",
            "target_food": "Acidic foods & preserves (pH ≤ 4.5, pickles, tomato paste, citrus)",
            "applies_to": f"Products with pH {ph_value:.1f} ≤ 4.5 (Heavy metal leaching test)",
            "condition": "40°C ± 2°C for 10 Days (or 70°C for 2 Hours)",
            "limit": "≤ 60 mg/kg (Zero toxic metal migration)",
            "applicable": bool(is_acidic)
        },
        {
            "code": "Simulant C",
            "simulant_code": "Simulant C",
            "name": "15% v/v Ethanol in Distilled Water",
            "description": "15% Ethanol (Sweet / Moist Products)",
            "target_food": "Moist sugary foods, fruit squashes, syrups & alcoholic beverages",
            "applies_to": "Sugary matrices and hydroalcoholic preserves",
            "condition": "40°C ± 2°C for 10 Days",
            "limit": "≤ 60 mg/kg or ≤ 10 mg/dm²",
            "applicable": bool(is_alcoholic_or_sweet and not is_fatty)
        },
        {
            "code": "Simulant D",
            "simulant_code": "Simulant D",
            "name": "n-Heptane / Rectified Olive Oil",
            "description": "n-Heptane / Iso-octane (Fatty Food Simulant)",
            "target_food": "Fatty foods, fried snacks, dairy fats & edible oils (fat > 5%)",
            "applies_to": f"Products with {fat_oil_pct:.1f}% Fat/Oil (Lipid leaching test)",
            "condition": "n-Heptane: 20°C for 30 Mins (or Olive Oil: 40°C for 10 Days)",
            "limit": "≤ 60 mg/kg (Subject to reduction factor)",
            "applicable": bool(is_fatty)
        }
    ]

    return {
        "standard": "IS 9845 : 1998 (Reaffirmed 2014)",
        "governing_standard": "IS 9845:1998 (Methods of analysis for overall migration)",
        "title": "Determination of Overall Migration of Constituents of Plastics Materials",
        "food_classification": food_class,
        "statutory_limit_mg_dm2": 10.0,
        "statutory_limit_mg_kg": 60.0,
        "overall_limit": "60 mg/kg (foodstuff) or 10 mg/dm² (contact area)",
        "primary_simulant": primary_simulant,
        "heavy_metal_screening": "Lead (Pb), Cadmium (Cd), Hexavalent Chromium (Cr VI), Mercury (Hg) < 100 ppm total",
        "analytical_method": "Gravimetric residue evaporation of simulant leachate per IS 9845 Annex A",
        "simulants": simulants
    }
