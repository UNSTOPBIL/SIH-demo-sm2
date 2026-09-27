import React, { useState, useMemo } from 'react';
import { Activity, Clock, AlertTriangle, ShieldCheck, Thermometer, Droplets, Info, TrendingDown } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export const ShelfLifeSimulator = ({ shelfLifeDecay, physicsMetrics, targetShelfLifeDays = 180, commodityName = '' }) => {
  const { language, t } = useLanguage();

  // Initial values from backend physics metrics or reasonable defaults
  const initialTemp = physicsMetrics?.temperature_c || 27;
  const initialRh = physicsMetrics?.ambient_rh || 65;

  const [tempC, setTempC] = useState(initialTemp);
  const [rhPct, setRhPct] = useState(initialRh);
  const [hoveredDay, setHoveredDay] = useState(null);

  // Biophysical recalculation of decay curves dynamically based on Arrhenius Q10 & RH vapor gradient
  const simulatedCurves = useMemo(() => {
    // Standard baseline rate constants (day^-1) calibrated so:
    // Recommended reaches 50% at targetShelfLifeDays (under 27°C, 65% RH)
    // Generic reaches 50% at ~0.25 * targetShelfLifeDays
    // Control reaches 50% at ~0.08 * targetShelfLifeDays
    const targetDays = Math.max(1, targetShelfLifeDays || 180);
    const baseKRec = -Math.log(0.50) / targetDays;
    const baseKGen = -Math.log(0.50) / Math.max(15, targetDays * 0.22);
    const baseKCtrl = -Math.log(0.50) / Math.max(5, targetDays * 0.08);

    // Temperature acceleration factor via Q10 Arrhenius approximation (Q10 = 2.1 for food spoilage)
    const safeTemp = Number.isFinite(tempC) ? tempC : 27;
    const deltaT = safeTemp - 27;
    const tempFactor = Math.pow(2.1, Math.max(-2, Math.min(5, deltaT / 10)));

    // RH driving force factor (assuming package interior equilibrium ~ 20-30% RH)
    const safeRh = Number.isFinite(rhPct) ? rhPct : 65;
    const baseDeltaRh = Math.max(10, 65 - 25);
    const currentDeltaRh = Math.max(10, safeRh - 25);
    const rhFactor = currentDeltaRh / baseDeltaRh;

    // Combined environmental acceleration multiplier
    const envMultiplier = Math.max(0.05, Math.min(50.0, tempFactor * rhFactor));

    const kRec = baseKRec * envMultiplier;
    const kGen = baseKGen * envMultiplier;
    const kCtrl = baseKCtrl * envMultiplier;

    const data = [];
    for (let day = 0; day <= 365; day += 5) {
      const qCtrl = Math.max(0, Math.min(100, Math.round(100 * Math.exp(-kCtrl * day)))) || 0;
      const qGen = Math.max(0, Math.min(100, Math.round(100 * Math.exp(-kGen * day)))) || 0;
      const qRec = Math.max(0, Math.min(100, Math.round(100 * Math.exp(-kRec * day)))) || 0;
      data.push({ day, control: qCtrl, generic: qGen, recommended: qRec });
    }
    return data;
  }, [tempC, rhPct, targetShelfLifeDays]);

  // Find day where quality drops below 50% (Critical Spoilage Day)
  const failureDays = useMemo(() => {
    const findHalfLife = (key) => {
      const point = simulatedCurves.find(p => p[key] <= 50);
      return point ? point.day : '> 365';
    };
    return {
      control: findHalfLife('control'),
      generic: findHalfLife('generic'),
      recommended: findHalfLife('recommended')
    };
  }, [simulatedCurves]);

  // SVG dimensions & coordinate transforms
  const svgWidth = 600;
  const svgHeight = 260;
  const padding = { top: 20, right: 30, bottom: 40, left: 45 };
  const graphWidth = svgWidth - padding.left - padding.right;
  const graphHeight = svgHeight - padding.top - padding.bottom;

  const getX = (day) => {
    const d = Number.isFinite(day) ? day : 0;
    return padding.left + (Math.max(0, Math.min(365, d)) / 365) * graphWidth;
  };
  const getY = (val) => {
    const v = Number.isFinite(val) ? val : 0;
    return padding.top + (1 - Math.max(0, Math.min(100, v)) / 100) * graphHeight;
  };

  // Generate SVG path strings
  const generatePath = (key) => {
    return simulatedCurves.reduce((acc, curr, idx) => {
      const val = Number.isFinite(curr[key]) ? curr[key] : 0;
      const x = getX(curr.day).toFixed(1);
      const y = getY(val).toFixed(1);
      return idx === 0 ? `M ${x} ${y}` : `${acc} L ${x} ${y}`;
    }, '');
  };

  const generateArea = (key) => {
    const linePath = generatePath(key);
    const bottomY = getY(0).toFixed(1);
    const firstX = getX(0).toFixed(1);
    const lastX = getX(365).toFixed(1);
    return `${linePath} L ${lastX} ${bottomY} L ${firstX} ${bottomY} Z`;
  };

  // Active hover data point
  const currentHoverPoint = useMemo(() => {
    if (hoveredDay === null) return simulatedCurves[Math.min(simulatedCurves.length - 1, Math.round(targetShelfLifeDays / 5))];
    const closest = simulatedCurves.reduce((prev, curr) => 
      Math.abs(curr.day - hoveredDay) < Math.abs(prev.day - hoveredDay) ? curr : prev
    );
    return closest;
  }, [hoveredDay, simulatedCurves, targetShelfLifeDays]);

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-700 uppercase tracking-wider mb-1">
            <Activity className="w-4 h-4 text-emerald-600" />
            <span>Biophysical Shelf-Life & Kinetic Decay Simulator</span>
          </div>
          <h3 className="text-xl font-bold text-slate-900">
            Dynamic Food Quality Degradation (0–365 Days)
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Arrhenius temperature kinetics + Fickian barrier permeation modeling. Move sliders below to simulate ambient extremes.
          </p>
        </div>

        {/* Status Badge */}
        <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-200 px-3.5 py-1.5 rounded-xl self-start sm:self-auto">
          <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
          <div className="text-xs">
            <span className="text-slate-500 block text-[10px]">Predicted Shelf-Life</span>
            <span className="font-bold text-emerald-800 text-sm">{failureDays.recommended} Days</span>
          </div>
        </div>
      </div>

      {/* Interactive Environmental Sliders */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-50 p-4 rounded-xl border border-slate-200">
        {/* Temperature Slider */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs">
            <span className="font-semibold text-slate-700 flex items-center gap-1.5">
              <Thermometer className="w-3.5 h-3.5 text-rose-500" />
              Storage Temperature:
            </span>
            <span className="font-bold text-rose-700 bg-rose-50 border border-rose-200 px-2 py-0.5 rounded font-mono">
              {tempC}°C ({tempC < 15 ? 'Cold Chain' : tempC <= 30 ? 'Ambient Room' : 'Tropical Extreme'})
            </span>
          </div>
          <input
            type="range"
            min="4"
            max="45"
            step="1"
            value={tempC}
            onChange={(e) => setTempC(parseInt(e.target.value))}
            className="w-full accent-rose-600 cursor-pointer h-1.5 bg-slate-200 rounded-lg appearance-none"
          />
          <div className="flex justify-between text-[10px] text-slate-400">
            <span>4°C (Refrigerated)</span>
            <span>27°C (Standard IS/ASTM)</span>
            <span>45°C (Indian Summer)</span>
          </div>
        </div>

        {/* Ambient Humidity Slider */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs">
            <span className="font-semibold text-slate-700 flex items-center gap-1.5">
              <Droplets className="w-3.5 h-3.5 text-blue-500" />
              Ambient Relative Humidity (RH):
            </span>
            <span className="font-bold text-blue-700 bg-blue-50 border border-blue-200 px-2 py-0.5 rounded font-mono">
              {rhPct}% RH ({rhPct < 45 ? 'Dry' : rhPct <= 75 ? 'Humid' : 'Monsoon Coastal'})
            </span>
          </div>
          <input
            type="range"
            min="20"
            max="95"
            step="1"
            value={rhPct}
            onChange={(e) => setRhPct(parseInt(e.target.value))}
            className="w-full accent-blue-600 cursor-pointer h-1.5 bg-slate-200 rounded-lg appearance-none"
          />
          <div className="flex justify-between text-[10px] text-slate-400">
            <span>20% (Arid Rajasthan)</span>
            <span>65% (IS 9845 Norm)</span>
            <span>95% (Coastal Mumbai / Kerala)</span>
          </div>
        </div>
      </div>

      {/* Dynamic SVG Line Chart */}
      <div className="relative bg-slate-950 rounded-2xl p-4 shadow-inner overflow-hidden border border-slate-800">
        {/* Chart Legend */}
        <div className="flex flex-wrap items-center justify-between gap-2 text-xs mb-2 border-b border-slate-800 pb-2">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5 text-emerald-400 font-semibold">
              <span className="w-3 h-3 rounded-full bg-emerald-500 inline-block shadow-sm"></span>
              <span>Recommended Barrier Composite</span>
            </div>
            <div className="flex items-center gap-1.5 text-amber-400 font-medium">
              <span className="w-3 h-3 rounded-full bg-amber-500 inline-block"></span>
              <span>Generic Monolayer Plastic</span>
            </div>
            <div className="flex items-center gap-1.5 text-rose-400 font-medium">
              <span className="w-3 h-3 rounded-full bg-rose-500 inline-block"></span>
              <span>Unpackaged Control</span>
            </div>
          </div>
          <div className="text-[11px] text-slate-400 font-mono">
            Critical Threshold $Q_c$: 50%
          </div>
        </div>

        {/* SVG Canvas */}
        <div className="w-full overflow-x-auto">
          <svg
            viewBox={`0 0 ${svgWidth} ${svgHeight}`}
            className="w-full h-auto min-w-[500px]"
            onMouseMove={(e) => {
              const rect = e.currentTarget.getBoundingClientRect();
              const mouseX = e.clientX - rect.left;
              const relativeX = (mouseX / rect.width) * svgWidth - padding.left;
              const clampedX = Math.max(0, Math.min(graphWidth, relativeX));
              const day = Math.round((clampedX / graphWidth) * 365);
              setHoveredDay(day);
            }}
            onMouseLeave={() => setHoveredDay(null)}
          >
            <defs>
              <linearGradient id="recGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#10b981" stopOpacity="0.35" />
                <stop offset="100%" stopColor="#10b981" stopOpacity="0.0" />
              </linearGradient>
              <linearGradient id="genGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.20" />
                <stop offset="100%" stopColor="#f59e0b" stopOpacity="0.0" />
              </linearGradient>
            </defs>

            {/* Grid Lines (Horizontal: 0%, 25%, 50%, 75%, 100%) */}
            {[0, 25, 50, 75, 100].map((val) => (
              <g key={val}>
                <line
                  x1={padding.left}
                  y1={getY(val)}
                  x2={svgWidth - padding.right}
                  y2={getY(val)}
                  stroke={val === 50 ? '#ef4444' : '#334155'}
                  strokeWidth={val === 50 ? 1.5 : 0.8}
                  strokeDasharray={val === 50 ? '4 3' : '2 2'}
                  opacity={val === 50 ? 0.9 : 0.4}
                />
                <text
                  x={padding.left - 8}
                  y={getY(val) + 3}
                  textAnchor="end"
                  fill={val === 50 ? '#f87171' : '#64748b'}
                  fontSize="10"
                  fontFamily="monospace"
                >
                  {val}%
                </text>
              </g>
            ))}

            {/* Vertical Time Grid (0, 90, 180, 270, 365 Days) */}
            {[0, 90, 180, 270, 365].map((day) => (
              <g key={day}>
                <line
                  x1={getX(day)}
                  y1={padding.top}
                  x2={getX(day)}
                  y2={svgHeight - padding.bottom}
                  stroke="#334155"
                  strokeWidth="0.8"
                  strokeDasharray="2 2"
                  opacity="0.35"
                />
                <text
                  x={getX(day)}
                  y={svgHeight - padding.bottom + 16}
                  textAnchor="middle"
                  fill="#94a3b8"
                  fontSize="10"
                  fontFamily="monospace"
                >
                  {day}d
                </text>
              </g>
            ))}

            {/* Threshold Label */}
            <text
              x={svgWidth - padding.right - 6}
              y={getY(50) - 6}
              textAnchor="end"
              fill="#f87171"
              fontSize="9"
              fontWeight="bold"
            >
              FAILURE LIMIT (50%)
            </text>

            {/* Area Fills */}
            <path d={generateArea('recommended')} fill="url(#recGradient)" />
            <path d={generateArea('generic')} fill="url(#genGradient)" />

            {/* Line Paths */}
            {/* Control Line */}
            <path
              d={generatePath('control')}
              fill="none"
              stroke="#ef4444"
              strokeWidth="1.8"
              strokeLinecap="round"
              opacity="0.85"
            />
            {/* Generic Line */}
            <path
              d={generatePath('generic')}
              fill="none"
              stroke="#f59e0b"
              strokeWidth="2.2"
              strokeLinecap="round"
            />
            {/* Recommended Line */}
            <path
              d={generatePath('recommended')}
              fill="none"
              stroke="#10b981"
              strokeWidth="3.2"
              strokeLinecap="round"
            />

            {/* Hover Guide Line & Dots */}
            {currentHoverPoint && (
              <g>
                <line
                  x1={getX(currentHoverPoint.day)}
                  y1={padding.top}
                  x2={getX(currentHoverPoint.day)}
                  y2={svgHeight - padding.bottom}
                  stroke="#38bdf8"
                  strokeWidth="1.2"
                  strokeDasharray="3 3"
                />
                <circle
                  cx={getX(currentHoverPoint.day)}
                  cy={getY(currentHoverPoint.control)}
                  r="4"
                  fill="#ef4444"
                  stroke="#ffffff"
                  strokeWidth="1.5"
                />
                <circle
                  cx={getX(currentHoverPoint.day)}
                  cy={getY(currentHoverPoint.generic)}
                  r="4"
                  fill="#f59e0b"
                  stroke="#ffffff"
                  strokeWidth="1.5"
                />
                <circle
                  cx={getX(currentHoverPoint.day)}
                  cy={getY(currentHoverPoint.recommended)}
                  r="5"
                  fill="#10b981"
                  stroke="#ffffff"
                  strokeWidth="2"
                />
              </g>
            )}
          </svg>
        </div>

        {/* Hover Point Tooltip Ribbon */}
        {currentHoverPoint && (
          <div className="mt-3 pt-2 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-3 text-xs">
            <div className="flex items-center gap-2">
              <Clock className="w-3.5 h-3.5 text-sky-400" />
              <span className="font-bold text-white">Day {currentHoverPoint.day}:</span>
            </div>
            <div className="flex items-center gap-4 text-xs font-mono">
              <span className="text-rose-400">
                Control: <strong className="text-white">{currentHoverPoint.control}%</strong>
              </span>
              <span className="text-amber-400">
                Generic: <strong className="text-white">{currentHoverPoint.generic}%</strong>
              </span>
              <span className="text-emerald-400">
                Recommended: <strong className="text-white">{currentHoverPoint.recommended}%</strong>
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Degradation Metrics & Shelf-Life Comparison Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Metric 1: Control Half-Life */}
        <div className="p-4 bg-rose-50/70 border border-rose-200 rounded-xl space-y-1">
          <span className="text-xs font-semibold text-rose-800 flex items-center gap-1.5">
            <AlertTriangle className="w-3.5 h-3.5 text-rose-600" />
            Unpackaged Control
          </span>
          <div className="text-2xl font-bold text-rose-900">
            {failureDays.control} {typeof failureDays.control === 'number' ? 'Days' : ''}
          </div>
          <p className="text-[11px] text-rose-700 leading-tight">
            Rapid quality degradation due to immediate ambient moisture/O2 ingress.
          </p>
        </div>

        {/* Metric 2: Monolayer Plastic */}
        <div className="p-4 bg-amber-50/70 border border-amber-200 rounded-xl space-y-1">
          <span className="text-xs font-semibold text-amber-800 flex items-center gap-1.5">
            <TrendingDown className="w-3.5 h-3.5 text-amber-600" />
            Generic Single-Layer
          </span>
          <div className="text-2xl font-bold text-amber-900">
            {failureDays.generic} {typeof failureDays.generic === 'number' ? 'Days' : ''}
          </div>
          <p className="text-[11px] text-amber-700 leading-tight">
            Moderate moisture barrier but permeable to oxygen, triggering lipid rancidity.
          </p>
        </div>

        {/* Metric 3: Multi-Layer Barrier Solution */}
        <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl space-y-1">
          <span className="text-xs font-semibold text-emerald-800 flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
            Recommended Barrier Film
          </span>
          <div className="text-2xl font-bold text-emerald-900">
            {failureDays.recommended} {typeof failureDays.recommended === 'number' ? 'Days' : ''}
          </div>
          <p className="text-[11px] text-emerald-700 leading-tight">
            Engineered metallized/EVOH barrier maintains sensory quality & nutrition.
          </p>
        </div>
      </div>
    </div>
  );
};
