import React, { useState } from 'react';
import { Package, ShieldCheck, Leaf, ArrowRight, ArrowLeft, ChevronDown, ChevronUp, Cpu, Award, Beaker, Layers, Activity, AlertTriangle } from 'lucide-react';
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
    warning_flag
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
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-emerald-700 uppercase tracking-wider mb-1">
            <Award className="w-4 h-4" />
            <span>{odop_region}</span>
          </div>
          <h2 className="text-2xl font-bold text-slate-900">
            {language === 'hi' ? name_hi : name_en}
          </h2>
          <p className="text-slate-500 text-sm mt-0.5">
            {t('recommendation_subtitle')}
          </p>
        </div>

        {/* ML Credential Tag */}
        {ml_metadata && (
          <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-200 px-3.5 py-2 rounded-xl text-xs font-medium text-emerald-900">
            <Cpu className="w-4 h-4 text-emerald-600" />
            <div>
              <span className="font-bold block">AI Verified Model</span>
              <span className="text-emerald-700">CV Accuracy: {ml_metadata.cross_val_accuracy}</span>
            </div>
          </div>
        )}
      </div>

      {/* Critical Climate / Barrier Advisory Banner */}
      {activeWarning && (
        <div className="bg-amber-50 border-2 border-amber-400 rounded-2xl p-4 flex items-start gap-3 shadow-sm">
          <AlertTriangle className="w-6 h-6 text-amber-600 shrink-0 mt-0.5" />
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <h4 className="text-sm font-bold text-amber-900 uppercase tracking-wide">
                MoFPI Packaging Safety Advisory
              </h4>
              <span className="text-[10px] bg-amber-200 text-amber-900 px-2 py-0.5 rounded font-mono font-bold">
                CRITICAL BARRIER ALERT
              </span>
            </div>
            <p className="text-xs text-amber-800 mt-1 font-medium leading-relaxed">
              {activeWarning}
            </p>
          </div>
        </div>
      )}

      {/* Primary & Alternative Material Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Primary Recommended Material */}
        <div className="bg-gradient-to-br from-emerald-50 via-white to-green-50/50 rounded-2xl border-2 border-emerald-500 p-6 shadow-md relative overflow-hidden flex flex-col justify-between">
          <div className="absolute top-0 right-0 bg-emerald-600 text-white text-[11px] font-bold px-3 py-1 rounded-bl-xl tracking-wide uppercase">
            {t('primary_material_badge')}
          </div>
          <div>
            <div className="w-12 h-12 rounded-xl bg-emerald-600 text-white flex items-center justify-center mb-4 shadow">
              <Package className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 leading-snug">
              {primary_material}
            </h3>
            <p className="text-xs text-slate-500 mt-2">
              Primary multi-layer composite engineered for target shelf life and physical barrier requirements.
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-emerald-100 flex items-center gap-2 text-xs font-semibold text-emerald-800">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>Optimal Barrier & Shelf-Life Match</span>
          </div>
        </div>

        {/* Sustainable / Alternative Material */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between hover:border-slate-300 transition">
          <div>
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 bg-teal-50 border border-teal-200 text-teal-800 rounded-full text-xs font-semibold mb-3">
              <Leaf className="w-3.5 h-3.5 text-teal-600" />
              <span>{t('alt_material_badge')}</span>
            </div>
            <h3 className="text-lg font-bold text-slate-900 leading-snug">
              {alternative_material}
            </h3>
            <p className="text-xs text-slate-500 mt-2">
              Eco-conscious or recyclable substitute meeting circular economy objectives.
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 text-xs text-slate-500">
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
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
        <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-emerald-600" />
          <span>{t('barrier_profile_title')}</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {/* Moisture Gauge */}
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <span className="text-xs font-medium text-slate-600 block">{t('moisture_barrier')}</span>
            <div className="flex items-center gap-1.5">
              {[1, 2, 3, 4, 5].map((idx) => (
                <div
                  key={idx}
                  className={`h-2 flex-1 rounded-full ${
                    idx <= moistureBadge.dots ? 'bg-emerald-500' : 'bg-slate-200'
                  }`}
                />
              ))}
            </div>
            <span className={`inline-block px-2 py-0.5 rounded text-xs font-semibold border ${moistureBadge.bg}`}>
              {moistureBadge.label}
            </span>
          </div>

          {/* Oxygen Gauge */}
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <span className="text-xs font-medium text-slate-600 block">{t('oxygen_barrier')}</span>
            <div className="flex items-center gap-1.5">
              {[1, 2, 3, 4, 5].map((idx) => (
                <div
                  key={idx}
                  className={`h-2 flex-1 rounded-full ${
                    idx <= oxygenBadge.dots ? 'bg-blue-500' : 'bg-slate-200'
                  }`}
                />
              ))}
            </div>
            <span className={`inline-block px-2 py-0.5 rounded text-xs font-semibold border ${oxygenBadge.bg}`}>
              {oxygenBadge.label}
            </span>
          </div>

          {/* Puncture / Mechanical Strength */}
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <span className="text-xs font-medium text-slate-600 block">{t('strength_barrier')}</span>
            <div className="flex items-center gap-1.5">
              {[1, 2, 3, 4, 5].map((idx) => (
                <div
                  key={idx}
                  className={`h-2 flex-1 rounded-full ${
                    idx <= strengthBadge.dots ? 'bg-amber-500' : 'bg-slate-200'
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

      {/* Why This Material (Scientific Rationale Card) */}
      <div className="bg-emerald-900 text-white rounded-2xl p-6 shadow-md space-y-2">
        <h4 className="text-sm font-semibold uppercase tracking-wider text-emerald-300 flex items-center gap-2">
          <Beaker className="w-4 h-4 text-emerald-400" />
          <span>{t('why_title')}</span>
        </h4>
        <p className="text-sm md:text-base leading-relaxed text-emerald-100 font-medium">
          {language === 'hi' ? why_material_hi : why_material_en}
        </p>
      </div>

      {/* Expandable Expert / Scientific Mode Toggle */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden transition">
        <button
          type="button"
          onClick={() => setShowExpertMode(!showExpertMode)}
          className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-slate-50 transition"
        >
          <div className="flex items-center gap-2">
            <Beaker className="w-4 h-4 text-emerald-600" />
            <span className="text-sm font-bold text-slate-800">
              {showExpertMode ? t('expert_toggle_on') : t('expert_toggle_off')}
            </span>
          </div>
          {showExpertMode ? (
            <ChevronUp className="w-5 h-5 text-slate-500" />
          ) : (
            <ChevronDown className="w-5 h-5 text-slate-500" />
          )}
        </button>

        {showExpertMode && (
          <div className="px-6 pb-6 pt-2 border-t border-slate-100 bg-slate-50/50 space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 text-xs">
              <div className="p-3 bg-white rounded-xl border border-slate-200 space-y-1">
                <span className="text-slate-500 font-medium">{t('otr_label')}</span>
                <span className="font-bold text-slate-900 text-sm block">{technical_specs?.otr_range}</span>
                <span className="text-[10px] text-slate-400">Tested per ASTM D3985 / ISO 15105-2 at 23°C</span>
              </div>

              <div className="p-3 bg-white rounded-xl border border-slate-200 space-y-1">
                <span className="text-slate-500 font-medium">{t('wvtr_label')}</span>
                <span className="font-bold text-slate-900 text-sm block">{technical_specs?.wvtr_range}</span>
                <span className="text-[10px] text-slate-400">Tested per ASTM F1249 / ISO 15106 at 38°C/90% RH</span>
              </div>

              <div className="p-3 bg-white rounded-xl border border-slate-200 space-y-1">
                <span className="text-slate-500 font-medium">{t('thickness_label')}</span>
                <span className="font-bold text-slate-900 text-sm block">{technical_specs?.thickness_um} µm</span>
                <span className="text-[10px] text-slate-400">Optimal puncture resistance and sealing caliber</span>
              </div>

              <div className="p-3 bg-white rounded-xl border border-slate-200 space-y-1">
                <span className="text-slate-500 font-medium">{t('map_label')}</span>
                <span className="font-bold text-slate-900 text-sm block">{technical_specs?.map_gas_mix}</span>
                <span className="text-[10px] text-slate-400">Gas equilibrium calculation for headspace</span>
              </div>
            </div>

            {/* Biophysical Formulation Equations Card */}
            {physics_metrics && (
              <div className="p-4 bg-emerald-50/60 rounded-xl border border-emerald-200 text-xs space-y-2">
                <div className="font-bold text-emerald-900 flex items-center gap-1.5">
                  <Activity className="w-4 h-4 text-emerald-700" />
                  <span>Biophysical Barrier Demand Metrics (Governing Equations)</span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-slate-700 font-mono text-[11px]">
                  <div>
                    <span className="text-slate-400 block text-[9px] uppercase font-sans">Tetens Vapor Press.</span>
                    <strong className="text-slate-900">{physics_metrics.ps_sat_pa} Pa</strong>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[9px] uppercase font-sans">WVTR Max Demand</span>
                    <strong className="text-emerald-800">{physics_metrics.target_wvtr_req} g/m²/d</strong>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[9px] uppercase font-sans">OTR Max Allowable</span>
                    <strong className="text-blue-800">{physics_metrics.target_otr_req} cc/m²/d</strong>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[9px] uppercase font-sans">Barrier Safety Margin</span>
                    <strong className="text-emerald-700">{ml_metadata?.safety_factor || 1.8}x</strong>
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
          className="w-full sm:w-auto px-5 py-3 rounded-xl border border-slate-300 text-slate-700 hover:bg-slate-100 font-semibold text-sm flex items-center justify-center gap-2 transition"
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
