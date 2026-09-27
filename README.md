# 🌿 PackAI India — SIH26236 Production Engine
### AI-Based Intelligent Food Packaging Material Recommendation System for Food Commodities
**Ministry of Food Processing Industries (MoFPI) | Smart India Hackathon (SIH) Problem Statement: SIH26236**  
*Target Initiative: Pradhan Mantri Formalisation of Micro food processing Enterprises (PMFME) & One District One Product (ODOP)*

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.x-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5.x-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev)
[![Scikit-Learn](https://img.shields.io/badge/ML%20Accuracy-92.2%25%20CV-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![FSSAI & BIS](https://img.shields.io/badge/Compliance-FSSAI%20%7C%20BIS%20%7C%20CPCB-138808?style=for-the-badge)](https://fssai.gov.in)
[![Offline-First](https://img.shields.io/badge/Offline%20First-Zero%20External%20APIs-22C55E?style=for-the-badge)](#)

---

## 📌 Executive Overview

In India's agro-food processing sector, micro-enterprises, Farmer Producer Organizations (FPOs), and Self-Help Groups (SHGs) under the **PMFME Scheme** face severe post-harvest losses and regulatory penalties due to:
1. **Unscientific Packaging Selection:** Relying on generic, non-barrier low-density poly bags (LDPE) leading to premature rancidity, moisture sogginess, and micro-perforation failures.
2. **Regulatory Non-Compliance:** Ignorance of mandatory statutory standards under the **Food Safety and Standards Authority of India (FSSAI)**, **Bureau of Indian Standards (BIS)**, and **Central Pollution Control Board (CPCB) Extended Producer Responsibility (EPR)**.
3. **Lack of Affordable Technical Tools:** Commercial packaging testing labs charge substantial consulting fees inaccessible to rural micro-processors.

**PackAI India** solves this bottleneck with an **offline-first, biophysically deterministic, AI-guided packaging recommendation engine and statutory compliance studio**. It converts physical food characteristics ($\text{moisture } M_0$, $\text{fat/oil } F$, $\text{pH}$, target shelf-life $\theta$, and ambient climate $T$, $\text{RH}$) into optimal multi-layer barrier laminates, FSSAI legal schedules, IS 9845 chemical simulant protocols, and 1-page statutory packaging readiness certificates.

---

## 🏛️ Interactive System Architecture

```mermaid
flowchart TD
    subgraph UI["1. Multimodal Presentation Layer (React 18 + Vite)"]
        A1["Voice Input (Web Speech API - hi-IN & en-IN)"]
        A2["18 Seeded PMFME/ODOP Crops + Custom Crop Studio"]
        A3["Environmental Sliders (T: 4-45°C, RH: 20-95%)"]
        A4["2.5D Laminate Structure Visualizer"]
        A5["Dynamic Shelf-Life Kinetics Simulator (SVG)"]
        A6["FSSAI 2020 SVG Mandatory Label Mockup"]
    end

    subgraph API["2. API Gateway & Micro-Services (FastAPI)"]
        B1["POST /api/recommend (Barrier Solver & ML Inference)"]
        B2["GET /api/compliance/{id} (Statutory Rules & Simulants)"]
        B3["POST /api/export-pdf (ReportLab 1-Page Generator)"]
        B4["GET /api/commodities & /api/translations (Bilingual)"]
    end

    subgraph Core["3. Biophysical Kinetics & Material Science Engine"]
        C1["Tetens Saturation Vapor Pressure: ps(T)"]
        C2["Moisture Sorption Kinetics: Target WVTR (g/m²/day)"]
        C3["Lipid Oxidation & Arrhenius Q10: Target OTR (cc/m²/day)"]
        C4["Respiration Permeation Matching (EMAP)"]
        C5["Multi-Criteria Barrier Laminate Constraint Solver"]
        C6["Scikit-Learn Decision Tree (Stratified 5-Fold CV: 92.2%)"]
        C7["Physics Authoritative Veto Logic"]
    end

    subgraph Legal["4. Indian Statutory Compliance & Certification Layer"]
        D1["FSSAI Packaging Regulations, 2018 (Schedule IV & I/II/III)"]
        D2["Bureau of Indian Standards (BIS Contact Standards: IS 10146, IS 12252, etc.)"]
        D3["IS 9845 Migration Matrix (Simulants A, B, C, D: 60 mg/kg OML)"]
        D4["CPCB Plastic Waste Management & EPR (Category I - IV)"]
        D5["FSSAI 2020 9-Point Mandatory Front/Back Display Checklist"]
        D6["Official 1-Page PMFME Packaging Readiness Certificate (PDF)"]
    end

    UI -->|JSON REST Payload| API
    API --> Core
    Core --> Legal
    Legal -->|Bilingual Readiness Bundle| API
    API -->|Realtime Reactive State| UI
```

---

## 🧮 Mathematical Foundations & Biophysical Kinetics

PackAI India abandons superficial static lookup tables in favor of deterministic biophysical equations:

### 1. Water Vapor Transmission Rate (WVTR) Demand
Governed by moisture sorption driving force under ambient temperature $T$ and relative humidity $R_1$, package equilibrium relative humidity $R_2$, dry solid mass $W_s$, critical moisture limit $M_c$, initial moisture $M_0$, pouch area $A$, and shelf life $\theta$:

$$\text{WVTR}_{\text{req}} = \frac{W_s \cdot (M_c - M_0)}{A \cdot \theta \cdot (R_1 - R_2) \cdot p_s(T)}$$

Where saturation vapor pressure $p_s(T)$ is dynamically calculated via the **Tetens Equation**:

$$p_s(T) = 0.61078 \exp\left(\frac{17.27 \cdot T}{T + 237.3}\right) \quad (\text{in kPa})$$

### 2. Oxygen Transmission Rate (OTR) & Arrhenius Oxidation
Lipid auto-oxidation rate doubles every 10°C according to the **Arrhenius $Q_{10}$ Temperature Quotient**:

$$k(T) = k_{20} \cdot Q_{10}^{(T - 20) / 10}, \quad Q_{10} \approx 2.1$$

For respiring fresh produce (e.g., mushrooms, strawberries), Equilibrium Modified Atmosphere Packaging (EMAP) requires high oxygen permeability to prevent anaerobic fermentation ($< 2\%\ \text{O}_2$) and ethanol accumulation:

$$\text{OTR}_{\text{req}} = \frac{R_{\text{O}_2} \cdot W}{A \cdot (0.21 - y_{\text{O}_2})}$$

### 3. Laminate Safety Factor ($\text{SF}$)
Every solved laminate structure must satisfy both moisture and oxygen barrier margins with an authoritative veto:

$$\text{SF} = \min\left(\frac{\text{WVTR}_{\text{allowable}}}{\text{WVTR}_{\text{structure}}}, \frac{\text{OTR}_{\text{allowable}}}{\text{OTR}_{\text{structure}}}\right) \ge 1.0$$

---

## 🇮🇳 The Statutory Compliance Layer (India Standards)

| Regulatory Body | Statute / Standard | Operationalized Engine Feature |
|---|---|---|
| **FSSAI** | **Food Safety & Standards (Packaging) Regulations, 2018** | Automated mapping of commodity to **Schedule IV** (food category specific restrictions) and **Schedule I/II/III** (approved polymers, paperboards, and tinplate). |
| **BIS** | **Bureau of Indian Standards** | Direct injection of mandatory Indian Standards into the specification (e.g., `IS 10146:2021` for PE contact layer, `IS 12252:2018` for BOPP/PET, `IS 8970` for Aluminium foil). |
| **BIS** | **IS 9845 Overall Migration Limits (OML)** | Automated evaluation of Overall Migration Limits ($\le 60\text{ mg/kg}$ or $\le 10\text{ mg/dm}^2$) across **Simulant A** (distilled water), **Simulant B** ($3\%$ acetic acid), **Simulant C** ($10\%$ ethanol), and **Simulant D** ($50\%$ ethanol / rectified spirit) based on pH and fat content. |
| **CPCB / MoEFCC** | **Plastic Waste Management Rules 2016 & 2022 EPR Amendment** | Classification into **Category I** (Rigid), **Category II** (Single/Multi-layer flexible), **Category III** (Multi-layered plastics with at least one non-plastic layer), or **Category IV** (Compostable). |
| **FSSAI** | **Food Safety & Standards (Labelling & Display) Regulations, 2020** | Live interactive 9-point packaging checklist validation + interactive bilingual front/back pouch mockup renderer. |
| **MoFPI** | **PMFME Scheme Documentation** | Exportable, official 1-page A4 **PMFME Packaging Readiness Certificate (PDF)** generated via ReportLab with zero multi-page spill guarantee. |

---

## 🌾 18 Seeded PMFME & ODOP Commodities

The system ships with pre-calibrated baseline chemical and physical data for 18 designated ODOP agricultural clusters across India:

1. **Foxnut / Makhana** (*Mithila & Katihar, Bihar*) — High moisture sensitivity, nitrogen flush required.
2. **Finger Millet / Ragi Flour** (*Mandya, Karnataka*) — Lipid hydrolysis and moisture caking prevention.
3. **Moringa Leaf Powder** (*Theni, Tamil Nadu*) — Photo-oxidation and chlorophyll degradation control.
4. **Turmeric Powder** (*Nizamabad, Telangana*) — Curcumin photolysis barrier.
5. **Mahua Dried Flowers** (*Bastar, Chhattisgarh*) — Hygroscopic sugar inversion control.
6. **Mango Pickle in Mustard Oil** (*Krishna, Andhra Pradesh / Varanasi, UP*) — High acidity ($\text{pH } 3.2$), pungent allylisothiocyanate barrier.
7. **Urad Dal Spiced Papad** (*Bikaner, Rajasthan*) — Moisture pickup leading to microbial spoilage.
8. **Solid Organic Jaggery** (*Muzaffarnagar, Uttar Pradesh*) — Deliquescence and non-enzymatic browning.
9. **Raw Forest Honey** (*Sundarbans, West Bengal*) — Hydroxymethylfurfural (HMF) kinetics and crystallization.
10. **Desi Cow Ghee** (*Saurashtra, Gujarat*) — Photo-induced lipid oxidation, rancidity prevention.
11. **Garam Masala Essential Oil Blend** (*Idukki, Kerala / Amritsar, Punjab*) — Volatile pinene/eugenol aroma scalping barrier.
12. **Sun-Dried Apricots** (*Kargil, Ladakh*) — Sulfur dioxide loss and enzymatic browning.
13. **Fresh White Button Mushrooms** (*Solan, Himachal Pradesh*) — High respiration ($450+\text{ mg CO}_2/\text{kg-hr}$), breathable anti-fog EMAP.
14. **Fresh Strawberries** (*Mahabaleshwar, Maharashtra*) — Botrytis cinerea suppression, equilibrium modified atmosphere.
15. **Fresh Malai Paneer** (*Karnal, Haryana / Ludhiana, Punjab*) — Anaerobic vacuum skin packaging, barrier to psychrotrophic microbes.
16. **Roasted Peanut Chikki** (*Lonavala, Maharashtra*) — Hexanal oxidative rancidity, critical moisture caking.
17. **Cured Tendu Leaves** (*Sambalpur, Odisha / Balaghat, MP*) — Forest micro-produce conditioning and mold prevention.
18. **Pearl Millet / Bajra Cookies** (*Barmer, Rajasthan*) — Unsaturated fat rancidity, crispness retention.

> **Dynamic Custom Mode:** Enterpreneurs can toggle to **Custom / Unlisted Commodity** mode to specify arbitrary crops (e.g., Red Dragonfruit, Murabba, Cold-Pressed Mustard Oil) and receive dynamic heuristic compliance mapping.

---

## 📁 Repository Structure

```
SIH-demo-sm2/
├── .gitignore                      # Python, Node, Environment, and OS exclusions
├── README.md                       # Comprehensive system architecture & documentation
├── run_demo.bat                    # Single-click unified system launcher for Windows
├── backend/
│   ├── data/
│   │   ├── commodities_seed.json   # 18 PMFME/ODOP seed commodities with physical & legal specs
│   │   └── translations.json       # Static bilingual dictionary (en, hi)
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── compliance.py           # FSSAI, BIS, CPCB-EPR, IS 9845 statutory rule engine
│   │   ├── model.joblib            # Trained Scikit-Learn DecisionTree classifier artifact
│   │   ├── pdf_generator.py        # ReportLab 1-page PMFME Packaging Readiness Certificate generator
│   │   ├── physics_engine.py       # Tetens vapor pressure, WVTR/OTR kinetics, laminate solver
│   │   ├── recommender.py          # Hybrid ML inference + barrier constraint scoring logic
│   │   └── train_model.py          # Synthetic dataset generator & Stratified 5-Fold model trainer
│   ├── main.py                     # FastAPI application endpoints & schema definitions
│   ├── requirements.txt            # Python production and testing dependencies
│   ├── stress_test.py              # Automated 6-scenario full-system adversarial stress runner
│   ├── test_api.py                 # Backend REST API integration test suite
│   └── test_physics.py             # Biophysical formulas and kinetics unit test suite
├── documents/
│   ├── extracted_build_spec.txt    # Extracted technical specifications from MoFPI
│   ├── info-form-bro.txt           # Problem statement context notes
│   └── SIH26236_Build_Spec.pdf     # Official SIH26236 Problem Statement Brief
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── LabelMockupPreview.jsx     # FSSAI 2020 SVG Pouch label preview
    │   │   ├── LaminateVisualizer.jsx     # 2.5D interactive multi-layer laminate stack visualizer
    │   │   ├── Screen1Input.jsx           # Commodity selector, custom mode & environmental sliders
    │   │   ├── Screen2Recommendation.jsx  # AI recommendation, advisory alert & barrier ratings
    │   │   ├── Screen3Compliance.jsx      # FSSAI, BIS, EPR & IS 9845 compliance studio
    │   │   ├── Screen4ReadinessSheet.jsx  # PMFME 1-page certificate view & PDF downloader
    │   │   ├── ShelfLifeSimulator.jsx     # Biophysical Arrhenius & RH quality decay SVG simulator
    │   │   └── SimulantProtocolCard.jsx   # IS 9845 food simulant test card component
    │   ├── context/
    │   │   └── LanguageContext.jsx        # Bilingual (English & Hindi) state provider
    │   ├── hooks/
    │   │   └── useVoiceInput.js           # Web Speech API speech-to-text hook
    │   ├── App.jsx                        # 4-stage navigation workflow coordinator
    │   ├── index.css                      # Tailwind styling & print media rules
    │   └── main.jsx                       # React 18 DOM root entrypoint
    ├── index.html                         # HTML5 template with Devanagari typography
    ├── package.json                       # NPM dependencies and scripts
    ├── package-lock.json                  # Deterministic dependency lockfile
    ├── postcss.config.js                  # PostCSS plugin configurations
    ├── tailwind.config.js                 # Custom color palettes & typography tokens
    └── vite.config.js                     # Vite build configuration with proxy to FastAPI
```

---

## ⚡ Quick Start & Installation

### Option 1: Single-Click Launcher (Windows)
Double-click `run_demo.bat` in the repository root. This automated batch script will:
1. Verify Python 3.10+ and Node.js 18+ installations.
2. Verify or train the AI model artifact (`backend/engine/model.joblib`).
3. Check and install frontend NPM packages.
4. Launch the FastAPI backend on `http://127.0.0.1:8000`.
5. Launch the Vite frontend on `http://localhost:5173`.
6. Open your default web browser directly to the dashboard.

### Option 2: Manual Setup

#### Step 1: Clone Repository
```bash
git clone https://github.com/UNSTOPBIL/SIH-demo-sm2.git
cd SIH-demo-sm2
```

#### Step 2: Setup Python Backend
```bash
# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# (Optional) Retrain Scikit-Learn DecisionTree model
python backend/engine/train_model.py

# Launch FastAPI Server
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
Interactive Swagger API documentation will be available at: `http://127.0.0.1:8000/docs`

#### Step 3: Setup Vite Frontend
Open a separate terminal window:
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in any modern web browser.

---

## 🧪 Comprehensive Verification & Stress Testing

Run the automated test runner to verify system behavior against hostile and out-of-distribution environments:

```bash
# 1. Biophysical and Arrhenius Kinetics Unit Tests
python backend/test_physics.py

# 2. REST API Integration Test Suite
python backend/test_api.py

# 3. Full-System Adversarial Stress Test Suite
python backend/stress_test.py
```

### Stress Test Matrix Results:
- **Hyper-Tropical Climate Stress ($48^\circ\text{C}$, $98\%\ \text{RH}$, $730\text{ days}$):** Validated finite target $\text{WVTR} = 0.09\text{ g/m}^2/\text{day}$ and automatic selection of Aluminium-foil triplex laminate with `CRITICAL_BARRIER_WARNING`.
- **Inverted / Equal Moisture Boundary ($M_0 \ge M_c$):** Mathematical division-by-zero avoided via algorithmic $\Delta M$ and $\Delta \text{RH}$ lower bounds; finite $\text{WVTR} = 17.87\text{ g/m}^2/\text{day}$.
- **Extreme Lipid Oxidation ($99.9\%\ \text{Fat}$ at $45^\circ\text{C}$):** Target $\text{OTR} = 0.84\text{ cc/m}^2/\text{day}$ clamped safely; tinplate canister selected.
- **Produce Respiration Edge Case ($35^\circ\text{C}$ ambient):** $Q_{10}$ rate exponent bounded; micro-perforated breathable film selected.
- **Unseeded Arbitrary Commodity:** Verified synthetic ID generation, FSSAI Schedule IV assignment, and IS 9845 Simulant B & D selection for acidic/fatty foods.
- **ReportLab 1-Page Constraint:** Guaranteed $100\%$ 1-page fit on A4 under $650+\ \text{character}$ field inputs, verified with PyMuPDF.

---

## ⚖️ Statutory & Legal Disclaimers

1. **MoFPI & PMFME Scheme:** This prototype has been developed strictly for educational and demonstration purposes for Smart India Hackathon (Problem ID: SIH26236).
2. **Statutory Standards:** References to FSSAI (Packaging Regulations 2018; Labelling and Display Regulations 2020), BIS (Bureau of Indian Standards), and CPCB (EPR Framework) are derived from publicly gazetted Government of India documents. Food business operators (FBOs) must perform physical migration testing at NABL-accredited laboratories prior to commercial retail distribution.

---
**Developed with ❤️ for Indian Food Micro-Enterprises, FPOs, and SHGs.**
