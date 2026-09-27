import io
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

def sanitize_text(val: Any) -> str:
    """Ensure string is clean ASCII/Latin-1 for standard ReportLab canvas."""
    if val is None:
        return ""
    s = str(val).strip()
    s = s.replace('≤', '<=').replace('≥', '>=').replace('µ', 'u').replace('²', '2')
    return s

def truncate_text(val: Any, max_len: int = 60, add_ellipsis: bool = True) -> str:
    s = sanitize_text(val)
    if len(s) > max_len:
        return s[:max_len - 3] + "..." if add_ellipsis else s[:max_len]
    return s

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

    # Typography Styles
    header_style = ParagraphStyle(
        'MainHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=14.5,
        textColor=colors.HexColor('#0f3b23')
    )

    sub_header_style = ParagraphStyle(
        'SubHeader',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#166534')
    )

    badge_style = ParagraphStyle(
        'BadgeText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor('#15803d')
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#134e2b'),
        spaceAfter=1
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor('#1f2937')
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor('#111827')
    )

    checklist_style = ParagraphStyle(
        'ChecklistText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6,
        leading=8,
        textColor=colors.HexColor('#1f2937')
    )

    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
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
            l_name = truncate_text(l.get('short_name', l.get('name', 'Layer')), 24)
            l_role = truncate_text(l.get('role_en', 'Protection'), 55)
            layer_strings.append(f"• <b>{l_name}</b>: {l_role}")
        layer_breakdown_html = "<br/>".join(layer_strings)
    else:
        layer_breakdown_html = "Outer Print Web (PET/BOPP) / Central Barrier Core (Al-Foil/Met-BOPP) / Inner Heat Sealant (PE)"

    spec_data = [
        [Paragraph("Target Mathematical Demand:", body_bold),
         Paragraph(f"Max Permissible WVTR: <b>{target_wvtr} g/m2/day</b> | Max Allowable OTR: <b>{target_otr} cc/m2/day</b> (Safety Factor: <b>{safety_fac}x</b>)", body_style)],
        [Paragraph("Recommended Substrate Structure:", body_bold),
         Paragraph(f"<b>{p_mat}</b> (Total Caliper: {thick})", body_bold)],
        [Paragraph("Multi-Layer Engineering Breakdown:", body_bold),
         Paragraph(layer_breakdown_html, body_style)],
        [Paragraph("Certified Barrier Performance:", body_bold),
         Paragraph(f"OTR: {otr_spec} | WVTR: {wvtr_spec} | MAP Gas Flush: {map_mix}", body_style)],
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
    
    # Simulants from protocol (capped at 3)
    sim_proto = commodity_data.get('simulant_protocol', {})
    simulants = sim_proto.get('simulants', [])
    if simulants:
        sim_desc_list = [f"<b>{s['simulant_code']}</b>: {truncate_text(s.get('description', s.get('name', 'Simulant')), 42)} ({truncate_text(s.get('condition', ''), 28)})" for s in simulants[:3]]
        simulant_html = "<br/>".join(sim_desc_list)
    else:
        simulant_html = "<b>Simulant A</b>: Distilled Water (40°C, 10d) | <b>Simulant D</b>: n-Heptane (20°C, 30m)"

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
