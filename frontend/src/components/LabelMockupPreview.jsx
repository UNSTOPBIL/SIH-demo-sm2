import React, { useState } from 'react';
import { Sparkles, ShieldCheck, QrCode, Tag, Check, RefreshCw, Barcode } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export const LabelMockupPreview = ({ commodity, primaryMaterial, complianceData }) => {
  const { language, t } = useLanguage();

  const [packSize, setPackSize] = useState('250 g');
  const [mrpVal, setMrpVal] = useState('180.00');
  const [batchNo, setBatchNo] = useState('ODOP-2026-B084');
  const [mfgDate, setMfgDate] = useState('28/09/2026');
  const [expiryDate, setExpiryDate] = useState('27/03/2027');

  const nameEn = commodity?.name_en || 'Premium Food Commodity';
  const nameHi = commodity?.name_hi || '';
  const odopRegion = commodity?.odop_region || 'India Cluster';
  const moisturePct = parseFloat(commodity?.moisture_pct ?? 7.0);
  const fatPct = parseFloat(commodity?.fat_oil_pct ?? 1.5);

  // Multiplier based on SKU weight
  const skuWeightGrams = packSize === '100 g' ? 100 : packSize === '250 g' ? 250 : packSize === '500 g' ? 500 : 1000;
  const packMultiplier = skuWeightGrams / 100.0;

  // Approximate macronutrients per 100g based on commodity properties
  const estProtein100g = Math.max(1.5, Math.min(25.0, (100 - moisturePct - fatPct) * 0.14)).toFixed(1);
  const estFat100g = fatPct.toFixed(1);
  const estCarb100g = Math.max(10, (100 - moisturePct - fatPct - parseFloat(estProtein100g))).toFixed(1);
  const estCalories100g = Math.round(parseFloat(estProtein100g) * 4 + parseFloat(estCarb100g) * 4 + parseFloat(estFat100g) * 9);

  // Per pack nutrient values
  const estCaloriesPack = Math.round(estCalories100g * packMultiplier);
  const estProteinPack = (parseFloat(estProtein100g) * packMultiplier).toFixed(1);
  const estCarbPack = (parseFloat(estCarb100g) * packMultiplier).toFixed(1);
  const estFatPack = (parseFloat(estFat100g) * packMultiplier).toFixed(1);

  // Determine resin recycling code based on primary material
  const isMultiLayer = primaryMaterial ? (primaryMaterial.includes('Foil') || primaryMaterial.includes('Met') || primaryMaterial.includes('BOPP') || primaryMaterial.includes('PET')) : true;
  const recyclingCode = isMultiLayer ? '7' : '4';
  const recyclingName = isMultiLayer ? 'OTHER (MLP)' : 'LDPE (MONO)';

  return (
    <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-6 md:p-8 shadow-sm space-y-6">
      {/* Header & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 dark:border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider mb-1">
            <Sparkles className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            <span>FSSAI (Labelling & Display) Regulations 2020 Compliant</span>
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white">
            Photorealistic FMCG Stand-Up Pouch Studio
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Interactive virtual mock-up featuring industrial crimp seal textures, ink-jet batch stamping, and statutory declarations.
          </p>
        </div>

        {/* SKU Size Switcher Pills */}
        <div className="flex items-center gap-2 bg-slate-100 dark:bg-slate-800 p-1.5 rounded-2xl self-start sm:self-auto text-xs font-semibold">
          <span className="text-slate-500 dark:text-slate-400 px-2 font-medium">SKU:</span>
          {[
            { sz: '100 g', mrp: '75.00' },
            { sz: '250 g', mrp: '180.00' },
            { sz: '500 g', mrp: '340.00' },
            { sz: '1 kg', mrp: '650.00' }
          ].map(({ sz, mrp }) => (
            <button
              key={sz}
              type="button"
              onClick={() => {
                setPackSize(sz);
                setMrpVal(mrp);
              }}
              className={`px-3 py-1.5 rounded-xl font-bold transition-all duration-150 ${
                packSize === sz
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30 scale-105'
                  : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              {sz}
            </button>
          ))}
        </div>
      </div>

      {/* 3D Physical Pouch Representation Container */}
      <div className="relative max-w-xl mx-auto flex flex-col items-center">
        {/* Ambient Ground Shadow */}
        <div className="absolute -bottom-4 w-4/5 h-8 bg-slate-900/30 dark:bg-black/60 rounded-full blur-xl pointer-events-none" />

        {/* Pouch Bag Shell */}
        <div className="relative w-full bg-gradient-to-b from-slate-100 via-white to-slate-100 dark:from-slate-100 dark:via-white dark:to-slate-100 border-2 border-slate-300 dark:border-slate-600 rounded-3xl shadow-2xl shadow-slate-900/20 overflow-hidden text-slate-900 font-sans transition-all duration-200">
          
          {/* Subtle Diagonal Plastic Gloss Reflection */}
          <div className="absolute inset-0 pouch-gloss-reflection pointer-events-none z-20" />

          {/* TOP CRIMPED HEAT-SEAL STRIP */}
          <div className="relative h-7 w-full pouch-crimp-pattern border-b border-slate-300 flex items-center justify-between px-4 z-10">
            {/* Left Tear Notch */}
            <div className="flex items-center gap-1">
              <div className="w-2.5 h-2.5 bg-slate-400 rotate-45 -ml-4" title="Tear Notch" />
              <span className="text-[8px] font-mono uppercase font-bold text-slate-600 tracking-tighter">◀ TEAR</span>
            </div>

            {/* Central Euro-Slot / Punch Hole Hanging Display */}
            <div className="w-10 h-2 bg-slate-300/80 rounded-full border border-slate-400/50 shadow-inner" />

            {/* Right Tear Notch */}
            <div className="flex items-center gap-1">
              <span className="text-[8px] font-mono uppercase font-bold text-slate-600 tracking-tighter">TEAR ▶</span>
              <div className="w-2.5 h-2.5 bg-slate-400 rotate-45 -mr-4" title="Tear Notch" />
            </div>
          </div>

          {/* MAIN POUCH PRINT AREA */}
          <div className="p-6 md:p-8 space-y-5 relative z-10">
            
            {/* Header: PMFME ODOP Enterprise + 100% FSSAI Veg Emblem */}
            <div className="flex items-start justify-between border-b-2 border-slate-900 pb-3">
              <div>
                <div className="text-[10px] uppercase font-black tracking-widest text-emerald-800 flex items-center gap-1.5">
                  <span className="bg-emerald-100 px-2 py-0.5 rounded text-emerald-900 font-bold">PMFME ODOP CLUSTER</span>
                  <span>·</span>
                  <span>{odopRegion}</span>
                </div>
                <h4 className="text-2xl md:text-3xl font-black text-slate-950 uppercase tracking-tight mt-1">
                  {nameEn}
                </h4>
                {nameHi && (
                  <div className="text-sm font-bold text-slate-700 font-serif">
                    {nameHi}
                  </div>
                )}
                <div className="text-[10px] text-slate-500 font-medium mt-0.5">
                  Primary Barrier: <span className="font-semibold text-slate-800">{primaryMaterial || 'Multi-Layer Barrier Laminate'}</span>
                </div>
              </div>

              {/* Exact 1:1 FSSAI Green Vegetarian Symbol */}
              <div className="flex flex-col items-center shrink-0">
                <div className="w-8 h-8 border-2 border-emerald-700 p-1 flex items-center justify-center bg-white shadow-xs rounded-sm">
                  <div className="w-4 h-4 rounded-full bg-emerald-700" />
                </div>
                <span className="text-[8px] font-black text-emerald-800 uppercase mt-0.5 tracking-tighter">100% VEG</span>
              </div>
            </div>

            {/* Nutritional Information Table with Per 100g & Per Pack scaling */}
            <div className="bg-white rounded-xl border border-slate-300 overflow-hidden shadow-xs">
              <div className="bg-slate-900 text-white px-3 py-1.5 flex items-center justify-between text-[11px] font-black uppercase tracking-wider">
                <span>NUTRITIONAL INFORMATION</span>
                <span className="text-[9px] text-slate-300 font-normal">Approx. Laboratory Values</span>
              </div>
              
              <table className="w-full text-xs border-collapse">
                <thead>
                  <tr className="bg-slate-100/90 border-b border-slate-200 text-[10px] font-black text-slate-700 uppercase">
                    <th className="py-1.5 px-3 text-left">Nutrient Component</th>
                    <th className="py-1.5 px-2 text-right">Per 100 g</th>
                    <th className="py-1.5 px-3 text-right text-emerald-800 font-extrabold bg-emerald-50/50">Per Pack ({packSize})</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 text-[11px]">
                  <tr className="font-bold bg-slate-50/70">
                    <td className="py-1 px-3">Energy / Calories</td>
                    <td className="py-1 px-2 text-right font-mono text-slate-700">{estCalories100g} kcal</td>
                    <td className="py-1 px-3 text-right font-mono text-emerald-800 font-bold bg-emerald-50/30">{estCaloriesPack} kcal</td>
                  </tr>
                  <tr>
                    <td className="py-1 px-3">Protein</td>
                    <td className="py-1 px-2 text-right font-mono text-slate-700">{estProtein100g} g</td>
                    <td className="py-1 px-3 text-right font-mono text-emerald-800 font-bold bg-emerald-50/30">{estProteinPack} g</td>
                  </tr>
                  <tr>
                    <td className="py-1 px-3">Carbohydrates</td>
                    <td className="py-1 px-2 text-right font-mono text-slate-700">{estCarb100g} g</td>
                    <td className="py-1 px-3 text-right font-mono text-emerald-800 font-bold bg-emerald-50/30">{estCarbPack} g</td>
                  </tr>
                  <tr className="text-slate-500 text-[10px]">
                    <td className="py-0.5 px-3 pl-6">- Total Sugars</td>
                    <td className="py-0.5 px-2 text-right font-mono">1.2 g</td>
                    <td className="py-0.5 px-3 text-right font-mono bg-emerald-50/30">{(1.2 * packMultiplier).toFixed(1)} g</td>
                  </tr>
                  <tr className="text-slate-500 text-[10px]">
                    <td className="py-0.5 px-3 pl-6">- Added Sugars</td>
                    <td className="py-0.5 px-2 text-right font-mono">0.0 g</td>
                    <td className="py-0.5 px-3 text-right font-mono bg-emerald-50/30">0.0 g</td>
                  </tr>
                  <tr>
                    <td className="py-1 px-3">Total Fat</td>
                    <td className="py-1 px-2 text-right font-mono text-slate-700">{estFat100g} g</td>
                    <td className="py-1 px-3 text-right font-mono text-emerald-800 font-bold bg-emerald-50/30">{estFatPack} g</td>
                  </tr>
                  <tr className="text-slate-500 text-[10px]">
                    <td className="py-0.5 px-3 pl-6">- Saturated Fatty Acids</td>
                    <td className="py-0.5 px-2 text-right font-mono">{(parseFloat(estFat100g) * 0.28).toFixed(1)} g</td>
                    <td className="py-0.5 px-3 text-right font-mono bg-emerald-50/30">{(parseFloat(estFatPack) * 0.28).toFixed(1)} g</td>
                  </tr>
                  <tr className="text-slate-500 text-[10px]">
                    <td className="py-0.5 px-3 pl-6">- Trans Fatty Acids</td>
                    <td className="py-0.5 px-2 text-right font-mono">0.0 g</td>
                    <td className="py-0.5 px-3 text-right font-mono bg-emerald-50/30">0.0 g</td>
                  </tr>
                  <tr>
                    <td className="py-1 px-3 font-semibold">Sodium</td>
                    <td className="py-1 px-2 text-right font-mono text-slate-700">12.5 mg</td>
                    <td className="py-1 px-3 text-right font-mono text-emerald-800 font-bold bg-emerald-50/30">{(12.5 * packMultiplier).toFixed(1)} mg</td>
                  </tr>
                </tbody>
              </table>
            </div>

            {/* Ingredients & Allergen Advisory Callout */}
            <div className="text-[11px] space-y-1 bg-slate-50 p-3 rounded-xl border border-slate-300">
              <div>
                <strong className="uppercase text-slate-900">INGREDIENTS:</strong> Pure {nameEn} (100%). No synthetic colors, preservatives, or artificial additives.
              </div>
              <div className="text-slate-600 text-[10px]">
                <strong>ALLERGEN ADVICE:</strong> Packed in a clean facility conforming to FSSAI Schedule IV GMP guidelines.
              </div>
            </div>

            {/* INDUSTRIAL INK-JET DOT-MATRIX STATUTORY DATA STRIP */}
            <div className="bg-slate-100/90 rounded-xl border border-slate-300 p-3 grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
              <div>
                <span className="text-[9px] text-slate-500 uppercase block font-semibold">Net Quantity</span>
                <span className="font-mono font-black text-sm text-slate-900 bg-white border border-slate-300 rounded px-1.5 py-0.5 inline-block">
                  {packSize}
                </span>
              </div>

              <div>
                <span className="text-[9px] text-slate-500 uppercase block font-semibold">Batch Number</span>
                <span className="font-mono font-bold text-xs text-slate-800 bg-white border border-slate-300 rounded px-1.5 py-0.5 inline-block tracking-wider">
                  {batchNo}
                </span>
              </div>

              <div>
                <span className="text-[9px] text-slate-500 uppercase block font-semibold">Date of Packing</span>
                <span className="font-mono font-bold text-xs text-slate-800 bg-white border border-slate-300 rounded px-1.5 py-0.5 inline-block">
                  {mfgDate}
                </span>
              </div>

              <div>
                <span className="text-[9px] text-slate-500 uppercase block font-semibold">Max Retail Price</span>
                <span className="font-mono font-black text-sm text-emerald-800 bg-white border border-emerald-300 rounded px-1.5 py-0.5 inline-block">
                  ₹ {mrpVal}
                </span>
                <span className="text-[8px] text-slate-500 block leading-none mt-0.5">(Incl. of all taxes)</span>
              </div>
            </div>

            {/* FSSAI Central License & CPCB EPR Barcode Footer */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-1 border-t-2 border-slate-900">
              {/* FSSAI Official Stamp */}
              <div className="flex items-center gap-3">
                <div className="border-2 border-slate-900 px-2.5 py-1 rounded bg-white text-center shadow-xs">
                  <div className="text-[12px] font-black tracking-widest text-slate-900 italic font-serif">fssai</div>
                  <div className="text-[8px] font-mono font-bold tracking-tight">Lic No. 10024011009845</div>
                </div>
                <div className="text-[10px] text-slate-600 leading-tight">
                  <strong className="block text-slate-900">Central Licensing Authority</strong>
                  Schedule IV (Packaging) Compliant
                </div>
              </div>

              {/* CPCB Mobius Recycling Loop & Barcode SVG */}
              <div className="flex items-center gap-4">
                {/* Mobius Recycling Icon */}
                <div className="flex items-center gap-2 bg-slate-50 px-2.5 py-1.5 rounded-xl border border-slate-300 text-center">
                  <div className="w-8 h-8 border border-slate-800 rounded-full flex flex-col items-center justify-center font-bold text-[9px] bg-white">
                    <span className="text-[10px]">♳</span>
                    <span className="text-[7px] leading-none">{recyclingCode}</span>
                  </div>
                  <div className="text-[9px] text-slate-700 leading-tight text-left">
                    <strong className="block text-slate-900">CPCB EPR</strong>
                    {recyclingName}
                  </div>
                </div>

                {/* Industrial Vector Barcode SVG */}
                <div className="flex flex-col items-center">
                  <svg className="h-8 w-24" viewBox="0 0 100 30" fill="currentColor">
                    <rect x="0" y="0" width="2" height="26" />
                    <rect x="3" y="0" width="1" height="26" />
                    <rect x="6" y="0" width="3" height="26" />
                    <rect x="11" y="0" width="1" height="26" />
                    <rect x="14" y="0" width="2" height="26" />
                    <rect x="18" y="0" width="4" height="26" />
                    <rect x="24" y="0" width="1" height="26" />
                    <rect x="27" y="0" width="2" height="26" />
                    <rect x="31" y="0" width="3" height="26" />
                    <rect x="36" y="0" width="1" height="26" />
                    <rect x="39" y="0" width="2" height="26" />
                    <rect x="43" y="0" width="4" height="26" />
                    <rect x="49" y="0" width="1" height="26" />
                    <rect x="52" y="0" width="3" height="26" />
                    <rect x="57" y="0" width="2" height="26" />
                    <rect x="61" y="0" width="1" height="26" />
                    <rect x="64" y="0" width="4" height="26" />
                    <rect x="70" y="0" width="2" height="26" />
                    <rect x="74" y="0" width="1" height="26" />
                    <rect x="77" y="0" width="3" height="26" />
                    <rect x="82" y="0" width="2" height="26" />
                    <rect x="86" y="0" width="1" height="26" />
                    <rect x="89" y="0" width="3" height="26" />
                    <rect x="94" y="0" width="2" height="26" />
                    <rect x="98" y="0" width="2" height="26" />
                  </svg>
                  <span className="font-mono text-[8px] text-slate-600 tracking-widest mt-0.5">8901234567890</span>
                </div>
              </div>
            </div>

            {/* Mandatory Statutory Advisory Callouts */}
            <div className="text-[9px] text-slate-500 border-t border-slate-200 pt-2 flex flex-col sm:flex-row items-center justify-between gap-1 font-medium">
              <span>MANUFACTURED UNDER PMFME SCHEME BY ODOP PRODUCER COOPERATIVE</span>
              <span className="font-bold text-slate-700">STORE IN A COOL, DRY PLACE AWAY FROM SUNLIGHT</span>
            </div>
          </div>

          {/* BOTTOM CRIMPED HEAT-SEAL STRIP */}
          <div className="relative h-5 w-full pouch-crimp-pattern border-t border-slate-300 z-10 flex items-center justify-center">
            <span className="text-[7px] font-mono uppercase tracking-widest text-slate-600 font-bold">
              HERMETIC INDUSTRIAL SEAL · IS 10146 COMPLIANT
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
