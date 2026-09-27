import React, { useState } from 'react';
import { Download, Printer, ArrowLeft, CheckCircle, FileCheck, Building, ShieldCheck, Sparkles, RefreshCw } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export const Screen4ReadinessSheet = ({ recommendation, complianceData, onBack }) => {
  const { language, t } = useLanguage();
  const [isExporting, setIsExporting] = useState(false);

  if (!recommendation || !complianceData) return null;

  const handleDownloadPdf = async () => {
    try {
      setIsExporting(true);
      // Combine recommendation & compliance data
      const payload = {
        ...recommendation,
        ...complianceData
      };

      const res = await fetch('/api/export-pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        throw new Error(`Export failed with status: ${res.status}`);
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `PMFME_Packaging_Compliance_${recommendation.commodity_id}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (e) {
      console.error("PDF export error:", e);
      alert("Server PDF export encountered an issue. Falling back to browser print...");
      window.print();
    } finally {
      setIsExporting(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  const now = new Date().toLocaleString('en-IN', {
    dateStyle: 'medium',
    timeStyle: 'short',
    timeZone: 'Asia/Kolkata'
  });

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Action Toolbar (Hidden during print) */}
      <div className="no-print bg-white rounded-2xl border border-slate-200 p-4 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
        <button
          type="button"
          onClick={onBack}
          className="w-full sm:w-auto px-4 py-2.5 rounded-xl border border-slate-300 text-slate-700 hover:bg-slate-50 font-semibold text-xs flex items-center justify-center gap-2 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>{t('back_edit_btn')}</span>
        </button>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          {/* Print / Save PDF Fallback */}
          <button
            type="button"
            onClick={handlePrint}
            className="flex-1 sm:flex-initial px-4 py-2.5 rounded-xl border border-slate-300 bg-slate-50 hover:bg-slate-100 text-slate-800 font-bold text-xs flex items-center justify-center gap-2 transition shadow-sm"
          >
            <Printer className="w-4 h-4 text-slate-600" />
            <span>{t('print_sheet_btn')}</span>
          </button>

          {/* Primary Download PDF */}
          <button
            type="button"
            onClick={handleDownloadPdf}
            disabled={isExporting}
            className="flex-1 sm:flex-initial bg-emerald-700 hover:bg-emerald-800 text-white font-bold py-2.5 px-5 rounded-xl shadow flex items-center justify-center gap-2 transition duration-200 text-xs"
          >
            {isExporting ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Generating Certificate...</span>
              </>
            ) : (
              <>
                <Download className="w-4 h-4" />
                <span>{t('download_pdf_btn')}</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* The Printable A4 Certificate Sheet */}
      <div className="print-page bg-white rounded-2xl border border-slate-300 p-8 shadow-md text-slate-900 space-y-6">
        {/* Certificate Header */}
        <div className="border-b-2 border-emerald-800 pb-4 text-center space-y-1">
          <div className="text-[11px] font-bold text-emerald-800 uppercase tracking-widest flex items-center justify-center gap-1.5">
            <Building className="w-3.5 h-3.5" />
            <span>MINISTRY OF FOOD PROCESSING INDUSTRIES (MoFPI) · GOVERNMENT OF INDIA</span>
          </div>
          <h1 className="text-xl md:text-2xl font-black text-slate-900 tracking-tight">
            PMFME / ODOP Food Packaging & Statutory Compliance Certificate
          </h1>
          <p className="text-xs text-slate-600">
            Intelligent Decision Support System for Micro Food Enterprises, FPOs & Packaging Technologists (SIH26236)
          </p>
          <div className="text-[11px] text-slate-500 pt-1">
            <span>{t('created_at_label')}: {now} IST · </span>
            <span className="font-semibold text-emerald-700">Cluster: {recommendation.odop_region}</span>
          </div>
        </div>

        {/* Section 1: Commodity Profile */}
        <div className="space-y-2">
          <h2 className="text-xs font-bold uppercase tracking-wider text-emerald-900 border-l-4 border-emerald-600 pl-2">
            1. Commodity & Formulation Profile
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 bg-slate-50 p-3 rounded-lg border border-slate-200 text-xs">
            <div>
              <span className="text-slate-500 block text-[10px]">Commodity Name:</span>
              <span className="font-bold text-slate-900">{recommendation.name_en}</span>
              <span className="text-slate-500 block text-[10px]">({recommendation.name_hi})</span>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px]">Food Category:</span>
              <span className="font-semibold text-slate-800">{recommendation.category}</span>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px]">Moisture & Fat:</span>
              <span className="font-semibold text-slate-800">M: {recommendation.moisture_pct}% | F: {recommendation.fat_oil_pct}%</span>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px]">Target Shelf Life:</span>
              <span className="font-semibold text-slate-800">{recommendation.shelf_life_days} Days ({recommendation.storage_type})</span>
            </div>
          </div>
        </div>

        {/* Section 2: Recommended Material & Lab Specs */}
        <div className="space-y-2">
          <h2 className="text-xs font-bold uppercase tracking-wider text-emerald-900 border-l-4 border-emerald-600 pl-2">
            2. Recommended Packaging Material & Technical Specifications
          </h2>
          <div className="bg-emerald-50/60 p-4 rounded-lg border border-emerald-200 space-y-3 text-xs">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <span className="text-[10px] font-bold text-emerald-900 uppercase block">Primary Recommended Structure:</span>
                <span className="text-sm font-black text-slate-900 block">{recommendation.primary_material}</span>
              </div>
              <div>
                <span className="text-[10px] font-bold text-teal-900 uppercase block">Eco-Friendly / Alternative:</span>
                <span className="text-xs font-bold text-slate-800 block">{recommendation.alternative_material}</span>
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 border-t border-emerald-200/70 text-[11px]">
              <div>
                <span className="text-slate-500 block text-[10px]">OTR Barrier:</span>
                <span className="font-semibold">{recommendation.technical_specs?.otr_range}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">WVTR Barrier:</span>
                <span className="font-semibold">{recommendation.technical_specs?.wvtr_range}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">Caliper Thickness:</span>
                <span className="font-semibold">{recommendation.technical_specs?.thickness_um} µm</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">MAP Gas Mix:</span>
                <span className="font-semibold">{recommendation.technical_specs?.map_gas_mix}</span>
              </div>
            </div>

            {recommendation.physics_metrics && (
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 border-t border-emerald-200/50 text-[11px]">
                <div>
                  <span className="text-slate-500 block text-[10px]">Target WVTR Req:</span>
                  <span className="font-semibold">{recommendation.physics_metrics.target_wvtr_req} g/m²/d</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px]">Allowable OTR Req:</span>
                  <span className="font-semibold">{recommendation.physics_metrics.target_otr_req} cc/m²/d</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px]">Vapor Press (ps):</span>
                  <span className="font-semibold">{recommendation.physics_metrics.ps_sat_pa} Pa</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px]">Barrier Safety Factor:</span>
                  <span className="font-bold text-emerald-800">{recommendation.ml_metadata?.safety_factor || 1.8}x</span>
                </div>
              </div>
            )}

            <div className="text-[11px] text-emerald-900 pt-1">
              <span className="font-bold">Scientific Rationale: </span>
              <span>{recommendation.why_material_en}</span>
            </div>
          </div>
        </div>

        {/* Section 3: Statutory India Compliance Shield */}
        <div className="space-y-2">
          <h2 className="text-xs font-bold uppercase tracking-wider text-blue-900 border-l-4 border-blue-600 pl-2">
            3. India Statutory Compliance Shield (FSSAI, BIS & CPCB Mandates)
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div className="p-3 bg-blue-50/60 rounded-lg border border-blue-200">
              <span className="font-bold text-blue-950 block">FSSAI Packaging Regulations, 2018:</span>
              <span className="font-semibold text-slate-900">{complianceData.fssai?.schedule_iv_category}</span>
              <span className="block text-slate-600 text-[10px] mt-0.5">{complianceData.fssai?.material_schedule}</span>
            </div>

            <div className="p-3 bg-blue-50/60 rounded-lg border border-blue-200">
              <span className="font-bold text-blue-950 block">Bureau of Indian Standards (BIS):</span>
              <span className="font-bold text-blue-800 text-sm">{complianceData.bis?.is_code}</span>
              <span className="block text-slate-600 text-[10px] mt-0.5">{complianceData.bis?.title}</span>
            </div>

            <div className="p-3 bg-blue-50/60 rounded-lg border border-blue-200">
              <span className="font-bold text-blue-950 block">IS 9845 Overall Migration Limit:</span>
              <span className="font-bold text-slate-900">{complianceData.migration?.overall_migration_limit}</span>
              <span className="block text-slate-600 text-[10px] mt-0.5">Tested with aqueous, acidic, and fatty simulants.</span>
            </div>

            <div className="p-3 bg-blue-50/60 rounded-lg border border-blue-200">
              <span className="font-bold text-blue-950 block">CPCB Extended Producer Responsibility:</span>
              <span className="font-bold text-purple-900">{complianceData.epr?.category}</span>
              <span className="block text-slate-600 text-[10px] mt-0.5">Mandatory registration on CPCB Central EPR Portal.</span>
            </div>
          </div>
        </div>

        {/* Section 4: Verified Labelling Declarations */}
        <div className="space-y-2">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-800 border-l-4 border-slate-600 pl-2">
            4. FSSAI (Labelling & Display) Checklist & NABL Advisory
          </h2>
          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-[11px] leading-relaxed">
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-1.5 font-medium text-slate-800">
              <span>[✓] FSSAI Logo + 14-Digit License</span>
              <span>[✓] Veg / Non-Veg Color Symbol</span>
              <span>[✓] Net Quantity (Legal Metrology)</span>
              <span>[✓] Maximum Retail Price (MRP)</span>
              <span>[✓] Batch / Lot Identification</span>
              <span>[✓] Mfg Date & Best-Before Date</span>
              <span>[✓] Complete Ingredients List</span>
              <span>[✓] Nutrition Facts per 100g</span>
              <span>[✓] Consumer Care Contact Info</span>
            </div>
            <div className="mt-2 pt-2 border-t border-slate-200 text-[10px] text-slate-600">
              <b>NABL Testing Advisory:</b> Commercial food contact packaging must possess a Certificate of Conformity from an ISO/IEC 17025 accredited laboratory verifying migration limits under IS 9845.
            </div>
          </div>
        </div>

        {/* Statutory Disclaimer Footer */}
        <div className="pt-2 border-t border-slate-200 text-center text-[9px] text-slate-500 leading-tight">
          {t('disclaimer_text')}
        </div>
      </div>
    </div>
  );
};
