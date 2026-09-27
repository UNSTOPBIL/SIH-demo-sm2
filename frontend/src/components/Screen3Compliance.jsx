import React, { useState } from 'react';
import { ShieldCheck, Scale, FileText, CheckSquare, Square, AlertTriangle, ArrowRight, ArrowLeft, Building2, CheckCircle2 } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { SimulantProtocolCard } from './SimulantProtocolCard';
import { LabelMockupPreview } from './LabelMockupPreview';

export const Screen3Compliance = ({ complianceData, onNext, onBack }) => {
  const { language, t } = useLanguage();

  // Interactive Checklist state
  const [checklist, setChecklist] = useState([
    { id: 'fssai_logo', key: 'label_fssai_logo', checked: true },
    { id: 'veg_mark', key: 'label_veg_mark', checked: true },
    { id: 'net_quantity', key: 'label_net_quantity', checked: true },
    { id: 'mrp', key: 'label_mrp', checked: true },
    { id: 'batch_no', key: 'label_batch_no', checked: true },
    { id: 'dates', key: 'label_dates', checked: true },
    { id: 'ingredients', key: 'label_ingredients', checked: true },
    { id: 'nutrition', key: 'label_nutrition', checked: true },
    { id: 'consumer_care', key: 'label_consumer_care', checked: true },
  ]);

  if (!complianceData) return null;

  const {
    commodity_name_en,
    commodity_name_hi,
    odop_region,
    primary_material,
    fssai,
    bis,
    migration,
    epr,
    nabl
  } = complianceData;

  const toggleCheck = (id) => {
    setChecklist(prev =>
      prev.map(item => item.id === id ? { ...item, checked: !item.checked } : item)
    );
  };

  const allChecked = checklist.every(c => c.checked);

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Hero Banner for Statutory Shield */}
      <div className="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-blue-800/80 rounded-xl border border-blue-600">
            <Scale className="w-6 h-6 text-blue-300" />
          </div>
          <div>
            <div className="text-xs font-semibold uppercase tracking-wider text-blue-300">
              India Regulatory Defense Layer · MoFPI Mandate
            </div>
            <h2 className="text-2xl font-bold tracking-tight">
              {t('compliance_title')}
            </h2>
            <p className="text-blue-200 text-xs mt-0.5">
              {t('compliance_subtitle')}
            </p>
          </div>
        </div>
      </div>

      {/* 4 Pillars Statutory Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Pillar 1: FSSAI Packaging Regulations */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
          <div className="flex items-center gap-2.5 text-emerald-800">
            <Building2 className="w-5 h-5 text-emerald-600" />
            <h3 className="font-bold text-base text-slate-900">{t('fssai_card_title')}</h3>
          </div>
          <div className="space-y-2 text-xs">
            <div className="p-2.5 bg-emerald-50/70 rounded-lg border border-emerald-200">
              <span className="font-semibold text-emerald-900 block">{t('fssai_sched_iv')}:</span>
              <span className="text-emerald-800 font-medium">{fssai?.schedule_iv_category}</span>
            </div>
            <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200">
              <span className="font-semibold text-slate-700 block">{t('fssai_sched_iii')}:</span>
              <span className="text-slate-800">{fssai?.material_schedule}</span>
            </div>
          </div>
        </div>

        {/* Pillar 2: Bureau of Indian Standards (BIS) */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
          <div className="flex items-center gap-2.5 text-blue-800">
            <ShieldCheck className="w-5 h-5 text-blue-600" />
            <h3 className="font-bold text-base text-slate-900">{t('bis_card_title')}</h3>
          </div>
          <div className="space-y-2 text-xs">
            <div className="p-2.5 bg-blue-50/70 rounded-lg border border-blue-200">
              <span className="font-semibold text-blue-900 block">{t('bis_code_label')}:</span>
              <span className="text-blue-800 font-bold text-sm">{bis?.is_code}</span>
            </div>
            <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200">
              <span className="font-semibold text-slate-700 block">Conformity Scope:</span>
              <span className="text-slate-800">{bis?.title}</span>
            </div>
          </div>
        </div>

        {/* Pillar 3: Overall Migration Limit (IS 9845) */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
          <div className="flex items-center gap-2.5 text-amber-800">
            <Scale className="w-5 h-5 text-amber-600" />
            <h3 className="font-bold text-base text-slate-900">{t('migration_card_title')}</h3>
          </div>
          <div className="space-y-2 text-xs">
            <div className="p-2.5 bg-amber-50/80 rounded-lg border border-amber-200">
              <span className="font-semibold text-amber-900 block">Statutory Migration Ceiling:</span>
              <span className="text-amber-800 font-bold text-sm">{migration?.overall_migration_limit}</span>
            </div>
            <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200 text-slate-600 text-[11px] leading-relaxed">
              {migration?.simulants_prescribed}
            </div>
          </div>
        </div>

        {/* Pillar 4: CPCB EPR Plastic Waste Category */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
          <div className="flex items-center gap-2.5 text-purple-800">
            <FileText className="w-5 h-5 text-purple-600" />
            <h3 className="font-bold text-base text-slate-900">{t('epr_card_title')}</h3>
          </div>
          <div className="space-y-2 text-xs">
            <div className="p-2.5 bg-purple-50/80 rounded-lg border border-purple-200">
              <span className="font-semibold text-purple-900 block">{t('epr_category_label')}:</span>
              <span className="text-purple-800 font-bold text-sm">{epr?.category}</span>
            </div>
            <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200 text-slate-600 text-[11px] leading-relaxed">
              {epr?.registration_portal} — {epr?.target_obligation}
            </div>
          </div>
        </div>
      </div>

      {/* IS 9845 Statutory Migration Simulants Matrix Protocol */}
      <SimulantProtocolCard
        simulantProtocol={complianceData.simulant_protocol || complianceData.migration?.simulant_matrix}
        commodityName={commodity_name_en}
      />

      {/* Interactive FSSAI 2020 Labelling Checklist */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
          <div>
            <h3 className="font-bold text-base text-slate-900 flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-600" />
              <span>{t('labelling_title')}</span>
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              {t('labelling_subtitle')}
            </p>
          </div>
          <span className="px-2.5 py-1 bg-emerald-100 text-emerald-800 rounded-full text-xs font-bold self-start sm:self-auto">
            {checklist.filter(c => c.checked).length} / {checklist.length} Mandatory Checks
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5 pt-1">
          {checklist.map((item) => (
            <button
              key={item.id}
              type="button"
              onClick={() => toggleCheck(item.id)}
              className={`flex items-start gap-3 p-3 rounded-xl border text-left text-xs transition duration-150 ${
                item.checked
                  ? 'bg-emerald-50/50 border-emerald-300 text-slate-800'
                  : 'bg-slate-50 border-slate-200 text-slate-500'
              }`}
            >
              {item.checked ? (
                <CheckSquare className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              ) : (
                <Square className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
              )}
              <span className={`font-medium ${item.checked ? 'text-slate-900' : 'text-slate-500'}`}>
                {t(item.key)}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Photorealistic FMCG Back-of-Pack Mockup */}
      <LabelMockupPreview
        commodity={{
          name_en: commodity_name_en,
          name_hi: commodity_name_hi,
          odop_region: odop_region,
          moisture_pct: complianceData.moisture_pct,
          fat_oil_pct: complianceData.fat_oil_pct
        }}
        primaryMaterial={primary_material}
        complianceData={complianceData}
      />

      {/* NABL Advisory Note */}
      <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 flex items-start gap-3 text-amber-900 text-xs leading-relaxed">
        <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold block text-sm mb-0.5">{t('nabl_title')}</span>
          {t('nabl_body')}
        </div>
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
          <span>{t('btn_goto_sheet')}</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
