import React, { useState } from 'react';
import { Package, ShieldCheck, Leaf, ArrowRight, ArrowLeft, ChevronDown, ChevronUp, Cpu, Award, Beaker, Layers, Activity, AlertTriangle, IndianRupee, TrendingUp, Recycle, BarChart3, TreePine } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { LaminateVisualizer } from './LaminateVisualizer';
import { ShelfLifeSimulator } from './ShelfLifeSimulator';

export const Screen2Recommendation = ({ recommendation, onNext, onBack }) => {
  const { language, t } = useLanguage();
  const [showExpertMode, setShowExpertMode] = useState(false);

  if (!recommendation) return null;

  const {
    name_en,
    name_hi,
    odop_region,
    primary_material,
    primary_structure,
    alternative_material,
    alt_structure,
    barrier_profile,
    technical_specs,
    why_material_en,
    why_material_hi,
    ml_metadata,
    physics_metrics,
    shelf_life_decay,
    shelf_life_days,
    warning_flag,
    economics,
    sustainability
  } = recommendation;

  // Rating badge coloring helper
  const getRatingBadge = (rating) => {
    const r = (rating || '').toLowerCase();
    if (r.includes('superior') || r.includes('ultra')) {
      return { bg: 'bg-emerald-100 text-emerald-800 border-emerald-300', dots: 5, label: t('rating_superior') };
    } else if (r.includes('high')) {
      return { bg: 'bg-blue-100 text-blue-800 border-blue-300', dots: 4, label: t('rating_high') };
    } else if (r.includes('moderate')) {
      return { bg: 'bg-amber-100 text-amber-800 border-amber-300', dots: 3, label: t('rating_moderate') };
    } else if (r.includes('breathable')) {
      return { bg: 'bg-teal-100 text-teal-800 border-teal-300', dots: 3, label: t('rating_breathable') };
    } else if (r.includes('vented')) {
      return { bg: 'bg-indigo-100 text-indigo-800 border-indigo-300', dots: 2, label: t('rating_vented') };
    }
    return { bg: 'bg-slate-100 text-slate-800 border-slate-300', dots: 2, label: t('rating_poor') };
  };

  const moistureBadge = getRatingBadge(barrier_profile?.moisture_barrier);
  const oxygenBadge = getRatingBadge(barrier_profile?.oxygen_barrier);
  const strengthBadge = getRatingBadge(barrier_profile?.mechanical_strength);

  const activeWarning = warning_flag || ml_metadata?.warning_flag;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Top Header */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4 transition-colors duration-200">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider mb-1">
            <Award className="w-4 h-4" />
            <span>{odop_region}</span>
          </div>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
            {language === 'hi' ? name_hi : name_en}
          </h2>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-0.5">
            {t('recommendation_subtitle')}
          </p>
        </div>

        {/* ML Credential Tag */}
        {ml_metadata && (
          <div className="flex items-center gap-2 bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 px-3.5 py-2 rounded-xl text-xs font-medium text-emerald-900 dark:text-emerald-300">
            <Cpu className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            <div>
              <span className="font-bold block">AI Verified Model</span>
              <span className="text-emerald-700 dark:text-emerald-400">CV Accuracy: {ml_metadata.cross_val_accuracy}</span>
            </div>
          </div>
        )}
      </div>

      {/* Critical Climate / Barrier Advisory Banner */}
      {activeWarning && (
        <div className="bg-amber-50 dark:bg-amber-950/50 border-2 border-amber-400 dark:border-amber-700 rounded-2xl p-4 flex items-start gap-3 shadow-sm">
          <AlertTriangle className="w-6 h-6 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <h4 className="text-sm font-bold text-amber-900 dark:text-amber-300 uppercase tracking-wide">
                MoFPI Packaging Safety Advisory
              </h4>
              <span className="text-[10px] bg-amber-200 dark:bg-amber-900/80 text-amber-900 dark:text-amber-300 px-2 py-0.5 rounded font-mono font-bold border border-amber-300 dark:border-amber-700">
                CRITICAL BARRIER ALERT
              </span>
            </div>
            <p className="text-xs text-amber-800 dark:text-amber-300 mt-1 font-medium leading-relaxed">
              {activeWarning}
            </p>
          </div>
        </div>
      )}

      {/* Primary & Alternative Material Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Primary Recommended Material */}
        <div className="bg-gradient-to-br from-emerald-50 via-white to-green-50/50 dark:from-emerald-950/40 dark:via-slate-900 dark:to-slate-900 rounded-2xl border-2 border-emerald-500 dark:border-emerald-600 p-6 shadow-md relative overflow-hidden flex flex-col justify-between transition-colors duration-200">
          <div className="absolute top-0 right-0 bg-emerald-600 text-white text-[11px] font-bold px-3 py-1 rounded-bl-xl tracking-wide uppercase">
            {t('primary_material_badge')}
          </div>
          <div>
            <div className="w-12 h-12 rounded-xl bg-emerald-600 text-white flex items-center justify-center mb-4 shadow">
              <Package className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white leading-snug">
              {primary_material}
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-2">
              Primary multi-layer composite engineered for target shelf life and physical barrier requirements.
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-emerald-100 dark:border-emerald-900/60 flex items-center gap-2 text-xs font-semibold text-emerald-800 dark:text-emerald-400">
            <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            <span>Optimal Barrier & Shelf-Life Match</span>
          </div>
        </div>

        {/* Sustainable / Alternative Material */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm flex flex-col justify-between hover:border-slate-300 dark:hover:border-slate-700 transition">
          <div>
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 bg-teal-50 dark:bg-teal-950/60 border border-teal-200 dark:border-teal-800 text-teal-800 dark:text-teal-300 rounded-full text-xs font-semibold mb-3">
              <Leaf className="w-3.5 h-3.5 text-teal-600 dark:text-teal-400" />
              <span>{t('alt_material_badge')}</span>
            </div>
            <h3 className="text-lg font-bold text-slate-900 dark:text-white leading-snug">
              {alternative_material}
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-2">
              Eco-conscious or recyclable substitute meeting circular economy objectives.
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-xs text-slate-500 dark:text-slate-400">
            Suitable for export or green-certified PMFME packaging brands.
          </div>
        </div>
      </div>

      {/* 2.5D Interactive Laminate Visualizer */}
      <LaminateVisualizer
        primaryStructure={primary_structure}
        altStructure={alt_structure}
        safetyFactor={ml_metadata?.safety_factor}
      />

      {/* Biophysical Shelf-Life Decay Simulator */}
      <ShelfLifeSimulator
        shelfLifeDecay={shelf_life_decay}
        physicsMetrics={physics_metrics}
        targetShelfLifeDays={shelf_life_days || 180}
        commodityName={name_en}
      />

      {/* Barrier Gauges Card */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-4 transition-colors duration-200">
        <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
          <span>{t('barrier_profile_title')}</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {/* Moisture Gauge */}
          <div className="p-4 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-200 dark:border-slate-700 space-y-2">
            <span className="text-xs font-medium text-slate-600 dark:text-slate-300 block">{t('moisture_barrier')}</span>
            <div className="flex items-center gap-1.5">
              {[1, 2, 3, 4, 5].map((idx) => (
                <div
                  key={idx}
                  className={`h-2 flex-1 rounded-full ${
                    idx <= moistureBadge.dots ? 'bg-emerald-500' : 'bg-slate-200 dark:bg-slate-700'
                  }`}
                />
              ))}
            </div>
            <span className={`inline-block px-2 py-0.5 rounded text-xs font-semibold border ${moistureBadge.bg}`}>
              {moistureBadge.label}
            </span>
          </div>

          {/* Oxygen Gauge */}
          <div className="p-4 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-200 dark:border-slate-700 space-y-2">
            <span className="text-xs font-medium text-slate-600 dark:text-slate-300 block">{t('oxygen_barrier')}</span>
            <div className="flex items-center gap-1.5">
              {[1, 2, 3, 4, 5].map((idx) => (
                <div
                  key={idx}
                  className={`h-2 flex-1 rounded-full ${
                    idx <= oxygenBadge.dots ? 'bg-blue-500' : 'bg-slate-200 dark:bg-slate-700'
                  }`}
                />
              ))}
            </div>
            <span className={`inline-block px-2 py-0.5 rounded text-xs font-semibold border ${oxygenBadge.bg}`}>
              {oxygenBadge.label}
            </span>
          </div>

          {/* Puncture / Mechanical Strength */}
          <div className="p-4 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-200 dark:border-slate-700 space-y-2">
            <span className="text-xs font-medium text-slate-600 dark:text-slate-300 block">{t('strength_barrier')}</span>
            <div className="flex items-center gap-1.5">
              {[1, 2, 3, 4, 5].map((idx) => (
                <div
                  key={idx}
                  className={`h-2 flex-1 rounded-full ${
                    idx <= strengthBadge.dots ? 'bg-amber-500' : 'bg-slate-200 dark:bg-slate-700'
                  }`}
                />
              ))}
            </div>
            <span className={`inline-block px-2 py-0.5 rounded text-xs font-semibold border ${strengthBadge.bg}`}>
              {strengthBadge.label}
            </span>
          </div>
        </div>
      </div>

      {/* Module 1: Industrial Converter Economics & Spoilage ROI Card */}
      {economics && economics.gsm_metrics && (
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-4 transition-colors duration-200">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-3">
            <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <IndianRupee className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
              <span>Industrial Converter Economics & Pouch Yield</span>
            </h3>
            <span className="text-xs bg-emerald-50 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 px-2.5 py-1 rounded-full font-semibold">
              Conversion Margin: ₹35/kg included
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <div className="p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1">
              <span className="text-slate-500 dark:text-slate-400 font-medium block">Total Composite GSM</span>
              <span className="text-lg font-bold text-slate-900 dark:text-slate-100 font-mono">
                {economics.gsm_metrics.total_gsm} <span className="text-xs font-normal text-slate-500 dark:text-slate-400">g/m²</span>
              </span>
            </div>
            <div className="p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1">
              <span className="text-slate-500 dark:text-slate-400 font-medium block">Film Yield</span>
              <span className="text-lg font-bold text-emerald-700 dark:text-emerald-400 font-mono">
                {economics.gsm_metrics.film_yield_m2_per_kg} <span className="text-xs font-normal text-slate-500 dark:text-slate-400">m²/kg</span>
              </span>
            </div>
            <div className="p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1">
              <span className="text-slate-500 dark:text-slate-400 font-medium block">Pouch Unit Cost</span>
              <span className="text-lg font-bold text-slate-900 dark:text-slate-100 font-mono">
                ₹{economics.unit_cost_metrics?.cost_per_pouch_inr} <span className="text-xs font-normal text-slate-500 dark:text-slate-400">/ pouch</span>
              </span>
            </div>
            <div className="p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1">
              <span className="text-slate-500 dark:text-slate-400 font-medium block">Cost per 1,000 Pouches</span>
              <span className="text-lg font-bold text-slate-900 dark:text-slate-100 font-mono">
                ₹{economics.unit_cost_metrics?.cost_per_1000_pouches_inr?.toLocaleString()}
              </span>
            </div>
          </div>

          {/* Spoilage vs. Barrier ROI Callout */}
          {economics.spoilage_roi && (
            <div className="p-4 bg-gradient-to-r from-emerald-50 via-green-50 to-teal-50 dark:from-emerald-950/40 dark:via-slate-900 dark:to-teal-950/40 rounded-xl border border-emerald-200 dark:border-emerald-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4 text-xs">
              <div className="space-y-1">
                <div className="flex items-center gap-1.5 text-emerald-900 dark:text-emerald-300 font-bold text-sm">
                  <TrendingUp className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                  <span>Inventory Protection & Spoilage Prevention ROI</span>
                </div>
                <p className="text-slate-600 dark:text-slate-300 max-w-xl">
                  {economics.spoilage_roi.economic_verdict}
                </p>
              </div>

              <div className="flex items-center gap-3 shrink-0">
                <div className="text-right">
                  <span className="text-[10px] text-slate-400 dark:text-slate-500 block uppercase font-bold">Net Financial ROI</span>
                  <span className="text-lg font-black text-emerald-800 dark:text-emerald-400">
                    +{economics.spoilage_roi.roi_percentage}%
                  </span>
                </div>
                <div className="text-right pl-3 border-l border-emerald-200 dark:border-emerald-800">
                  <span className="text-[10px] text-slate-400 dark:text-slate-500 block uppercase font-bold">Breakeven</span>
                  <span className="text-lg font-black text-slate-800 dark:text-slate-200">
                    {economics.spoilage_roi.pouches_to_breakeven} <span className="text-xs font-normal">packs</span>
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Module 2: CPCB EPR Liability & Embodied Carbon LCA Card */}
      {sustainability && sustainability.embodied_carbon && (
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-4 transition-colors duration-200">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-3">
            <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Recycle className="w-5 h-5 text-teal-600 dark:text-teal-400" />
              <span>CPCB EPR Liability & Embodied Carbon LCA</span>
            </h3>
            <span className="text-xs font-bold px-2.5 py-0.5 rounded-full"
                  style={{ backgroundColor: `${sustainability.circularity_rating?.badge_color}25`, color: sustainability.circularity_rating?.badge_color }}>
              {sustainability.circularity_rating?.grade} · {sustainability.circularity_rating?.label}
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
            <div className="p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1">
              <span className="text-slate-500 dark:text-slate-400 font-medium block">Embodied Carbon Footprint</span>
              <span className="text-base font-bold text-slate-900 dark:text-slate-100 font-mono">
                {sustainability.embodied_carbon.carbon_per_pouch_g_co2e} <span className="text-xs font-normal text-slate-500 dark:text-slate-400">g CO2e / pack</span>
              </span>
              <span className="text-[10px] text-slate-400 dark:text-slate-500 block">
                {sustainability.embodied_carbon.carbon_per_10k_pouches_kg_co2e} kg CO2e per 10k pouches
              </span>
            </div>

            <div className="p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1">
              <span className="text-slate-500 dark:text-slate-400 font-medium block">CPCB EPR Classification</span>
              <span className="text-xs font-bold text-slate-900 dark:text-slate-100 block truncate" title={sustainability.cpcb_epr_compliance?.category_name}>
                {sustainability.cpcb_epr_compliance?.category_name}
              </span>
              <span className="text-[10px] text-emerald-700 dark:text-emerald-400 font-semibold block">
                Fee Rate: ₹{sustainability.cpcb_epr_compliance?.fee_rate_per_ton_inr?.toLocaleString()} / ton
              </span>
            </div>

            <div className="p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1">
              <span className="text-slate-500 dark:text-slate-400 font-medium block">Est. Annual EPR Obligation</span>
              <span className="text-base font-bold text-slate-900 dark:text-slate-100 font-mono">
                {sustainability.cpcb_epr_compliance?.is_exempt ? (
                  <span className="text-emerald-700 dark:text-emerald-400 font-bold">₹0 (IS 17088 Exempt)</span>
                ) : (
                  <span>₹{sustainability.cpcb_epr_compliance?.estimated_annual_epr_liability_inr?.toLocaleString()} <span className="text-xs font-normal text-slate-400 dark:text-slate-500">/ yr</span></span>
                )}
              </span>
              <span className="text-[10px] text-slate-400 dark:text-slate-500 block">
                Based on {sustainability.cpcb_epr_compliance?.assumed_annual_pouches?.toLocaleString()} pouches/yr
              </span>
            </div>
          </div>

          {/* Circularity Guidance */}
          <div className="p-3.5 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-200 dark:border-slate-700 text-xs flex items-start gap-2.5">
            <TreePine className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
            <div className="space-y-0.5">
              <span className="font-bold text-slate-800 dark:text-slate-200">
                Circularity Stream: {sustainability.circularity_rating?.recycling_stream}
              </span>
              <p className="text-slate-600 dark:text-slate-400 text-[11px]">
                {language === 'hi' ? sustainability.circularity_rating?.guidance_hi : sustainability.circularity_rating?.guidance_en}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Why This Material (Scientific Rationale Card) */}
      <div className="bg-emerald-900 dark:bg-emerald-950 border border-emerald-800 dark:border-emerald-800/80 text-white rounded-2xl p-6 shadow-md space-y-2">
        <h4 className="text-sm font-semibold uppercase tracking-wider text-emerald-300 flex items-center gap-2">
          <Beaker className="w-4 h-4 text-emerald-400" />
          <span>{t('why_title')}</span>
        </h4>
        <p className="text-sm md:text-base leading-relaxed text-emerald-100 font-medium">
          {language === 'hi' ? why_material_hi : why_material_en}
        </p>
      </div>

      {/* Expandable Expert / Scientific Mode Toggle */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden transition-colors duration-200">
        <button
          type="button"
          onClick={() => setShowExpertMode(!showExpertMode)}
          className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-slate-50 dark:hover:bg-slate-800/70 transition"
        >
          <div className="flex items-center gap-2">
            <Beaker className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            <span className="text-sm font-bold text-slate-800 dark:text-slate-200">
              {showExpertMode ? t('expert_toggle_on') : t('expert_toggle_off')}
            </span>
          </div>
          {showExpertMode ? (
            <ChevronUp className="w-5 h-5 text-slate-500 dark:text-slate-400" />
          ) : (
            <ChevronDown className="w-5 h-5 text-slate-500 dark:text-slate-400" />
          )}
        </button>

        {showExpertMode && (
          <div className="px-6 pb-6 pt-2 border-t border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/40 space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 text-xs">
              <div className="p-3 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1">
                <span className="text-slate-500 dark:text-slate-400 font-medium">{t('otr_label')}</span>
                <span className="font-bold text-slate-900 dark:text-slate-100 text-sm block">{technical_specs?.otr_range}</span>
                <span className="text-[10px] text-slate-400 dark:text-slate-500">Tested per ASTM D3985 / ISO 15105-2 at 23°C</span>
              </div>

              <div className="p-3 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1">
                <span className="text-slate-500 dark:text-slate-400 font-medium">{t('wvtr_label')}</span>
                <span className="font-bold text-slate-900 dark:text-slate-100 text-sm block">{technical_specs?.wvtr_range}</span>
                <span className="text-[10px] text-slate-400 dark:text-slate-500">Tested per ASTM F1249 / ISO 15106 at 38°C/90% RH</span>
              </div>

              <div className="p-3 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1">
                <span className="text-slate-500 dark:text-slate-400 font-medium">{t('thickness_label')}</span>
                <span className="font-bold text-slate-900 dark:text-slate-100 text-sm block">{technical_specs?.thickness_um} µm</span>
                <span className="text-[10px] text-slate-400 dark:text-slate-500">Optimal puncture resistance and sealing caliber</span>
              </div>

              <div className="p-3 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1">
                <span className="text-slate-500 dark:text-slate-400 font-medium">{t('map_label')}</span>
                <span className="font-bold text-slate-900 dark:text-slate-100 text-sm block">{technical_specs?.map_gas_mix}</span>
                <span className="text-[10px] text-slate-400 dark:text-slate-500">Gas equilibrium calculation for headspace</span>
              </div>
            </div>

            {/* Biophysical Formulation Equations Card */}
            {physics_metrics && (
              <div className="p-4 bg-emerald-50/60 dark:bg-emerald-950/40 rounded-xl border border-emerald-200 dark:border-emerald-800 text-xs space-y-2">
                <div className="font-bold text-emerald-900 dark:text-emerald-300 flex items-center gap-1.5">
                  <Activity className="w-4 h-4 text-emerald-700 dark:text-emerald-400" />
                  <span>Biophysical Barrier Demand Metrics (Governing Equations)</span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-slate-700 dark:text-slate-300 font-mono text-[11px]">
                  <div>
                    <span className="text-slate-400 dark:text-slate-500 block text-[9px] uppercase font-sans">Tetens Vapor Press.</span>
                    <strong className="text-slate-900 dark:text-slate-100">{physics_metrics.ps_sat_pa} Pa</strong>
                  </div>
                  <div>
                    <span className="text-slate-400 dark:text-slate-500 block text-[9px] uppercase font-sans">WVTR Max Demand</span>
                    <strong className="text-emerald-800 dark:text-emerald-400">{physics_metrics.target_wvtr_req} g/m²/d</strong>
                  </div>
                  <div>
                    <span className="text-slate-400 dark:text-slate-500 block text-[9px] uppercase font-sans">OTR Max Allowable</span>
                    <strong className="text-blue-800 dark:text-blue-400">{physics_metrics.target_otr_req} cc/m²/d</strong>
                  </div>
                  <div>
                    <span className="text-slate-400 dark:text-slate-500 block text-[9px] uppercase font-sans">Barrier Safety Margin</span>
                    <strong className="text-emerald-700 dark:text-emerald-400">{ml_metadata?.safety_factor || 1.8}x</strong>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Navigation Footer */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
        <button
          type="button"
          onClick={onBack}
          className="w-full sm:w-auto px-5 py-3 rounded-xl border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 font-semibold text-sm flex items-center justify-center gap-2 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>{t('back_edit_btn')}</span>
        </button>

        <button
          type="button"
          onClick={onNext}
          className="w-full sm:w-auto bg-emerald-700 hover:bg-emerald-800 text-white font-bold py-3.5 px-6 rounded-xl shadow-md hover:shadow-lg flex items-center justify-center gap-2 transition duration-200 text-sm"
        >
          <span>{t('btn_goto_compliance')}</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
