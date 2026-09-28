import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  AlertTriangle, 
  CheckCircle2, 
  XCircle, 
  FileText, 
  RefreshCw, 
  Sparkles, 
  Check, 
  Copy, 
  ArrowRight,
  Info,
  Scale,
  Building,
  Tag
} from 'lucide-react';

export const LabelAuditor = ({ onBack }) => {
  const [labelText, setLabelText] = useState('');
  const [isAuditing, setIsAuditing] = useState(false);
  const [auditResult, setAuditResult] = useState(null);
  const [samples, setSamples] = useState({ compliant: '', non_compliant: '' });
  const [activeTab, setActiveTab] = useState('violations'); // 'violations' or 'passed'
  const [copied, setCopied] = useState(false);

  // Fetch sample texts from backend on mount
  useEffect(() => {
    fetch('/api/audit-samples')
      .then((res) => res.json())
      .then((data) => {
        setSamples({
          compliant: data.compliant_sample,
          non_compliant: data.non_compliant_sample
        });
      })
      .catch((err) => console.warn("Could not load audit samples:", err));
  }, []);

  const handleRunAudit = async (textToAudit) => {
    const targetText = textToAudit !== undefined ? textToAudit : labelText;
    if (!targetText.trim()) return;

    setIsAuditing(true);
    try {
      const res = await fetch('/api/audit-label', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ raw_text: targetText })
      });
      const data = await res.json();
      setAuditResult(data);
      if (data.violations && data.violations.length > 0) {
        setActiveTab('violations');
      } else {
        setActiveTab('passed');
      }
    } catch (e) {
      console.error("Audit error:", e);
      alert("Error contacting FSSAI Label Audit Engine.");
    } finally {
      setIsAuditing(false);
    }
  };

  const loadSample = (type) => {
    const text = type === 'compliant' ? samples.compliant : samples.non_compliant;
    setLabelText(text);
    handleRunAudit(text);
  };

  const handleCopyReport = () => {
    if (!auditResult) return;
    const summary = `PackAI India - FSSAI Label Compliance Audit Report
Status: ${auditResult.verdict} (${auditResult.score}/100)
Violations (${auditResult.failed_count}):
${auditResult.violations.map((v, i) => `${i + 1}. [${v.rule_id}] ${v.name}: ${v.remedy} (${v.citation})`).join('\n')}
Verified Checks (${auditResult.passed_count}):
${auditResult.passed_rules.map((p, i) => `${i + 1}. ${p.name}: ${p.found_value}`).join('\n')}
`;
    navigator.clipboard.writeText(summary);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 my-4 px-3 sm:px-0">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-emerald-800 to-slate-900 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-emerald-700/60 rounded-full text-xs font-semibold text-emerald-200 mb-2">
              <Scale className="w-3.5 h-3.5" />
              <span>Reverse FSSAI & Legal Metrology Statutory Auditor</span>
            </div>
            <h1 className="text-2xl font-bold tracking-tight">
              Pre-Print Packaging Artwork & Label Auditor
            </h1>
            <p className="text-xs text-emerald-200 mt-1 max-w-2xl">
              Instant automated compliance testing against Food Safety and Standards (Labelling and Display) Regulations, 2020 
              and Legal Metrology (Packaged Commodities) Rules, 2011.
            </p>
          </div>

          {onBack && (
            <button
              onClick={onBack}
              className="px-3.5 py-2 bg-white/10 hover:bg-white/20 border border-white/20 rounded-xl text-xs font-bold transition self-start sm:self-auto shrink-0"
            >
              Back to Dashboard
            </button>
          )}
        </div>
      </div>

      {/* Main Studio Area */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-5">
        {/* Sample Load Buttons */}
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
          <span className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-emerald-600" />
            <span>Test Label Artwork Text</span>
          </span>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => loadSample('compliant')}
              className="px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-300 rounded-lg text-xs font-semibold transition"
            >
              Load Compliant Sample (100%)
            </button>
            <button
              type="button"
              onClick={() => loadSample('non_compliant')}
              className="px-3 py-1.5 bg-rose-50 hover:bg-rose-100 text-rose-800 border border-rose-300 rounded-lg text-xs font-semibold transition"
            >
              Load Defective Sample (0%)
            </button>
          </div>
        </div>

        {/* Text Input Area */}
        <div className="space-y-2">
          <label className="block text-xs font-semibold text-slate-700">
            Paste Packaging Artwork Copy / Label Declaration Text:
          </label>
          <textarea
            rows={7}
            value={labelText}
            onChange={(e) => setLabelText(e.target.value)}
            placeholder="Paste text printed on front or back panel (e.g., FSSAI Lic No, MRP, Net Qty, Unit Sale Price, Ingredients, Nutritional Information, Dates, Veg logo, Address)..."
            className="w-full p-4 rounded-xl border border-slate-300 bg-slate-50 font-mono text-xs text-slate-800 focus:ring-2 focus:ring-emerald-500 focus:bg-white outline-none transition"
          />
        </div>

        {/* Action Button */}
        <div className="flex items-center justify-between gap-3">
          <span className="text-xs text-slate-500">
            Checks 10 mandatory statutory rules under FSSAI 2020 & Legal Metrology.
          </span>
          <button
            type="button"
            onClick={() => handleRunAudit()}
            disabled={!labelText.trim() || isAuditing}
            className="px-6 py-2.5 bg-emerald-700 hover:bg-emerald-800 disabled:bg-slate-300 text-white rounded-xl text-xs font-bold shadow-xs hover:shadow transition flex items-center gap-2"
          >
            {isAuditing ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Auditing Statutory Clauses...</span>
              </>
            ) : (
              <>
                <span>Run Statutory Label Audit</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </div>

      {/* Audit Results View */}
      {auditResult && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6">
          {/* Top Score Banner */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-5 rounded-2xl border"
               style={{ backgroundColor: `${auditResult.verdict_color}10`, borderColor: `${auditResult.verdict_color}40` }}>
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 rounded-2xl flex flex-col items-center justify-center font-black shadow-inner"
                   style={{ backgroundColor: auditResult.verdict_color, color: '#ffffff' }}>
                <span className="text-2xl leading-none">{auditResult.score}</span>
                <span className="text-[9px] uppercase tracking-wider font-bold">/ 100</span>
              </div>
              <div>
                <span className="text-xs font-bold uppercase tracking-wider block" style={{ color: auditResult.verdict_color }}>
                  Statutory Audit Verdict: {auditResult.verdict}
                </span>
                <h3 className="text-base font-bold text-slate-900 mt-0.5">
                  {auditResult.summary}
                </h3>
                <span className="text-xs text-slate-500 mt-1 block">
                  Passed {auditResult.passed_count} of {auditResult.total_checks} mandatory statutory checkpoints ({auditResult.failed_count} violations detected).
                </span>
              </div>
            </div>

            <button
              onClick={handleCopyReport}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-slate-300 text-xs font-bold text-slate-700 hover:bg-slate-50 shadow-2xs self-start sm:self-auto shrink-0 transition"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? "Copied Report" : "Copy Audit Report"}</span>
            </button>
          </div>

          {/* Tab Navigation: Violations vs Passed */}
          <div className="flex items-center gap-3 border-b border-slate-200">
            <button
              onClick={() => setActiveTab('violations')}
              className={`pb-3 text-xs font-bold flex items-center gap-2 border-b-2 transition ${
                activeTab === 'violations'
                  ? 'border-rose-600 text-rose-700'
                  : 'border-transparent text-slate-500 hover:text-slate-800'
              }`}
            >
              <XCircle className="w-4 h-4 text-rose-600" />
              <span>Statutory Violations & Remedies ({auditResult.failed_count})</span>
            </button>
            <button
              onClick={() => setActiveTab('passed')}
              className={`pb-3 text-xs font-bold flex items-center gap-2 border-b-2 transition ${
                activeTab === 'passed'
                  ? 'border-emerald-600 text-emerald-700'
                  : 'border-transparent text-slate-500 hover:text-slate-800'
              }`}
            >
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Verified Compliant Clauses ({auditResult.passed_count})</span>
            </button>
          </div>

          {/* Active Tab Content */}
          {activeTab === 'violations' ? (
            auditResult.violations.length === 0 ? (
              <div className="p-8 text-center bg-emerald-50 rounded-2xl border border-emerald-200 text-emerald-800 space-y-2">
                <CheckCircle2 className="w-10 h-10 text-emerald-600 mx-auto" />
                <h4 className="text-base font-bold">Zero Statutory Violations Detected!</h4>
                <p className="text-xs text-emerald-700 max-w-md mx-auto">
                  All mandatory FSSAI 2020 labelling clauses and Legal Metrology Packaged Commodities provisions are fully compliant.
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                {auditResult.violations.map((v, i) => (
                  <div key={i} className="p-4 bg-rose-50/50 rounded-2xl border border-rose-200 space-y-2">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                      <div className="flex items-center gap-2">
                        <span className="w-5 h-5 rounded-full bg-rose-600 text-white text-[11px] font-bold flex items-center justify-center shrink-0">
                          {i + 1}
                        </span>
                        <h4 className="text-xs font-bold text-slate-900">{v.name}</h4>
                        <span className="text-[10px] bg-rose-200 text-rose-900 font-semibold px-2 py-0.5 rounded">
                          {v.category}
                        </span>
                      </div>
                      <span className="text-[10px] font-mono text-rose-700 font-medium">
                        {v.citation}
                      </span>
                    </div>

                    <div className="pl-7 space-y-1 text-xs">
                      <p className="text-slate-600">
                        <strong className="text-slate-700">Found Value:</strong> {v.found_value}
                      </p>
                      <div className="p-2.5 bg-white rounded-xl border border-rose-200 text-rose-900 font-medium text-[11px] flex items-start gap-2">
                        <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                        <div>
                          <strong>Actionable Legal Remedy:</strong> {v.remedy}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )
          ) : (
            <div className="space-y-2.5">
              {auditResult.passed_rules.map((p, i) => (
                <div key={i} className="p-3.5 bg-emerald-50/40 rounded-xl border border-emerald-200 flex items-start justify-between gap-3 text-xs">
                  <div className="flex items-start gap-2.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                    <div>
                      <h4 className="font-bold text-slate-900">{p.name}</h4>
                      <span className="text-emerald-800 font-medium text-[11px] block mt-0.5">
                        {p.found_value}
                      </span>
                    </div>
                  </div>
                  <span className="text-[10px] font-mono text-slate-500 shrink-0">
                    {p.citation}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
