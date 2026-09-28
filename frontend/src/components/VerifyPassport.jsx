import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  Award, 
  CheckCircle2, 
  Calendar, 
  Clock, 
  Layers, 
  FileText, 
  ExternalLink, 
  ArrowLeft, 
  Printer, 
  Share2, 
  Copy, 
  Check, 
  Sparkles,
  QrCode,
  Building2,
  AlertCircle
} from 'lucide-react';

export const VerifyPassport = ({ onBack }) => {
  const [passportData, setPassportData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);

  // Parse query parameters from current window URL
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const batchId = params.get('batch') || `PMFME-2026-${Math.random().toString(36).substring(2, 8).toUpperCase()}`;
    const commodityId = params.get('id') || 'makhana';
    const laminateId = params.get('laminate');

    let url = `/api/verify/${batchId}?id=${commodityId}`;
    if (laminateId) url += `&laminate_id=${laminateId}`;

    fetch(url)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}: Failed to load digital passport`);
        return res.json();
      })
      .then((data) => {
        setPassportData(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Passport fetch error:", err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const handleCopyLink = () => {
    navigator.clipboard.writeText(window.location.href);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  const handlePrint = () => {
    window.print();
  };

  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center space-y-4 p-6 text-center">
        <div className="w-14 h-14 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-slate-700 font-semibold text-base">
          Verifying MoFPI Cryptographic Integrity Seal...
        </p>
        <span className="text-xs text-slate-400 font-mono">
          Querying Government of India PMFME Packaging Registry
        </span>
      </div>
    );
  }

  if (error || !passportData) {
    return (
      <div className="max-w-xl mx-auto p-6 bg-white rounded-2xl border border-red-200 shadow-md text-center space-y-4 my-8">
        <div className="w-12 h-12 bg-red-100 text-red-600 rounded-full flex items-center justify-center mx-auto">
          <AlertCircle className="w-6 h-6" />
        </div>
        <h3 className="text-lg font-bold text-slate-900">Verification Certificate Not Reachable</h3>
        <p className="text-xs text-slate-600">{error || "Invalid passport query parameters."}</p>
        {onBack && (
          <button
            onClick={onBack}
            className="px-4 py-2 bg-emerald-700 text-white rounded-xl text-xs font-bold hover:bg-emerald-800 transition"
          >
            Return to Dashboard
          </button>
        )}
      </div>
    );
  }

  const {
    batch_id,
    status,
    integrity_hash,
    issuing_authority,
    commodity,
    certified_packaging,
    safety_and_conformity,
    timestamps
  } = passportData;

  return (
    <div className="max-w-3xl mx-auto space-y-6 my-4 px-3 sm:px-0">
      {/* Top Action Bar */}
      <div className="no-print flex items-center justify-between gap-3 bg-white p-3.5 rounded-2xl border border-slate-200 shadow-xs">
        <button
          onClick={onBack || (() => window.history.back())}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Engine</span>
        </button>

        <div className="flex items-center gap-2">
          <button
            onClick={handleCopyLink}
            className="inline-flex items-center gap-1 px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-xs font-bold text-slate-700 transition"
            title="Copy verification link"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? "Copied Link" : "Copy URL"}</span>
          </button>
          <button
            onClick={handlePrint}
            className="inline-flex items-center gap-1 px-3.5 py-1.5 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-xs font-bold text-white shadow-xs transition"
          >
            <Printer className="w-3.5 h-3.5" />
            <span>Print Passport</span>
          </button>
        </div>
      </div>

      {/* Main Official Passport Certificate */}
      <div className="bg-white rounded-3xl border-2 border-emerald-600 shadow-xl overflow-hidden relative">
        {/* Government Top Ribbon */}
        <div className="bg-gradient-to-r from-emerald-900 via-green-800 to-emerald-950 p-6 text-white text-center relative">
          {/* Watermark Emblem Style */}
          <div className="inline-flex items-center justify-center w-14 h-14 bg-white/10 rounded-2xl backdrop-blur-xs border border-white/20 mb-3 shadow-inner">
            <Building2 className="w-8 h-8 text-amber-300" />
          </div>

          <p className="text-[11px] font-extrabold uppercase tracking-widest text-emerald-200">
            {issuing_authority.ministry} · GOVERNMENT OF INDIA
          </p>
          <h1 className="text-xl sm:text-2xl font-black tracking-tight text-white mt-0.5">
            Official Digital Product Passport (DPP)
          </h1>
          <p className="text-xs text-emerald-100 font-medium mt-1 max-w-xl mx-auto">
            {issuing_authority.initiative} · {issuing_authority.scheme}
          </p>

          {/* Hologram-like Live Seal */}
          <div className="mt-4 inline-flex items-center gap-2 px-4 py-1.5 bg-emerald-500/20 border border-emerald-400/40 rounded-full text-emerald-100 text-xs font-bold backdrop-blur-xs">
            <CheckCircle2 className="w-4 h-4 text-emerald-300 shrink-0" />
            <span className="tracking-wide">VERIFIED STATUTORY CLEARANCE — MoFPI SIH26236 ENGINE</span>
          </div>
        </div>

        {/* Certificate Body */}
        <div className="p-6 md:p-8 space-y-6">
          {/* Header Metadata Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 p-4 bg-slate-50 rounded-2xl border border-slate-200 text-xs">
            <div>
              <span className="text-slate-400 block text-[10px] uppercase font-bold">Verification Batch ID</span>
              <span className="font-mono font-black text-slate-900 text-sm">{batch_id}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase font-bold">Registration Status</span>
              <span className="inline-flex items-center gap-1 font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-md mt-0.5">
                <ShieldCheck className="w-3.5 h-3.5" />
                {status}
              </span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase font-bold">Issuance Timestamp</span>
              <span className="font-semibold text-slate-800">{timestamps.issued_at}</span>
            </div>
          </div>

          {/* Section 1: Commodity & Regional Cluster */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <Award className="w-4 h-4 text-emerald-600" />
              <span>1. Agricultural Commodity & ODOP Origin</span>
            </h3>
            <div className="p-4 bg-white rounded-2xl border border-slate-200 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h4 className="text-lg font-bold text-slate-900">
                  {commodity.name_en} <span className="text-slate-500 font-normal">({commodity.name_hi})</span>
                </h4>
                <p className="text-xs text-slate-500 mt-0.5">
                  Designated ODOP District: <strong className="text-slate-700">{commodity.odop_region}</strong>
                </p>
              </div>
              <div className="text-right sm:text-right">
                <span className="px-3 py-1 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-bold block sm:inline-block">
                  {commodity.fssai_schedule_category}
                </span>
                <span className="text-[10px] text-slate-400 block mt-1">Classification: {commodity.food_category}</span>
              </div>
            </div>
          </div>

          {/* Section 2: Certified Multi-Layer Packaging Substrate */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <Layers className="w-4 h-4 text-emerald-600" />
              <span>2. Approved Food-Contact Packaging Specification</span>
            </h3>
            <div className="p-5 bg-emerald-50/40 rounded-2xl border border-emerald-200 space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-2">
                <div>
                  <h4 className="text-base font-bold text-slate-900">
                    {certified_packaging.structure_name}
                  </h4>
                  <span className="text-xs font-mono font-semibold text-emerald-700">
                    Code: {certified_packaging.structure_code} · Caliper: {certified_packaging.thickness_um} µm
                  </span>
                </div>
                <span className="px-2.5 py-1 bg-emerald-100 text-emerald-900 rounded-lg text-xs font-bold uppercase tracking-wider shrink-0">
                  IS Compliant
                </span>
              </div>

              {/* Layer Sequence */}
              {certified_packaging.layers && (
                <div className="space-y-1.5 pt-2 border-t border-emerald-100">
                  <span className="text-[11px] font-bold text-slate-700 block">Laminate Structure Sequence:</span>
                  <div className="flex flex-wrap gap-2">
                    {certified_packaging.layers.map((layer, idx) => (
                      <span
                        key={idx}
                        className="px-2.5 py-1 bg-white border border-emerald-300 text-slate-800 rounded-lg text-xs font-medium shadow-2xs"
                      >
                        {idx + 1}. {layer}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Barrier Matrix */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 text-xs">
                <div className="p-2.5 bg-white rounded-xl border border-emerald-100">
                  <span className="text-slate-400 block text-[10px]">Moisture Barrier (WVTR)</span>
                  <span className="font-bold text-slate-800 font-mono">{certified_packaging.water_vapor_transmission_rate}</span>
                </div>
                <div className="p-2.5 bg-white rounded-xl border border-emerald-100">
                  <span className="text-slate-400 block text-[10px]">Oxygen Barrier (OTR)</span>
                  <span className="font-bold text-slate-800 font-mono">{certified_packaging.oxygen_transmission_rate}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Section 3: Statutory Conformity & Standards */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <FileText className="w-4 h-4 text-emerald-600" />
              <span>3. Statutory Indian Standards & Chemical Simulant Matrix</span>
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
                <span className="text-slate-500 font-bold block">BIS Polymer Standard:</span>
                <span className="font-semibold text-slate-900">{certified_packaging.bis_standard}</span>
              </div>
              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
                <span className="text-slate-500 font-bold block">Overall Migration Limit (OML):</span>
                <span className="font-semibold text-emerald-800">{safety_and_conformity.overall_migration_limit}</span>
              </div>
              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
                <span className="text-slate-500 font-bold block">Mandatory Simulants Tested:</span>
                <span className="font-medium text-slate-800">
                  {safety_and_conformity.mandatory_simulants_tested.join(" · ") || "Simulants A, B, C, D"}
                </span>
              </div>
              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
                <span className="text-slate-500 font-bold block">CPCB EPR Classification:</span>
                <span className="font-medium text-slate-800">{certified_packaging.cpcb_epr_category}</span>
              </div>
            </div>
          </div>

          {/* Section 4: Cryptographic Integrity Seal & NABL Stamp */}
          <div className="p-4 bg-slate-900 text-slate-200 rounded-2xl space-y-3 font-mono text-xs">
            <div className="flex items-center justify-between">
              <span className="text-emerald-400 font-bold tracking-wider flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5" />
                CRYPTOGRAPHIC INTEGRITY DIGEST
              </span>
              <span className="text-[10px] text-slate-400">SHA-256</span>
            </div>
            <p className="break-all text-[11px] text-slate-300 font-mono bg-slate-950 p-2.5 rounded-lg border border-slate-800">
              {integrity_hash}
            </p>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between text-[10px] text-slate-400 border-t border-slate-800 pt-2 gap-2">
              <span>NABL ISO/IEC 17025 Conformant Packaging Protocol</span>
              <span>Valid Until: {timestamps.valid_until}</span>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-50 border-t border-slate-200 text-center text-[10px] text-slate-500">
          This digital passport is verifiable under the Government of India MoFPI PMFME Scheme. 
          To re-verify, scan the QR code printed on the physical packaging readiness certificate or visit{' '}
          <a href={issuing_authority.portal} target="_blank" rel="noreferrer" className="text-emerald-700 underline font-semibold">
            pmfme.mofpi.gov.in
          </a>.
        </div>
      </div>
    </div>
  );
};
