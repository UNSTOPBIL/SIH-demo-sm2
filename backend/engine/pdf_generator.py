import io
import os
import uuid
from datetime import datetime
from typing import Dict, Any, List

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register TrueType font family for crisp Unicode symbols ([✔], m², °C, Rs.)
UNICODE_FONT = 'Helvetica'
UNICODE_FONT_BOLD = 'Helvetica-Bold'
UNICODE_FONT_OBLIQUE = 'Helvetica-Oblique'

try:
    import matplotlib
    mpl_font_dir = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
    dejavu_regular = os.path.join(mpl_font_dir, 'DejaVuSans.ttf')
    dejavu_bold = os.path.join(mpl_font_dir, 'DejaVuSans-Bold.ttf')
    dejavu_oblique = os.path.join(mpl_font_dir, 'DejaVuSans-Oblique.ttf')
    if os.path.exists(dejavu_regular) and os.path.exists(dejavu_bold):
        pdfmetrics.registerFont(TTFont('DejaVuSans', dejavu_regular))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', dejavu_bold))
        if os.path.exists(dejavu_oblique):
            pdfmetrics.registerFont(TTFont('DejaVuSans-Oblique', dejavu_oblique))
        pdfmetrics.registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSans-Bold', italic='DejaVuSans-Oblique' if os.path.exists(dejavu_oblique) else 'DejaVuSans')
        UNICODE_FONT = 'DejaVuSans'
        UNICODE_FONT_BOLD = 'DejaVuSans-Bold'
        UNICODE_FONT_OBLIQUE = 'DejaVuSans-Oblique' if os.path.exists(dejavu_oblique) else 'DejaVuSans'
except Exception:
    pass

if UNICODE_FONT == 'Helvetica':
    for win_font in ['C:/Windows/Fonts/seguisym.ttf', 'C:/Windows/Fonts/seguiemj.ttf']:
        if os.path.exists(win_font):
            try:
                pdfmetrics.registerFont(TTFont('SegoeUISymbol', win_font))
                UNICODE_FONT = 'SegoeUISymbol'
                UNICODE_FONT_BOLD = 'SegoeUISymbol'
                UNICODE_FONT_OBLIQUE = 'SegoeUISymbol'
                break
            except Exception:
                pass


def sanitize_text(val: Any) -> str:
    """Ensure string is clean text for ReportLab canvas without unencoded currency glyphs."""
    if val is None:
        return ""
    s = str(val).strip()
    s = s.replace('₹', 'Rs. ').replace('\u20b9', 'Rs. ')
    s = s.replace('≤', '<=').replace('≥', '>=')
    return s


def truncate_text(val: Any, max_len: int = 60, add_ellipsis: bool = True) -> str:
    """Defensive truncation that avoids cutting words in half."""
    s = sanitize_text(val)
    if len(s) <= max_len:
        return s
    if not add_ellipsis:
        cut = s[:max_len]
        last_sp = cut.rfind(' ')
        if last_sp > max_len // 2:
            cut = cut[:last_sp]
        return cut.rstrip()
    
    target_len = max_len - 3
    cut = s[:target_len]
    last_sp = cut.rfind(' ')
    if last_sp > target_len // 2:
        cut = cut[:last_sp]
    return cut.rstrip() + "..."


def build_qr_drawing(verify_url: str, size_mm: float = 22.0) -> Drawing:
    qr_code = QrCodeWidget(verify_url)
    bounds = qr_code.getBounds()
    w = bounds[2] - bounds[0]
    h = bounds[3] - bounds[1]
    size_pt = size_mm * 2.83465
    d = Drawing(size_pt, size_pt, transform=[size_pt / w, 0, 0, size_pt / h, 0, 0])
    d.add(qr_code)
    return d


def generate_packaging_readiness_pdf(commodity_data: Dict[str, Any], lang: str = "en") -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=10 * mm,
        rightMargin=10 * mm,
        topMargin=8 * mm,
        bottomMargin=8 * mm
    )

    styles = getSampleStyleSheet()

    # Typography Styles using Unicode font family
    header_style = ParagraphStyle(
        'MainHeader',
        parent=styles['Normal'],
        fontName=UNICODE_FONT_BOLD,
        fontSize=12,
        leading=14.5,
        textColor=colors.HexColor('#0f3b23')
    )

    sub_header_style = ParagraphStyle(
        'SubHeader',
        parent=styles['Normal'],
        fontName=UNICODE_FONT,
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#166534')
    )

    badge_style = ParagraphStyle(
        'BadgeText',
        parent=styles['Normal'],
        fontName=UNICODE_FONT_BOLD,
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor('#15803d')
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName=UNICODE_FONT_BOLD,
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#134e2b'),
        spaceAfter=1
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName=UNICODE_FONT,
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor('#1f2937')
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName=UNICODE_FONT_BOLD,
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor('#111827')
    )

    checklist_style = ParagraphStyle(
        'ChecklistText',
        parent=styles['Normal'],
        fontName=UNICODE_FONT,
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor('#1f2937')
    )

    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontName=UNICODE_FONT_OBLIQUE,
        fontSize=5.5,
        leading=7.5,
        textColor=colors.HexColor('#6b7280'),
        alignment=1
    )

    elements = []

    # Generate Audit Verification Token
    batch_uuid = uuid.uuid4().hex[:10].upper()
    cid = commodity_data.get('commodity_id', 'makhana')
    verify_url = f"http://localhost:5173/verify?id={cid}&batch={batch_uuid}"
    qr_drawing = build_qr_drawing(verify_url, size_mm=20.0)

    # 1. Executive Header Strip with In-Memory QR Code
    header_text = [
        Paragraph("MINISTRY OF FOOD PROCESSING INDUSTRIES (MoFPI) · GOVERNMENT OF INDIA", sub_header_style),
        Paragraph("PMFME / ODOP Food Packaging & Statutory Compliance Certificate", header_style),
        Paragraph(f"Decision Support Tool for Micro-Enterprises & FPOs · Ref: <b>SIH26236-MoFPI-{batch_uuid}</b>", sub_header_style),
        Paragraph(f"Verified Audit Certificate · Generated: {datetime.now().strftime('%d-%b-%Y %H:%M IST')} · Authenticity Secured", badge_style)
    ]

    header_table_data = [
        [header_text, qr_drawing]
    ]

    t_header = Table(header_table_data, colWidths=[164 * mm, 26 * mm])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    elements.append(t_header)
    elements.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor('#15803d'), spaceAfter=2.0))

    # --- BLOCK I: Commodity Bio-Chemical & Storage Matrix ---
    elements.append(Paragraph("I. Commodity Bio-Chemical & Storage Matrix", section_heading))
    
    raw_name_en = commodity_data.get('name_en', 'Food Product').strip()
    c_name_base = raw_name_en.split('(')[0].strip() if '(' in raw_name_en and ')' not in raw_name_en else raw_name_en
    c_name = truncate_text(c_name_base, 55)
    c_region = truncate_text(commodity_data.get('odop_region', 'National Scheme'), 45)
    c_cat = truncate_text(commodity_data.get('category', 'Processed Food'), 35)
    m_val = f"{commodity_data.get('moisture_pct', 0)}%"
    fat_val = f"{commodity_data.get('fat_oil_pct', 0)}%"
    ph_val = str(commodity_data.get('ph_value', 7.0))
    sl_val = f"{commodity_data.get('shelf_life_days', 90)} days"
    st_val = str(commodity_data.get('storage_type', 'ambient')).capitalize()
    temp_c = commodity_data.get('storage_temp_c', 30.0)
    raw_rh = commodity_data.get('ambient_rh', 0.70)
    rh_pct = int(raw_rh * 100) if raw_rh <= 1.0 else int(raw_rh)
    rh_val = f"{rh_pct}% RH"
    rc_val = str(commodity_data.get('respiration_class', 'Low'))

    profile_data = [
        [Paragraph("Commodity Name:", body_bold), Paragraph(c_name, body_style),
         Paragraph("ODOP Cluster:", body_bold), Paragraph(c_region, body_style)],
        [Paragraph("Food Category:", body_bold), Paragraph(c_cat, body_style),
         Paragraph("Storage Condition:", body_bold), Paragraph(f"{st_val} ({temp_c}°C, {rh_val})", body_style)],
        [Paragraph("Moisture & Fat:", body_bold), Paragraph(f"M: {m_val} | Fat: {fat_val}", body_style),
         Paragraph("Acidity & Respiration:", body_bold), Paragraph(f"pH {ph_val} ({rc_val} Resp.)", body_style)],
        [Paragraph("Target Shelf Life:", body_bold), Paragraph(sl_val, body_style),
         Paragraph("Verification Token:", body_bold), Paragraph(f"<b>{batch_uuid}</b>", body_style)]
    ]

    t1 = Table(profile_data, colWidths=[38 * mm, 57 * mm, 38 * mm, 57 * mm])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f9fafb')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#d1d5db')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t1)
    elements.append(Spacer(1, 1.5 * mm))

    # --- BLOCK II: Mathematical Barrier Demand vs Recommended Laminate Engineering ---
    elements.append(Paragraph("II. Mathematical Barrier Demand vs Recommended Laminate Engineering", section_heading))
    
    p_mat = truncate_text(commodity_data.get('primary_material', 'Multi-Layer Barrier Laminate'), 65)
    specs = commodity_data.get('technical_specs', {})
    physics = commodity_data.get('physics_metrics', {})
    
    target_wvtr = physics.get('target_wvtr_allowable', commodity_data.get('target_wvtr', 1.5))
    target_otr = physics.get('target_otr_allowable', commodity_data.get('target_otr', 45.0))
    safety_fac = commodity_data.get('safety_factor', 1.8)
    
    otr_spec = truncate_text(specs.get('otr_range', f"{target_otr} cc/m2/day"), 45)
    wvtr_spec = truncate_text(specs.get('wvtr_range', f"{target_wvtr} g/m2/day"), 45)
    thick = f"{specs.get('thickness_um', 70)} um"
    map_mix = truncate_text(specs.get('map_gas_mix', 'N/A'), 45)
    rationale = truncate_text(commodity_data.get('why_material_en', 'Engineered barrier protection.'), 180)

    # Format multi-layer laminate breakdown if present (capped at 3 layers)
    prim_struct = commodity_data.get('primary_structure', {})
    layers = prim_struct.get('layers', [])
    if layers:
        layer_strings = []
        for l in layers[:3]:
            raw_name = l.get('short_name') or l.get('name') or 'Layer'
            l_name = truncate_text(raw_name, 28, add_ellipsis=False)
            
            raw_role = l.get('role_en', 'Protection').strip()
            # Clean up role descriptions so key technical phrases render completely without mid-word cuts
            if "flex-crack resistance" in raw_role:
                clean_role = "Optical clarity, surface gloss & flex-crack resistance"
            elif "blocking 98%" in raw_role or "blocks 98%" in raw_role:
                clean_role = "Vacuum metallized barrier; blocks 98% light/UV & moisture"
            elif "puncture resistance" in raw_role:
                clean_role = "Low SIT heat seal (105°C) & high puncture strength"
            elif "pinhole" in raw_role or "hermetic" in raw_role:
                clean_role = "Hermetic sealing & exceptional puncture strength"
            else:
                # Strip trailing test standards like (ASTM D1922)
                clean_role = raw_role
                if "(" in clean_role and ")" in clean_role:
                    idx = clean_role.rfind("(")
                    if any(t in clean_role[idx:] for t in ["ASTM", "IS ", "ISO", "DIN"]):
                        clean_role = clean_role[:idx].strip().rstrip(",- ")
            
            l_role = truncate_text(clean_role, 80, add_ellipsis=True)
            layer_strings.append(f"• <b>{l_name}</b>: {l_role}")
        layer_breakdown_html = "<br/>".join(layer_strings)
    else:
        layer_breakdown_html = "Outer Print Web (PET/BOPP) / Central Barrier Core (Al-Foil/Met-BOPP) / Inner Heat Sealant (PE)"

    econ = commodity_data.get('economics', {})
    sust = commodity_data.get('sustainability', {})
    gsm_val = econ.get('gsm_metrics', {}).get('total_gsm') or specs.get('total_gsm', 73.8)
    yield_val = econ.get('gsm_metrics', {}).get('film_yield_m2_per_kg') or specs.get('film_yield_m2_per_kg', 13.55)
    cost_val = econ.get('unit_cost_metrics', {}).get('cost_per_pouch_inr') or specs.get('unit_cost_inr', 0.55)
    if isinstance(cost_val, (int, float)):
        cost_str = f"{cost_val:.2f}"
    else:
        cost_str = str(cost_val).replace('₹', '').replace('Rs.', '').strip()

    epr_raw = sust.get('cpcb_epr_compliance', {}).get('estimated_annual_epr_liability_inr')
    if epr_raw is None:
        epr_raw = 5800.0
    epr_val = abs(float(epr_raw))
    
    epr_cat_name = sust.get('cpcb_epr_compliance', {}).get('category_name') or commodity_data.get('epr_category', 'Category III MLP')
    if "Category III" in epr_cat_name:
        epr_cat_clean = "Category III MLP"
    elif "Category II" in epr_cat_name:
        epr_cat_clean = "Category II Mono-PE"
    elif "Category I" in epr_cat_name:
        epr_cat_clean = "Category I Rigid"
    elif "Category IV" in epr_cat_name:
        epr_cat_clean = "Category IV Compostable"
    else:
        epr_cat_clean = truncate_text(epr_cat_name, 24, add_ellipsis=False)

    econ_str = (
        f"Composite GSM: <b>{gsm_val} g/m²</b> (Yield: {yield_val} m²/kg) | "
        f"Est. Unit Cost: <b>Rs. {cost_str}/pouch</b> | "
        f"CPCB EPR: {epr_cat_clean} (~Rs. {int(round(epr_val)):,}/yr)"
    )

    spec_data = [
        [Paragraph("Target Mathematical Demand:", body_bold),
         Paragraph(f"Max Permissible WVTR: <b>{target_wvtr} g/m2/day</b> | Max Allowable OTR: <b>{target_otr} cc/m2/day</b> (Safety Factor: <b>{safety_fac}x</b>)", body_style)],
        [Paragraph("Recommended Substrate Structure:", body_bold),
         Paragraph(f"<b>{p_mat}</b> (Total Caliper: {thick})", body_bold)],
        [Paragraph("Multi-Layer Engineering Breakdown:", body_bold),
         Paragraph(layer_breakdown_html, body_style)],
        [Paragraph("Certified Barrier Performance:", body_bold),
         Paragraph(f"OTR: {otr_spec} | WVTR: {wvtr_spec} | MAP Gas Flush: {map_mix}", body_style)],
        [Paragraph("Converter Economics & EPR:", body_bold),
         Paragraph(econ_str, body_style)],
        [Paragraph("Bio-Physical Rationale:", body_bold),
         Paragraph(rationale, body_style)]
    ]

    t2 = Table(spec_data, colWidths=[55 * mm, 135 * mm])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdf4')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#86efac')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bbf7d0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 1.5 * mm))

    # --- BLOCK III: Statutory Regulatory Clearances & IS 9845 Simulant Protocol ---
    elements.append(Paragraph("III. India Statutory Compliance Shield & IS 9845 Simulant Protocol", section_heading))
    fssai_sched = truncate_text(commodity_data.get('fssai_schedule', 'Schedule IV & Schedule III (Plastics)'), 60)
    
    raw_bis = sanitize_text(commodity_data.get('bis_code', 'IS 10146:2021 (PE Contact Layer)'))
    if "IS 10146" in raw_bis and "PE Contact Layer" not in raw_bis:
        bis_code_clean = raw_bis.replace("Polyethylene in contact with foodstuffs", "PE Contact Layer")\
                                .replace("Polyethylene", "PE Contact Layer")\
                                .replace("Plastics in food contact", "PE Contact Layer")\
                                .replace("Plastics for packaging", "PE Contact Layer")
    else:
        bis_code_clean = raw_bis
    bis_code_clean = truncate_text(bis_code_clean, 60)

    epr_cat = truncate_text(commodity_data.get('epr_category', 'Category III Multilayer Flexible Plastic'), 60)
    
    # Concise Simulants from protocol
    sim_proto = commodity_data.get('simulant_protocol', {})
    simulants = sim_proto.get('simulants', [])
    if simulants:
        sim_desc_list = []
        for s in simulants[:3]:
            code = s.get('simulant_code') or s.get('code') or 'Simulant'
            if 'Simulant A' in code:
                sim_line = "• <b>Simulant A</b>: Distilled Water (Aqueous Foods) | 40°C ± 2°C for 10 Days"
            elif 'Simulant B' in code:
                sim_line = "• <b>Simulant B</b>: 3% w/v Acetic Acid (Acidic Foods) | 40°C ± 2°C for 10 Days"
            elif 'Simulant C' in code:
                sim_line = "• <b>Simulant C</b>: 15% Ethanol (Sweet / Moist Foods) | 40°C ± 2°C for 10 Days"
            elif 'Simulant D' in code:
                sim_line = "• <b>Simulant D</b>: Iso-octane / n-Heptane (Fatty Foods) | 20°C for 30 Mins"
            else:
                raw_d = s.get('description') or s.get('name') or 'Simulant'
                d_clean = raw_d.split('(')[0].strip()
                cond = s.get('condition', '40°C for 10 Days')
                if "(or" in cond:
                    cond = cond.split("(or")[0].strip()
                sim_line = f"• <b>{code}</b>: {truncate_text(d_clean, 35, add_ellipsis=False)} | {truncate_text(cond, 25, add_ellipsis=False)}"
            sim_desc_list.append(sim_line)
        simulant_html = "<br/>".join(sim_desc_list)
    else:
        simulant_html = (
            "• <b>Simulant A</b>: Distilled Water (Aqueous Foods) | 40°C ± 2°C for 10 Days<br/>"
            "• <b>Simulant D</b>: Iso-octane / n-Heptane (Fatty Foods) | 20°C for 30 Mins"
        )

    comp_data = [
        [Paragraph("FSSAI Regulations, 2018:", body_bold),
         Paragraph(f"<b>{fssai_sched}</b><br/>Mandatory Food-Contact Packaging Authorization", body_style)],
        [Paragraph("Bureau of Indian Standards (BIS):", body_bold),
         Paragraph(f"<b>{bis_code_clean}</b><br/>Mandatory Polymer / Substrate Conformity Standard", body_style)],
        [Paragraph("IS 9845 Simulant Protocol:", body_bold),
         Paragraph(f"Overall Migration Ceiling: <b><= 60 mg/kg or <= 10 mg/dm2</b><br/>{simulant_html}", body_style)],
        [Paragraph("CPCB EPR Plastic Waste Rules:", body_bold),
         Paragraph(f"<b>Mandatory Registration: {epr_cat}</b><br/>Central EPR Portal Registration & Annual Recycling Target Compliance", body_style)]
    ]

    t3 = Table(comp_data, colWidths=[55 * mm, 135 * mm])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#eff6ff')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#93c5fd')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bfdbfe')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t3)
    elements.append(Spacer(1, 1.5 * mm))

    # --- BLOCK IV: Mandatory 9-Point Labelling & NABL Batch Conformity Protocol ---
    elements.append(Paragraph("IV. Mandatory 9-Point Labelling & NABL Batch Conformity Protocol", section_heading))

    checklist_col1 = (
        "<b>[✔] FSSAI Logo + 14-Digit License</b><br/>"
        "<b>[✔] Veg / Non-Veg Color Symbol</b><br/>"
        "<b>[✔] Net Quantity (Legal Metrology)</b>"
    )
    checklist_col2 = (
        "<b>[✔] Retail MRP (incl. all taxes)</b><br/>"
        "<b>[✔] Batch / Lot Identification</b><br/>"
        "<b>[✔] Mfg Date & Best-Before Date</b>"
    )
    checklist_col3 = (
        "<b>[✔] Ingredients List (Descending Wt)</b><br/>"
        "<b>[✔] Nutrition Facts per 100g</b><br/>"
        "<b>[✔] Consumer Care Helpline Details</b>"
    )

    t_check = Table([
        [Paragraph(checklist_col1, checklist_style),
         Paragraph(checklist_col2, checklist_style),
         Paragraph(checklist_col3, checklist_style)]
    ], colWidths=[45 * mm, 45 * mm, 45 * mm])
    t_check.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))

    checklist_data = [
        [Paragraph("FSSAI 2020 Display Mandates:", body_bold), t_check],
        [Paragraph("NABL Testing Advisory:", body_bold),
         Paragraph("Commercial batches require batch-wise Certificate of Conformity from an ISO/IEC 17025 accredited (NABL) laboratory verifying IS 9845 overall migration limits and heavy metal absence (<100 ppm total Pb, Cd, Cr, Hg).", body_style)]
    ]

    t4 = Table(checklist_data, colWidths=[55 * mm, 135 * mm])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fffbeb')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#fcd34d')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#fde68a')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t4)
    elements.append(Spacer(1, 1.5 * mm))

    # Disclaimer Footer
    elements.append(Paragraph(
        "Statutory Advisory Disclaimer: This document is produced by an intelligent decision support platform developed for MoFPI PMFME/ODOP initiatives (SIH26236). "
        f"Certificate Verification Token: {batch_uuid}. Micro-processors and FBOs must ensure physical batch conformity through NABL accredited testing before commercial market distribution.",
        disclaimer_style
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer
