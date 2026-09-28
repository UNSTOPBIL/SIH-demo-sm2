import React from 'react';
import { FlaskConical, Scale, CheckCircle2, AlertCircle, Info, Clock, Thermometer } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export const SimulantProtocolCard = ({ simulantProtocol, commodityName = '' }) => {
  const { language, t } = useLanguage();

  if (!simulantProtocol) return null;

  const {
    standard = "IS 9845 : 1998 (Reaffirmed 2014)",
    title = "Determination of Overall Migration of Constituents of Plastics Materials",
    food_classification = "General Food Contact",
    statutory_limit_mg_dm2 = 10.0,
    statutory_limit_mg_kg = 60.0,
    primary_simulant = "Simulant A",
    simulants = [],
    analytical_method = "Gravimetric residue evaporation of simulant leachate per IS 9845 Annex A"
  } = simulantProtocol;

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-100 dark:border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-amber-700 dark:text-amber-400 uppercase tracking-wider mb-1">
            <FlaskConical className="w-4 h-4 text-amber-600 dark:text-amber-400" />
            <span>NABL Certified Laboratory Protocol · FSSAI Mandate</span>
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white">
            {standard}
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            {title}
          </p>
        </div>

        {/* Limits Badge */}
        <div className="flex items-center gap-3 bg-amber-50/80 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 p-3 rounded-xl self-start md:self-auto">
          <Scale className="w-5 h-5 text-amber-700 dark:text-amber-400 shrink-0" />
          <div className="text-xs">
            <span className="text-slate-500 dark:text-slate-400 block text-[10px] uppercase font-bold">Overall Migration Limit (OML)</span>
            <span className="font-extrabold text-amber-900 dark:text-amber-300 text-sm">
              ≤ {statutory_limit_mg_dm2} mg/dm² <span className="text-slate-500 dark:text-slate-400 font-normal">or</span> ≤ {statutory_limit_mg_kg} mg/kg
            </span>
          </div>
        </div>
      </div>

      {/* Commodity Classification Strip */}
      <div className="bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 p-3.5 rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
        <div>
          <span className="text-slate-500 dark:text-slate-400 font-medium">Assigned IS 9845 Food Classification: </span>
          <span className="font-bold text-slate-900 dark:text-white">{food_classification}</span>
        </div>
        <div className="flex items-center gap-1.5 text-emerald-800 dark:text-emerald-300 font-semibold bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800 px-2.5 py-1 rounded-lg">
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
          <span>Designated Primary: {primary_simulant}</span>
        </div>
      </div>

      {/* Simulants Matrix Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {simulants.map((sim, idx) => {
          const isPrimary = sim.applicable;
          return (
            <div
              key={idx}
              className={`p-4 rounded-xl border transition duration-200 flex flex-col justify-between ${
                isPrimary
                  ? 'bg-amber-50/50 dark:bg-amber-950/30 border-amber-300 dark:border-amber-700 ring-2 ring-amber-200/60 dark:ring-amber-900/40 shadow-xs'
                  : 'bg-white dark:bg-slate-800/50 border-slate-200 dark:border-slate-700 opacity-75 hover:opacity-100'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className={`w-6 h-6 rounded-lg flex items-center justify-center font-bold text-xs ${
                      isPrimary ? 'bg-amber-600 text-white' : 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300'
                    }`}>
                      {sim.code.replace('Simulant ', '')}
                    </span>
                    <span className="font-bold text-slate-900 dark:text-white text-sm">{sim.code}</span>
                  </div>
                  <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${
                    isPrimary
                      ? 'bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800'
                      : 'bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400'
                  }`}>
                    {isPrimary ? 'Mandatory Contact' : 'Reference Only'}
                  </span>
                </div>

                <div className="space-y-1.5 text-xs text-slate-700 dark:text-slate-300">
                  <div className="font-medium text-slate-900 dark:text-white">
                    {sim.name}
                  </div>
                  <div className="text-[11px] text-slate-500 dark:text-slate-400">
                    <strong>Applicability:</strong> {sim.target_food}
                  </div>
                </div>
              </div>

              <div className="mt-3 pt-2.5 border-t border-slate-200/80 dark:border-slate-700/80 flex items-center justify-between text-[11px] text-slate-600 dark:text-slate-300 font-mono">
                <span className="flex items-center gap-1">
                  <Clock className="w-3 h-3 text-slate-400" />
                  {sim.condition}
                </span>
                <span className="font-bold text-slate-800 dark:text-slate-200">Limit: ≤ 60 ppm</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Analytical Protocol & Extraction Method */}
      <div className="bg-slate-900 text-slate-200 p-4 rounded-xl text-xs space-y-2 border border-slate-800">
        <div className="flex items-center gap-2 font-bold text-emerald-400">
          <Info className="w-4 h-4" />
          <span>Statutory Testing Methodology (IS 9845:1998 Annex A)</span>
        </div>
        <p className="text-slate-300 text-[11px] leading-relaxed">
          {analytical_method}. Total exposed surface area $A \ge 1\text{ dm}^2$ per $100\text{ ml}$ of simulant. Test specimen must be completely immersed in conditioned simulant within sealed borosilicate cell. Residue calculated after drying to constant weight at $105^\circ\text{C} \pm 2^\circ\text{C}$.
        </p>
      </div>
    </div>
  );
};
