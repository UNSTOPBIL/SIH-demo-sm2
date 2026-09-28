import React, { useState } from 'react';
import { Tag, ShieldCheck, QrCode, AlertCircle, RefreshCw, Check, Sparkles, Building, PhoneCall } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export const LabelMockupPreview = ({ commodity, primaryMaterial, complianceData }) => {
  const { language, t } = useLanguage();

  const [packSize, setPackSize] = useState('250 g');
  const [mrpVal, setMrpVal] = useState('180.00');
  const [batchNo, setBatchNo] = useState('ODOP-2026-B084');

  const nameEn = commodity?.name_en || 'Premium Food Commodity';
  const nameHi = commodity?.name_hi || '';
  const odopRegion = commodity?.odop_region || 'India Cluster';
  const moisturePct = commodity?.moisture_pct ?? 10.0;
  const fatPct = commodity?.fat_oil_pct ?? 2.0;

  // Approximate macronutrients per 100g based on commodity properties
  const estProtein = Math.max(1.5, Math.min(25.0, (100 - moisturePct - fatPct) * 0.14)).toFixed(1);
  const estFat = fatPct.toFixed(1);
  const estCarb = Math.max(10, (100 - moisturePct - fatPct - parseFloat(estProtein))).toFixed(1);
  const estCalories = Math.round(parseFloat(estProtein) * 4 + parseFloat(estCarb) * 4 + parseFloat(estFat) * 9);

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 dark:border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-indigo-700 dark:text-indigo-400 uppercase tracking-wider mb-1">
            <Sparkles className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
            <span>FSSAI (Labelling & Display) Regulations 2020 Compliant</span>
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white">
            Interactive FMCG Back-of-Pack Label Studio
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Photorealistic rendering of mandatory statutory declarations, nutrition tables, and CPCB EPR barcodes.
          </p>
        </div>

        {/* Pack Size Switcher */}
        <div className="flex items-center gap-2 text-xs">
          <span className="text-slate-500 dark:text-slate-400 font-medium">SKU Size:</span>
          {['100 g', '250 g', '500 g', '1 kg'].map(sz => (
            <button
              key={sz}
              type="button"
              onClick={() => {
                setPackSize(sz);
                if (sz === '100 g') setMrpVal('75.00');
                if (sz === '250 g') setMrpVal('180.00');
                if (sz === '500 g') setMrpVal('340.00');
                if (sz === '1 kg') setMrpVal('650.00');
              }}
              className={`px-2.5 py-1 rounded-lg border font-semibold transition ${
                packSize === sz
                  ? 'bg-indigo-600 text-white border-indigo-600 shadow-xs'
                  : 'bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:border-slate-300'
              }`}
            >
              {sz}
            </button>
          ))}
        </div>
      </div>

      {/* Photorealistic Back-of-Pack Mockup Container */}
      <div className="max-w-2xl mx-auto bg-white dark:bg-slate-50 border-2 border-slate-300 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-md relative font-sans text-slate-900 space-y-5">
        {/* Top Bar: Brand, Crop Title & FSSAI Veg Symbol */}
        <div className="flex items-start justify-between border-b-2 border-slate-900 pb-3">
          <div>
            <div className="text-[10px] uppercase font-black tracking-widest text-emerald-800 flex items-center gap-1.5">
              <span>PMFME ODOP ENTERPRISE</span>
              <span>·</span>
              <span>{odopRegion}</span>
            </div>
            <h4 className="text-xl md:text-2xl font-black text-slate-950 uppercase tracking-tight">
              {nameEn}
            </h4>
            {nameHi && (
              <div className="text-sm font-bold text-slate-700 font-serif">
                {nameHi}
              </div>
            )}
          </div>

          {/* FSSAI Green Vegetarian Symbol (Square with green circle) */}
          <div className="flex flex-col items-center">
            <div className="w-8 h-8 border-2 border-emerald-600 p-1 flex items-center justify-center bg-white shadow-xs">
              <div className="w-4 h-4 rounded-full bg-emerald-600"></div>
            </div>
            <span className="text-[8px] font-bold text-emerald-800 uppercase mt-0.5 tracking-tighter">100% VEG</span>
          </div>
        </div>

        {/* Nutritional Information Table (Per 100g) */}
        <div>
          <div className="flex items-center justify-between text-xs font-black uppercase border-b-2 border-slate-900 pb-1">
            <span>NUTRITIONAL INFORMATION</span>
            <span>Approx. Values per 100g</span>
          </div>
          <table className="w-full text-xs border-collapse">
            <tbody>
              <tr className="border-b border-slate-200 font-bold bg-slate-100/60">
                <td className="py-1 px-1">Energy / Calories</td>
                <td className="py-1 px-1 text-right font-mono">{estCalories} kcal</td>
              </tr>
              <tr className="border-b border-slate-200">
                <td className="py-1 px-1">Protein</td>
                <td className="py-1 px-1 text-right font-mono">{estProtein} g</td>
              </tr>
              <tr className="border-b border-slate-200">
                <td className="py-1 px-1">Carbohydrates</td>
                <td className="py-1 px-1 text-right font-mono">{estCarb} g</td>
              </tr>
              <tr className="border-b border-slate-200 text-slate-600">
                <td className="py-1 px-1 pl-4">- Total Sugars</td>
                <td className="py-1 px-1 text-right font-mono">1.2 g</td>
              </tr>
              <tr className="border-b border-slate-200 text-slate-600">
                <td className="py-1 px-1 pl-4">- Added Sugars</td>
                <td className="py-1 px-1 text-right font-mono">0.0 g</td>
              </tr>
              <tr className="border-b border-slate-200">
                <td className="py-1 px-1">Total Fat</td>
                <td className="py-1 px-1 text-right font-mono">{estFat} g</td>
              </tr>
              <tr className="border-b border-slate-200 text-slate-600">
                <td className="py-1 px-1 pl-4">- Saturated Fatty Acids</td>
                <td className="py-1 px-1 text-right font-mono">{(estFat * 0.28).toFixed(1)} g</td>
              </tr>
              <tr className="border-b border-slate-200 text-slate-600">
                <td className="py-1 px-1 pl-4">- Trans Fatty Acids</td>
                <td className="py-1 px-1 text-right font-mono">0.0 g</td>
              </tr>
              <tr className="border-b-2 border-slate-900">
                <td className="py-1 px-1 font-semibold">Sodium</td>
                <td className="py-1 px-1 text-right font-mono">12.5 mg</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Ingredients & Allergen Declaration */}
        <div className="text-xs space-y-1 bg-slate-50 p-2.5 rounded-lg border border-slate-200">
          <div>
            <strong className="uppercase">INGREDIENTS:</strong> Pure {nameEn} (100%). No added preservatives, synthetic colors, or artificial flavors.
          </div>
          <div className="text-slate-600 text-[11px]">
            <strong>ALLERGEN ADVICE:</strong> Processed in a dedicated facility conforming to FSSAI Schedule 4 GMP guidelines.
          </div>
        </div>

        {/* Commercial & Statutory Data Strip (Grid of 4) */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs border-y-2 border-slate-900 py-3 bg-white">
          <div className="border-r border-slate-200 pr-2">
            <span className="text-[10px] text-slate-500 uppercase block font-semibold">Net Quantity</span>
            <span className="font-extrabold text-sm">{packSize}</span>
          </div>

          <div className="border-r border-slate-200 pr-2">
            <span className="text-[10px] text-slate-500 uppercase block font-semibold">Batch No.</span>
            <span className="font-bold text-xs font-mono">{batchNo}</span>
          </div>

          <div className="border-r border-slate-200 pr-2">
            <span className="text-[10px] text-slate-500 uppercase block font-semibold">Date of Packing</span>
            <span className="font-bold text-xs font-mono">28/09/2026</span>
          </div>

          <div>
            <span className="text-[10px] text-slate-500 uppercase block font-semibold">Max Retail Price</span>
            <span className="font-extrabold text-sm text-emerald-800 font-mono">₹ {mrpVal}</span>
            <span className="text-[8px] text-slate-400 block leading-none">(Incl. of all taxes)</span>
          </div>
        </div>

        {/* FSSAI License, CPCB EPR & Plastic Waste Recycling Declarations */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-1">
          {/* FSSAI Badge */}
          <div className="flex items-center gap-3">
            <div className="border-2 border-slate-900 px-2 py-1 rounded bg-white text-center">
              <div className="text-[11px] font-black tracking-widest text-slate-900 italic font-serif">fssai</div>
              <div className="text-[8px] font-mono font-bold tracking-tight">Lic No. 10024011009845</div>
            </div>
            <div className="text-[10px] text-slate-600 leading-tight">
              Central Licensing Authority<br />
              Schedule IV (Packaging) Compliant
            </div>
          </div>

          {/* CPCB EPR Mobius Loop Symbol */}
          <div className="flex items-center gap-2.5 bg-slate-100 px-3 py-1.5 rounded-xl border border-slate-200 text-xs">
            <div className="w-8 h-8 border border-slate-800 rounded-full flex flex-col items-center justify-center font-bold text-[9px] bg-white">
              <span>♳</span>
              <span className="text-[7px] leading-none">OTHER</span>
            </div>
            <div className="text-[10px] text-slate-700 leading-tight">
              <strong className="block text-slate-900">CPCB EPR MANDATE</strong>
              PWM Rules 2016 Reg: CPCB-2026-EPR
            </div>
          </div>
        </div>

        {/* Footer Mandatory Callouts */}
        <div className="text-[10px] text-slate-500 border-t border-slate-200 pt-2 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>MANUFACTURED UNDER PMFME SCHEME BY ODOP PRODUCER COOPERATIVE</span>
          <span className="font-semibold text-slate-700">STORE IN A COOL, DRY PLACE AWAY FROM DIRECT SUNLIGHT</span>
        </div>
      </div>
    </div>
  );
};
