import React, { createContext, useContext, useState, useEffect } from 'react';

// Embedded fallback dictionary in case of network lag or initial load
const fallbackTranslations = {
  en: {
    app_title: "AI Food Packaging & Compliance Engine",
    app_subtitle: "Ministry of Food Processing Industries (MoFPI) · PMFME & ODOP Decision Support Platform",
    step1_nav: "1. Commodity & Specs",
    step2_nav: "2. Material Science",
    step3_nav: "3. India Regulatory Shield",
    step4_nav: "4. Readiness Sheet (PDF)",
    select_commodity: "Select PMFME / ODOP Commodity",
    select_placeholder: "-- Choose from 18 Seed Commodities --",
    voice_search_tooltip: "Click to speak in Hindi / English (e.g. 'Makhana' or 'मखाना')",
    listening: "Listening... Speak now",
    speech_unsupported: "Web Speech API not supported in this browser. Please use text select.",
    odop_cluster: "PMFME / ODOP Cluster",
    category: "Food Category",
    customize_parameters: "Adjust Commodity Properties (Pre-filled from ODOP standards)",
    moisture_label: "Moisture Content",
    fat_label: "Oil / Fat Content",
    ph_label: "Acidity / pH Level",
    shelf_life_label: "Target Shelf Life",
    days: "days",
    storage_condition: "Storage & Logistics Condition",
    storage_ambient: "Ambient Storage (25°C - 35°C)",
    storage_chilled: "Chilled / Cold Chain (2°C - 8°C)",
    storage_frozen: "Frozen Storage (-18°C)",
    respiration_class: "Respiration Class (Kader's Band)",
    btn_get_recommendation: "Analyze Barrier Needs & Recommend Packaging",
    recommendation_title: "Packaging Material Recommendation",
    recommendation_subtitle: "Multi-criteria barrier optimization verified with Scikit-Learn Decision Model",
    primary_material_badge: "Primary Recommended Material",
    alt_material_badge: "Sustainable / Alternative Option",
    barrier_profile_title: "Barrier Performance Profile",
    moisture_barrier: "Moisture Vapor Barrier",
    oxygen_barrier: "Oxygen Barrier",
    strength_barrier: "Puncture & Seal Strength",
    rating_poor: "Low / Breathable",
    rating_moderate: "Moderate",
    rating_high: "High Barrier",
    rating_superior: "Ultra / Hermetic",
    rating_breathable: "Controlled Breathable",
    rating_vented: "Vented / Perforated",
    expert_toggle_on: "Hide Technical Science & Test Standards",
    expert_toggle_off: "Expand Technical Specifications & ASTM Standards",
    tech_specs_title: "Certified Laboratory Specifications",
    otr_label: "Oxygen Transmission Rate (OTR)",
    wvtr_label: "Water Vapor Transmission Rate (WVTR)",
    thickness_label: "Recommended Film Caliper / Thickness",
    map_label: "Modified Atmosphere Packaging (MAP)",
    why_title: "Scientific Rationale (Why This Material?)",
    btn_goto_compliance: "Review India Statutory Compliance (FSSAI & BIS)",
    compliance_title: "India Statutory Compliance & Standards Shield",
    compliance_subtitle: "Chained statutory clearance: FSSAI 2018 Regulations, BIS Mandatory Codes & CPCB-EPR Rules",
    fssai_card_title: "FSSAI Food Safety Regulations, 2018",
    fssai_sched_iv: "Schedule IV Categorization",
    fssai_sched_iii: "Schedule I / II / III Material Class",
    bis_card_title: "Bureau of Indian Standards (BIS)",
    bis_code_label: "Mandatory IS Standard",
    migration_card_title: "Overall Migration Limit (IS 9845)",
    migration_standard: "Tested as per IS 9845 with specified food simulants (Distilled water, 3% Acetic acid, 10% Ethanol, n-Heptane/Iso-octane)",
    epr_card_title: "CPCB Extended Producer Responsibility (EPR)",
    epr_mandate: "Registration on CPCB Central Portal mandatory for Plastic Packaging Brand Owners & Processors",
    epr_category_label: "Plastic Waste Category",
    labelling_title: "FSSAI (Labelling and Display) Regulations, 2020 Checklist",
    labelling_subtitle: "Mandatory packaging declarations verified for retail distribution",
    label_fssai_logo: "FSSAI Logo with 14-Digit Food Business Operator (FBO) License Number",
    label_veg_mark: "Vegetarian / Non-Vegetarian Distinctive Green/Brown Square-Dot Symbol",
    label_net_quantity: "Net Quantity and Unit Sale Price (Legal Metrology Act, 2009)",
    label_mrp: "Maximum Retail Price (MRP inclusive of all taxes)",
    label_batch_no: "Batch / Lot Identification Code for Traceability",
    label_dates: "Date of Manufacture / Packing and 'Best Before' / Expiry Date",
    label_ingredients: "Ingredients List in Descending Order of Weight + Allergen Declarations",
    label_nutrition: "Nutritional Information per 100g / per serve (Calories, Protein, Carb, Sugars, Fat)",
    label_consumer_care: "Consumer Care Helpline Name, Address, Phone and Email",
    nabl_title: "NABL Accredited Testing Protocol Advisory",
    nabl_body: "Under FSSAI guidelines, food-contact packaging material must possess a Certificate of Conformity from an ISO/IEC 17025 accredited (NABL) testing laboratory prior to commercial rollout.",
    btn_goto_sheet: "Generate Official Readiness Sheet (PDF)",
    readiness_title: "Packaging & Compliance Readiness Sheet",
    readiness_subtitle: "Official decision document for PMFME micro-processors, FPOs, suppliers, and district officers",
    download_pdf_btn: "Download Official PDF (Server ReportLab)",
    print_sheet_btn: "Print / Save PDF (Browser Print)",
    back_edit_btn: "Modify Input Parameters",
    disclaimer_text: "Statutory Disclaimer: This system acts as an AI decision-support platform under MoFPI guidelines. Final commercial batches must be validated with an accredited NABL laboratory and comply with FSSAI regulations.",
    pmfme_scheme_tag: "PMFME Scheme / MoFPI Supported",
    created_at_label: "Generated Date & Time",
    odop_cluster_label: "ODOP Cluster Location"
  },
  hi: {
    app_title: "एआई खाद्य पैकेजिंग एवं अनुपालन इंजन",
    app_subtitle: "खाद्य प्रसंस्करण उद्योग मंत्रालय (MoFPI) · पीएमएफएमई और ओडीओपी निर्णय समर्थन प्रणाली",
    step1_nav: "1. उत्पाद एवं गुण",
    step2_nav: "2. पैकेजिंग विज्ञान",
    step3_nav: "3. भारतीय वैधानिक अनुपालन",
    step4_nav: "4. अनुपालन पत्र (PDF)",
    select_commodity: "पीएमएफएमई / ओडीओपी उत्पाद चुनें",
    select_placeholder: "-- 18 प्रमाणित उत्पादों में से चुनें --",
    voice_search_tooltip: "हिंदी या अंग्रेजी में बोलने के लिए क्लिक करें (उदा. 'मखाना' या 'रागी')",
    listening: "सुन रहा हूँ... अब बोलें",
    speech_unsupported: "इस ब्राउज़र में वॉइस इनपुट समर्थित नहीं है। कृपया ड्रॉपडाउन से चुनें।",
    odop_cluster: "ओडीओपी / पीएमएफएमई क्लस्टर",
    category: "खाद्य श्रेणी",
    customize_parameters: "उत्पाद के गुण समायोजित करें (ओडीओपी मानकों से पूर्व-भरे)",
    moisture_label: "नमी की मात्रा (Moisture %)",
    fat_label: "तेल / वसा की मात्रा (Fat %)",
    ph_label: "अम्लता / पीएच स्तर (pH)",
    shelf_life_label: "अपेक्षित शेल्फ लाइफ (दिन)",
    days: "दिन",
    storage_condition: "भंडारण एवं परिवहन स्थिति",
    storage_ambient: "सामान्य तापमान (25°C - 35°C)",
    storage_chilled: "शीत भंडारण / कोल्ड चेन (2°C - 8°C)",
    storage_frozen: "डीप फ्रीजर (-18°C)",
    respiration_class: "श्वसन दर श्रेणी (कादर बैंड्स)",
    btn_get_recommendation: "पैकेजिंग सामग्री एवं अवरोधक की सिफारिश देखें",
    recommendation_title: "अनुशंसित पैकेजिंग सामग्री एवं विनिर्देश",
    recommendation_subtitle: "मल्टी-क्राइटेरिया बैरियर ऑप्टिमाइज़ेशन एवं साइकिट-लर्न डिसीजन मॉडल द्वारा सत्यापित",
    primary_material_badge: "प्राथमिक अनुशंसित सामग्री",
    alt_material_badge: "पर्यावरण-अनुकूल / वैकल्पिक सामग्री",
    barrier_profile_title: "बैरियर सुरक्षा प्रोफ़ाइल",
    moisture_barrier: "नमी अवरोधक (Moisture Barrier)",
    oxygen_barrier: "ऑक्सीजन अवरोधक (Oxygen Barrier)",
    strength_barrier: "पंचर एवं सील मजबूती",
    rating_poor: "कम / हवादार",
    rating_moderate: "मध्यम",
    rating_high: "उच्च अवरोधक",
    rating_superior: "अल्ट्रा / पूर्ण सीलबंद",
    rating_breathable: "नियंत्रित सांस लेने योग्य",
    rating_vented: "छिद्रयुक्त (Vented)",
    expert_toggle_on: "तकनीकी विज्ञान और परीक्षण मानक छुपाएं",
    expert_toggle_off: "विस्तृत तकनीकी विनिर्देश एवं ASTM मानक देखें",
    tech_specs_title: "प्रमाणित प्रयोगशाला विनिर्देश",
    otr_label: "ऑक्सीजन संचरण दर (OTR)",
    wvtr_label: "जल वाष्प संचरण दर (WVTR)",
    thickness_label: "अनुशंसित फिल्म मोटाई",
    map_label: "संशोधित वातावरण पैकेजिंग (MAP)",
    why_title: "वैज्ञानिक कारण (यह सामग्री क्यों?)",
    btn_goto_compliance: "भारतीय वैधानिक अनुपालन (FSSAI एवं BIS) देखें",
    compliance_title: "भारतीय वैधानिक अनुपालन एवं मानक सुरक्षा कवच",
    compliance_subtitle: "शृंखलाबद्ध मंजूरी: FSSAI 2018 नियम, BIS अनिवार्य कोड एवं CPCB-EPR नियम",
    fssai_card_title: "एफएसएसएआई (FSSAI) पैकेजिंग विनियम, 2018",
    fssai_sched_iv: "अनुसूची IV (खाद्य श्रेणी वर्गीकरण)",
    fssai_sched_iii: "अनुसूची I / II / III (सामग्री वर्ग)",
    bis_card_title: "भारतीय मानक ब्यूरो (BIS)",
    bis_code_label: "अनिवार्य आईएस (IS) कोड",
    migration_card_title: "समग्र प्रवासन सीमा (IS 9845 Migration Limit)",
    migration_standard: "खाद्य सिमुलेटरों (आसुत जल, 3% एसिटिक एसिड, एन-हेप्टेन) के साथ IS 9845 अनुसार परीक्षण",
    epr_card_title: "सीपीसीबी विस्तारित उत्पादक उत्तरदायित्व (CPCB-EPR)",
    epr_mandate: "प्लास्टिक पैकेजिंग ब्रांड मालिकों के लिए CPCB पोर्टल पर पंजीकरण कानूनी रूप से अनिवार्य है",
    epr_category_label: "प्लास्टिक अपशिष्ट श्रेणी",
    labelling_title: "एफएसएसएआई (लेबलिंग एवं प्रदर्शन) विनियम, 2020 चेकलिस्ट",
    labelling_subtitle: "खुदरा बिक्री हेतु अनिवार्य पैकेजिंग घोषणाएं",
    label_fssai_logo: "FSSAI लोगो एवं 14-अंकों का खाद्य व्यवसाय लाइसेंस नंबर",
    label_veg_mark: "शाकाहारी / मांसाहारी विशिष्ट हरा / भूरा प्रतीक चिन्ह",
    label_net_quantity: "शुद्ध मात्रा एवं इकाई विक्रय मूल्य (विधिक मापविज्ञान अधिनियम, 2009)",
    label_mrp: "अधिकतम खुदरा मूल्य (सभी करों सहित MRP)",
    label_batch_no: "ट्रेसेबिलिटी हेतु बैच / लॉट पहचान संख्या",
    label_dates: "निर्माण / पैकिंग तिथि एवं 'उपयोग की अंतिम तिथि' (Best Before / Expiry)",
    label_ingredients: "वजन के घटते क्रम में सामग्री सूची एवं एलर्जिन चेतावनी",
    label_nutrition: "प्रति 100 ग्राम / सर्व पोषण संबंधी जानकारी (ऊर्जा, प्रोटीन, कार्ब, वसा)",
    label_consumer_care: "उपभोक्ता सहायता हेल्पलाइन नाम, पता, फोन और ईमेल",
    nabl_title: "एनएबीएल (NABL) मान्यता प्राप्त लैब परीक्षण सलाह",
    nabl_body: "FSSAI के नियमों के तहत, व्यावसायिक पैकेजिंग से पहले सामग्री का NABL मान्यता प्राप्त लैब से अनुरूपता प्रमाण पत्र प्राप्त करना आवश्यक है।",
    btn_goto_sheet: "आधिकारिक पैकेजिंग अनुपालन पत्रक (PDF) बनाएं",
    readiness_title: "पैकेजिंग एवं वैधानिक अनुपालन तत्परता पत्र",
    readiness_subtitle: "पीएमएफएमई सूक्ष्म उद्यमियों, एफपीओ, आपूर्तिकर्ताओं और बैंक अधिकारियों हेतु आधिकारिक दस्तावेज",
    download_pdf_btn: "आधिकारिक पीडीएफ डाउनलोड करें (ReportLab)",
    print_sheet_btn: "प्रिंट करें / पीडीएफ सेव करें (ब्राउज़र प्रिंट)",
    back_edit_btn: "पैरामीटर में बदलाव करें",
    disclaimer_text: "वैधानिक अस्वीकरण: यह प्रणाली MoFPI दिशानिर्देशों के तहत निर्णय समर्थन उपकरण के रूप में कार्य करती है। अंतिम व्यावसायिक बैच NABL मान्यता प्राप्त लैब से परीक्षणोपरांत ही जारी करें।",
    pmfme_scheme_tag: "पीएमएफएमई योजना / खाद्य प्रसंस्करण उद्योग मंत्रालय",
    created_at_label: "निर्मित दिनांक एवं समय",
    odop_cluster_label: "ओडीओपी क्लस्टर स्थान"
  }
};

const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState('en');
  const [dict, setDict] = useState(fallbackTranslations);

  useEffect(() => {
    fetch('/api/translations')
      .then(res => res.json())
      .then(data => {
        if (data && data.en && data.hi) {
          setDict(data);
        }
      })
      .catch(() => {
        // Fallback already populated
      });
  }, []);

  const t = (key) => {
    if (dict[language] && dict[language][key]) {
      return dict[language][key];
    }
    if (dict.en && dict.en[key]) {
      return dict.en[key];
    }
    return key;
  };

  const toggleLanguage = () => {
    setLanguage(prev => (prev === 'en' ? 'hi' : 'en'));
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, toggleLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
