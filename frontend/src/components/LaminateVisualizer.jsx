import React, { useState } from 'react';
import { Layers, Shield, Sparkles, CheckCircle2, Info, ChevronRight } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export const LaminateVisualizer = ({ primaryStructure, altStructure, safetyFactor }) => {
  const { language } = useLanguage();
  const [selectedLayerIndex, setSelectedLayerIndex] = useState(0);
  const [activeTab, setActiveTab] = useState('primary'); // 'primary' | 'alternative'

  const currentStructure = activeTab === 'primary' ? primaryStructure : (altStructure || primaryStructure);
  const layers = currentStructure?.layers || [];
  const totalThickness = currentStructure?.total_thickness_um || 70;

  const activeLayer = layers[selectedLayerIndex] || layers[0] || {};

  const getLayerStyle = (layer) => {
    const name = (layer.name || '').toLowerCase();
    const type = (layer.layer_type || '').toLowerCase();

    // Metallized film or Aluminum Foil (Metallic Sheen)
    if (name.includes('foil') || name.includes('met') || name.includes('alu') || name.includes('al-')) {
      return {
        background: 'linear-gradient(135deg, #475569 0%, #94a3b8 20%, #f1f5f9 45%, #cbd5e1 60%, #64748b 85%, #334155 100%)',
        textColor: 'text-slate-900',
        badgeBg: 'bg-slate-950/80 text-white',
        border: 'border-slate-300',
        badgeLabel: 'METALLIC BARRIER'
      };
    }
    // EVOH / Specialty gas barrier
    if (name.includes('evoh') || name.includes('nylon') || name.includes('pa')) {
      return {
        background: 'linear-gradient(135deg, rgba(139, 92, 246, 0.95) 0%, rgba(167, 139, 250, 0.85) 45%, rgba(109, 40, 217, 0.95) 100%)',
        textColor: 'text-white',
        badgeBg: 'bg-purple-950/70 text-purple-200',
        border: 'border-purple-300/40',
        badgeLabel: 'GAS CORE'
      };
    }
    // Paper / Kraft / Cellulose
    if (name.includes('paper') || name.includes('kraft') || name.includes('pla')) {
      return {
        background: 'linear-gradient(135deg, #b45309 0%, #d97706 40%, #f59e0b 65%, #92400e 100%)',
        textColor: 'text-amber-950',
        badgeBg: 'bg-amber-950/80 text-amber-100',
        border: 'border-amber-300/40',
        badgeLabel: 'BIO KRAFT'
      };
    }
    // Sealant / Translucent Polyethylene: LDPE / LLDPE / HDPE
    if (name.includes('pe') || name.includes('polyethylene') || type === 'sealant') {
      return {
        background: 'linear-gradient(135deg, rgba(248, 250, 252, 0.95) 0%, rgba(226, 232, 240, 0.85) 45%, rgba(203, 213, 225, 0.92) 100%)',
        textColor: 'text-slate-800',
        badgeBg: 'bg-slate-800/80 text-white',
        border: 'border-slate-300/60',
        badgeLabel: 'FOOD SEALANT'
      };
    }
    // Clear gloss films: BOPP / PET / Polyester
    return {
      background: 'linear-gradient(135deg, rgba(14, 165, 233, 0.9) 0%, rgba(56, 189, 248, 0.75) 40%, rgba(2, 132, 199, 0.95) 100%)',
      textColor: 'text-white',
      badgeBg: 'bg-sky-950/70 text-sky-200',
      border: 'border-sky-300/40',
      badgeLabel: 'CLEAR WEB'
    };
  };

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-6 transition-colors duration-200">
      {/* Header with Tab Switcher */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 dark:border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider mb-1">
            <Layers className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            <span>Interactive Laminate Cross-Section Explorer</span>
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white">
            {currentStructure?.name || "Multi-Layer Composite Film"}
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Total Film Caliper: <span className="font-bold text-slate-800 dark:text-slate-200">{totalThickness} µm</span> · Barrier Safety Margin: <span className="font-bold text-emerald-700 dark:text-emerald-400">{safetyFactor || 1.8}x</span>
          </p>
        </div>

        {/* Tab Buttons */}
        <div className="flex items-center bg-slate-100 dark:bg-slate-800 p-1 rounded-xl self-start sm:self-auto text-xs font-semibold">
          <button
            type="button"
            onClick={() => { setActiveTab('primary'); setSelectedLayerIndex(0); }}
            className={`px-3 py-1.5 rounded-lg transition ${
              activeTab === 'primary'
                ? 'bg-white dark:bg-slate-700 text-emerald-800 dark:text-emerald-300 shadow-xs font-bold'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            Primary Recommended
          </button>
          {altStructure && (
            <button
              type="button"
              onClick={() => { setActiveTab('alternative'); setSelectedLayerIndex(0); }}
              className={`px-3 py-1.5 rounded-lg transition ${
                activeTab === 'alternative'
                  ? 'bg-white dark:bg-slate-700 text-teal-800 dark:text-teal-300 shadow-xs font-bold'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
              }`}
            >
              Eco / Alternative
            </button>
          )}
        </div>
      </div>

      {/* Visual 2.5D Layer Stack Representation */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        {/* Left Side: 2.5D Cross-Section Film Stack */}
        <div className="lg:col-span-6 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 rounded-2xl p-6 text-white shadow-xl flex flex-col justify-center space-y-4 border border-slate-800">
          <div className="flex justify-between items-center text-[11px] text-slate-400 border-b border-slate-700/60 pb-2 font-mono">
            <span>PACKAGING EXTERIOR (ENVIRONMENT)</span>
            <span>PRINT WEB</span>
          </div>

          {/* Interactive Layer Slabs */}
          <div className="space-y-3 py-2">
            {layers.map((layer, idx) => {
              const isSelected = idx === selectedLayerIndex;
              const heightPx = Math.max(40, Math.min(72, Math.round((layer.thickness_um / totalThickness) * 160)));
              const style = getLayerStyle(layer);

              return (
                <div
                  key={idx}
                  onClick={() => setSelectedLayerIndex(idx)}
                  className={`group relative rounded-xl p-3 cursor-pointer transition-all duration-200 transform overflow-hidden ${
                    isSelected
                      ? 'ring-2 ring-emerald-400 shadow-lg shadow-emerald-950/40 scale-[1.02] border-white'
                      : 'border-slate-700 hover:border-slate-400 opacity-90 hover:opacity-100'
                  }`}
                  style={{
                    background: style.background,
                    height: `${heightPx}px`,
                    boxShadow: isSelected 
                      ? '0 10px 25px -5px rgba(0, 0, 0, 0.4), inset 0 1px 2px rgba(255, 255, 255, 0.4)' 
                      : '0 4px 6px -1px rgba(0, 0, 0, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.2)'
                  }}
                >
                  {/* Subtle Diagonal Gloss Reflection across layer */}
                  <div className="absolute inset-0 pointer-events-none opacity-40 bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12" />

                  <div className={`flex items-center justify-between drop-shadow-sm h-full relative z-10 ${style.textColor}`}>
                    <div className="flex items-center gap-2.5 font-bold text-xs md:text-sm">
                      <span className="w-5 h-5 rounded-full bg-black/40 text-white flex items-center justify-center text-[10px] font-mono shadow-xs">
                        {idx + 1}
                      </span>
                      <span className="tracking-tight">{layer.short_name || layer.name}</span>
                    </div>

                    <div className="flex items-center gap-2 text-xs">
                      <span className={`${style.badgeBg} px-2 py-0.5 rounded text-[11px] font-mono font-bold shadow-xs`}>
                        {layer.thickness_um} µm
                      </span>
                      <ChevronRight className={`w-4 h-4 transition ${isSelected ? 'text-emerald-500 scale-125' : 'text-slate-400'}`} />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="flex justify-between items-center text-[11px] text-emerald-400 border-t border-slate-700/60 pt-2 font-medium font-mono">
            <span>FOOD CONTACT INTERIOR (SEALED)</span>
            <span>IS 10146 COMPLIANT</span>
          </div>
        </div>

        {/* Right Side: Selected Layer Detailed Inspector */}
        <div className="lg:col-span-6 bg-slate-50 dark:bg-slate-800/70 rounded-2xl border border-slate-200 dark:border-slate-700 p-5 space-y-4">
          <div className="flex items-center justify-between">
            <span className="px-2.5 py-1 bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800 rounded-lg text-xs font-bold uppercase tracking-wider">
              Layer {selectedLayerIndex + 1} of {layers.length} · {activeLayer.layer_type?.toUpperCase()}
            </span>
            <span className="text-xs font-mono font-bold text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 px-2 py-1 rounded border border-slate-200 dark:border-slate-700">
              {activeLayer.thickness_um} µm ({Math.round(((activeLayer.thickness_um || 1) / totalThickness) * 100)}% of film)
            </span>
          </div>

          <div>
            <h4 className="text-base font-bold text-slate-900 dark:text-white">
              {activeLayer.name}
            </h4>
            <p className="text-xs text-slate-600 dark:text-slate-300 mt-2 leading-relaxed">
              {language === 'hi' ? activeLayer.role_hi : activeLayer.role_en}
            </p>
          </div>

          {/* Caliper Gauge Progress Bar */}
          <div className="p-3 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1.5">
            <div className="flex justify-between text-xs font-medium text-slate-500 dark:text-slate-400">
              <span>Layer Caliper Contribution</span>
              <span className="font-bold text-slate-800 dark:text-slate-200 font-mono">
                {activeLayer.thickness_um} µm / {totalThickness} µm
              </span>
            </div>
            <div className="h-2 w-full bg-slate-100 dark:bg-slate-700 rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-emerald-500 to-teal-400 rounded-full transition-all duration-300"
                style={{ width: `${Math.round(((activeLayer.thickness_um || 1) / totalThickness) * 100)}%` }}
              />
            </div>
          </div>

          <div className="pt-2 border-t border-slate-200/80 dark:border-slate-700/80 space-y-2 text-xs">
            <div className="flex items-center justify-between">
              <span className="text-slate-500 dark:text-slate-400 font-medium">Statutory / ASTM Standard:</span>
              <span className="font-bold text-slate-800 dark:text-slate-200 bg-white dark:bg-slate-800 px-2 py-0.5 rounded border border-slate-200 dark:border-slate-700">
                {activeLayer.standards || "ASTM D3985 / IS 10146:2021"}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-500 dark:text-slate-400 font-medium">FSSAI / BIS Role:</span>
              <span className="font-semibold text-emerald-800 dark:text-emerald-400">
                {activeLayer.layer_type === 'sealant'
                  ? "Direct Food Contact Layer (Overall Migration <= 60 mg/kg)"
                  : activeLayer.layer_type === 'barrier'
                  ? "Atmospheric Vapor & Light Attenuation Core"
                  : "Outer Web Mechanical & Scuff Protection"}
              </span>
            </div>
          </div>

          {/* Quick Selection Pills */}
          <div className="pt-3 border-t border-slate-200 dark:border-slate-700 flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400">
            <span className="font-medium mr-1">Inspect:</span>
            {layers.map((l, i) => (
              <button
                key={i}
                type="button"
                onClick={() => setSelectedLayerIndex(i)}
                className={`px-2 py-0.5 rounded text-[11px] font-semibold transition ${
                  i === selectedLayerIndex
                    ? 'bg-emerald-700 text-white'
                    : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-700'
                }`}
              >
                L{i + 1}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
