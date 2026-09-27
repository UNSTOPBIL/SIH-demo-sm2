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

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6">
      {/* Header with Tab Switcher */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-700 uppercase tracking-wider mb-1">
            <Layers className="w-4 h-4 text-emerald-600" />
            <span>Interactive Laminate Cross-Section Explorer</span>
          </div>
          <h3 className="text-xl font-bold text-slate-900">
            {currentStructure?.name || "Multi-Layer Composite Film"}
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Total Film Caliper: <span className="font-bold text-slate-800">{totalThickness} µm</span> · Barrier Safety Margin: <span className="font-bold text-emerald-700">{safetyFactor || 1.8}x</span>
          </p>
        </div>

        {/* Tab Buttons */}
        <div className="flex items-center bg-slate-100 p-1 rounded-xl self-start sm:self-auto text-xs font-semibold">
          <button
            type="button"
            onClick={() => { setActiveTab('primary'); setSelectedLayerIndex(0); }}
            className={`px-3 py-1.5 rounded-lg transition ${
              activeTab === 'primary'
                ? 'bg-white text-emerald-800 shadow-xs font-bold'
                : 'text-slate-600 hover:text-slate-900'
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
                  ? 'bg-white text-teal-800 shadow-xs font-bold'
                  : 'text-slate-600 hover:text-slate-900'
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
        <div className="lg:col-span-6 bg-gradient-to-b from-slate-900 via-slate-850 to-slate-900 rounded-2xl p-6 text-white shadow-inner flex flex-col justify-center space-y-4">
          <div className="flex justify-between items-center text-[11px] text-slate-400 border-b border-slate-700/60 pb-2">
            <span>PACKAGING EXTERIOR (ENVIRONMENT)</span>
            <span>PRINT WEB</span>
          </div>

          {/* Interactive Layer Slabs */}
          <div className="space-y-2.5 py-2">
            {layers.map((layer, idx) => {
              const isSelected = idx === selectedLayerIndex;
              const heightPx = Math.max(36, Math.min(68, Math.round((layer.thickness_um / totalThickness) * 160)));

              return (
                <div
                  key={idx}
                  onClick={() => setSelectedLayerIndex(idx)}
                  className={`group relative rounded-xl p-3 cursor-pointer transition-all duration-200 transform border ${
                    isSelected
                      ? 'ring-2 ring-emerald-400 border-white shadow-lg scale-[1.02]'
                      : 'border-slate-700 hover:border-slate-500 opacity-85 hover:opacity-100'
                  }`}
                  style={{
                    backgroundColor: layer.color || '#475569',
                    height: `${heightPx}px`
                  }}
                >
                  <div className="flex items-center justify-between text-white drop-shadow-sm h-full">
                    <div className="flex items-center gap-2 font-bold text-xs md:text-sm">
                      <span className="w-5 h-5 rounded-full bg-black/30 flex items-center justify-center text-[10px]">
                        {idx + 1}
                      </span>
                      <span>{layer.short_name || layer.name}</span>
                    </div>
                    <div className="flex items-center gap-2 text-xs">
                      <span className="bg-black/35 px-2 py-0.5 rounded text-[11px] font-mono">
                        {layer.thickness_um} µm
                      </span>
                      <ChevronRight className={`w-4 h-4 transition ${isSelected ? 'text-emerald-300' : 'text-white/50'}`} />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="flex justify-between items-center text-[11px] text-emerald-400 border-t border-slate-700/60 pt-2 font-medium">
            <span>FOOD CONTACT INTERIOR (SEALED)</span>
            <span>IS 10146 COMPLIANT</span>
          </div>
        </div>

        {/* Right Side: Selected Layer Detailed Inspector */}
        <div className="lg:col-span-6 bg-slate-50 rounded-2xl border border-slate-200 p-5 space-y-4">
          <div className="flex items-center justify-between">
            <span className="px-2.5 py-1 bg-emerald-100 text-emerald-800 rounded-lg text-xs font-bold uppercase tracking-wider">
              Layer {selectedLayerIndex + 1} of {layers.length} · {activeLayer.layer_type?.toUpperCase()}
            </span>
            <span className="text-xs font-mono font-bold text-slate-700 bg-white px-2 py-1 rounded border border-slate-200">
              {activeLayer.thickness_um} µm ({Math.round(((activeLayer.thickness_um || 1) / totalThickness) * 100)}% of film)
            </span>
          </div>

          <div>
            <h4 className="text-base font-bold text-slate-900">
              {activeLayer.name}
            </h4>
            <p className="text-xs text-slate-600 mt-2 leading-relaxed">
              {language === 'hi' ? activeLayer.role_hi : activeLayer.role_en}
            </p>
          </div>

          <div className="pt-2 border-t border-slate-200/80 space-y-2 text-xs">
            <div className="flex items-center justify-between">
              <span className="text-slate-500 font-medium">Statutory / ASTM Standard:</span>
              <span className="font-bold text-slate-800 bg-white px-2 py-0.5 rounded border border-slate-200">
                {activeLayer.standards || "ASTM D3985 / IS 10146:2021"}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-500 font-medium">FSSAI / BIS Role:</span>
              <span className="font-semibold text-emerald-800">
                {activeLayer.layer_type === 'sealant'
                  ? "Direct Food Contact Layer (Overall Migration <= 60 mg/kg)"
                  : activeLayer.layer_type === 'barrier'
                  ? "Atmospheric Vapor & Light Attenuation Core"
                  : "Outer Web Mechanical & Scuff Protection"}
              </span>
            </div>
          </div>

          {/* Quick Selection Pills */}
          <div className="pt-3 border-t border-slate-200 flex items-center gap-1.5 text-xs text-slate-500">
            <span className="font-medium mr-1">Inspect:</span>
            {layers.map((l, i) => (
              <button
                key={i}
                type="button"
                onClick={() => setSelectedLayerIndex(i)}
                className={`px-2 py-0.5 rounded text-[11px] font-semibold transition ${
                  i === selectedLayerIndex
                    ? 'bg-emerald-700 text-white'
                    : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-100'
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
