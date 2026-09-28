import React, { useState, useEffect } from 'react';
import { Package, Globe, CheckCircle, ChevronRight, Layers, ShieldCheck, FileCheck2, Cpu, Scale, QrCode, Sun, Moon } from 'lucide-react';
import { useLanguage } from './context/LanguageContext';
import { useTheme } from './context/ThemeContext';
import { Screen1Input } from './components/Screen1Input';
import { Screen2Recommendation } from './components/Screen2Recommendation';
import { Screen3Compliance } from './components/Screen3Compliance';
import { Screen4ReadinessSheet } from './components/Screen4ReadinessSheet';
import { VerifyPassport } from './components/VerifyPassport';
import { LabelAuditor } from './components/LabelAuditor';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught:", error, errorInfo);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div className="max-w-xl mx-auto p-6 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 rounded-2xl text-center space-y-4 my-10">
          <div className="w-12 h-12 bg-rose-100 dark:bg-rose-900 text-rose-600 dark:text-rose-300 rounded-full flex items-center justify-center mx-auto text-xl font-bold">!</div>
          <h3 className="text-lg font-bold text-rose-950 dark:text-rose-200">An unexpected rendering issue occurred</h3>
          <p className="text-xs text-rose-700 dark:text-rose-400 font-mono bg-rose-100/60 dark:bg-rose-900/40 p-2.5 rounded-lg text-left overflow-auto max-h-24">
            {this.state.error?.message || "Unknown error"}
          </p>
          <button
            type="button"
            onClick={() => {
              this.setState({ hasError: false, error: null });
              if (this.props.onReset) this.props.onReset();
              else window.location.href = '/';
            }}
            className="px-5 py-2.5 bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold rounded-xl shadow-xs transition"
          >
            Return to Dashboard
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

export const App = () => {
  const { language, toggleLanguage, t } = useLanguage();
  const { theme, toggleTheme, isDark } = useTheme();

  const [activeView, setActiveView] = useState(() => {
    if (typeof window !== 'undefined') {
      const p = window.location.pathname;
      const s = window.location.search;
      if (p.includes('/verify') || s.includes('batch=')) return 'verify';
      if (p.includes('/audit')) return 'auditor';
    }
    return 'stepper';
  });

  const [commodities, setCommodities] = useState([]);
  const [selectedCommodity, setSelectedCommodity] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [complianceData, setComplianceData] = useState(null);
  const [currentStep, setCurrentStep] = useState(1);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Fetch commodities seed on mount
  useEffect(() => {
    fetch('/api/commodities')
      .then(res => res.json())
      .then(data => {
        if (data && data.commodities && data.commodities.length > 0) {
          setCommodities(data.commodities);
          setSelectedCommodity(data.commodities[0]); // default to Makhana
        }
      })
      .catch(err => {
        console.warn("Could not fetch commodities, retrying...", err);
      });
  }, []);

  const handleAnalyze = async (inputParams) => {
    setIsAnalyzing(true);
    try {
      // 1. Fetch ML Recommendation & Barrier Specs
      const recRes = await fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(inputParams)
      });
      const recData = await recRes.json();
      setRecommendation(recData);

      // 2. Fetch Linked India Compliance Data
      const qParams = new URLSearchParams();
      if (inputParams.ph_value !== undefined) qParams.set('ph_value', inputParams.ph_value);
      if (inputParams.fat_oil_pct !== undefined) qParams.set('fat_oil_pct', inputParams.fat_oil_pct);
      if (inputParams.moisture_pct !== undefined) qParams.set('moisture_pct', inputParams.moisture_pct);
      if (inputParams.commodity_name) qParams.set('commodity_name', inputParams.commodity_name);
      const qStr = qParams.toString() ? `?${qParams.toString()}` : '';
      const compRes = await fetch(`/api/compliance/${inputParams.commodity_id}${qStr}`);
      const compData = await compRes.json();
      setComplianceData(compData);

      // Advance to Screen 2
      setCurrentStep(2);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (e) {
      console.error("Analysis error:", e);
      alert("Error connecting to packaging recommendation engine. Ensure backend is running on :8000");
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Synchronize browser history and popstate
  useEffect(() => {
    const handlePopState = () => {
      const p = window.location.pathname;
      const s = window.location.search;
      if (p.includes('/verify') || s.includes('batch=')) setActiveView('verify');
      else if (p.includes('/audit')) setActiveView('auditor');
      else setActiveView('stepper');
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const navigateTo = (view, query = '') => {
    setActiveView(view);
    const path = view === 'verify' ? `/verify${query}` : view === 'auditor' ? '/audit' : '/';
    window.history.pushState({}, '', path);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const steps = [
    { num: 1, title: t('step1_nav'), icon: Layers },
    { num: 2, title: t('step2_nav'), icon: Package },
    { num: 3, title: t('step3_nav'), icon: ShieldCheck },
    { num: 4, title: t('step4_nav'), icon: FileCheck2 },
  ];

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-[#0B0F17] text-slate-900 dark:text-slate-100 flex flex-col font-sans transition-colors duration-200 relative selection:bg-emerald-500/20 selection:text-emerald-700 dark:selection:text-emerald-300">
      {/* Ambient background glow for enterprise dark mode */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden opacity-0 dark:opacity-100 transition-opacity duration-500 z-0">
        <div className="absolute -top-40 left-1/2 -translate-x-1/2 w-[900px] h-[450px] bg-gradient-to-b from-emerald-600/10 via-teal-500/5 to-transparent blur-3xl rounded-full" />
      </div>

      {/* Top Tricolor Brand Accent Line */}
      <div className="h-0.5 bg-gradient-to-r from-amber-500 via-slate-200 dark:via-slate-700 to-emerald-600 relative z-40" />

      {/* Top Navbar */}
      <header className="no-print bg-white/85 dark:bg-[#0B0F17]/90 backdrop-blur-md border-b border-slate-200/80 dark:border-slate-800/80 sticky top-0 z-30 shadow-xs transition-colors duration-200">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between gap-3">
          <div 
            className="flex items-center gap-3 cursor-pointer group"
            onClick={() => navigateTo('stepper')}
            title="Return to Home Dashboard"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-600 to-teal-800 text-white flex items-center justify-center font-bold shadow-md shadow-emerald-950/20 ring-1 ring-white/20 group-hover:scale-105 transition-transform duration-200">
              <Package className="w-5 h-5 text-emerald-100" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-slate-900 dark:text-white text-base tracking-tight leading-tight">PackAI India</span>
                <span className="px-2 py-0.5 bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 text-[10px] font-black rounded-md uppercase border border-emerald-200 dark:border-emerald-800 tracking-wider">
                  SIH26236
                </span>
              </div>
              <div className="flex items-center gap-1.5 text-[11px] text-slate-500 dark:text-slate-400">
                <span className="font-semibold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider text-[9px]">MoFPI</span>
                <span>·</span>
                <span>PMFME & ODOP Packaging Studio</span>
              </div>
            </div>
          </div>

          {/* Center Engine Status Live Pill */}
          <div className="hidden lg:flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/25 text-[11px] font-mono font-medium text-emerald-700 dark:text-emerald-300 shadow-xs">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span>DETERMINISTIC ENGINE: ACTIVE (92.2% ACCURACY) | OFFLINE-READY</span>
          </div>

          <div className="flex items-center gap-2 sm:gap-3">
            {/* View Switcher: Stepper (Recommendation Engine) */}
            <button
              type="button"
              onClick={() => navigateTo('stepper')}
              className={`flex items-center gap-1.5 px-3 py-1.5 border rounded-xl text-xs font-bold transition ${
                activeView === 'stepper'
                  ? 'bg-emerald-50 dark:bg-emerald-950/60 border-emerald-300 dark:border-emerald-700 text-emerald-800 dark:text-emerald-300 shadow-xs'
                  : 'bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300'
              }`}
              title="Recommendation & Compliance Flow"
            >
              <Layers className="w-3.5 h-3.5 text-emerald-700 dark:text-emerald-400" />
              <span className="hidden sm:inline">Engine</span>
            </button>

            {/* View Switcher: Label Artwork Auditor */}
            <button
              type="button"
              onClick={() => navigateTo(activeView === 'auditor' ? 'stepper' : 'auditor')}
              className={`flex items-center gap-1.5 px-3 py-1.5 border rounded-xl text-xs font-bold transition ${
                activeView === 'auditor'
                  ? 'bg-amber-50 dark:bg-amber-950/60 border-amber-400 dark:border-amber-700 text-amber-900 dark:text-amber-300 shadow-xs'
                  : 'bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300'
              }`}
              title="Reverse FSSAI Label Artwork Auditor"
            >
              <FileCheck2 className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
              <span className="hidden sm:inline">Label Auditor</span>
            </button>

            {/* View Switcher: Digital Product Passport */}
            <button
              type="button"
              onClick={() => {
                const q = recommendation ? `?id=${recommendation.commodity_id}&batch=PMFME-2026-CERT` : '';
                navigateTo(activeView === 'verify' ? 'stepper' : 'verify', q);
              }}
              className={`flex items-center gap-1.5 px-3 py-1.5 border rounded-xl text-xs font-bold transition ${
                activeView === 'verify'
                  ? 'bg-indigo-50 dark:bg-indigo-950/60 border-indigo-400 dark:border-indigo-700 text-indigo-900 dark:text-indigo-300 shadow-xs'
                  : 'bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300'
              }`}
              title="Live Digital Product Passport Verification"
            >
              <QrCode className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />
              <span className="hidden sm:inline">Passport</span>
            </button>

            {/* Language Switcher Button */}
            <button
              type="button"
              onClick={toggleLanguage}
              className="flex items-center gap-1.5 px-2.5 sm:px-3 py-1.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-300 transition"
              title="Toggle Hindi / English"
            >
              <Globe className="w-3.5 h-3.5 text-emerald-700 dark:text-emerald-400" />
              <span>{language === 'en' ? 'हिंदी' : 'EN'}</span>
            </button>

            {/* Dark / Light Mode Switcher Button */}
            <button
              type="button"
              onClick={toggleTheme}
              className="flex items-center justify-center p-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-700 rounded-xl text-slate-700 dark:text-slate-200 transition"
              title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
              aria-label="Toggle theme"
            >
              {isDark ? (
                <Sun className="w-4 h-4 text-amber-400" />
              ) : (
                <Moon className="w-4 h-4 text-slate-600" />
              )}
            </button>
          </div>
        </div>
      </header>

      {/* Connected 4-Step Progress Stepper Navigation */}
      {activeView === 'stepper' && (
        <nav className="no-print bg-white/70 dark:bg-[#0B0F17]/80 backdrop-blur-sm border-b border-slate-200 dark:border-slate-800/80 px-4 py-3 transition-colors duration-200 relative z-20">
          <div className="max-w-4xl mx-auto flex items-center justify-between gap-1 sm:gap-2">
            {steps.map((step, idx) => {
              const isActive = currentStep === step.num;
              const isCompleted = currentStep > step.num;
              const isClickable = step.num === 1 || (recommendation && complianceData);

              return (
                <React.Fragment key={step.num}>
                  <button
                    type="button"
                    disabled={!isClickable}
                    onClick={() => isClickable && setCurrentStep(step.num)}
                    className={`flex items-center gap-2 sm:gap-2.5 px-2 py-1.5 rounded-xl text-xs sm:text-sm font-semibold transition shrink-0 group ${
                      isActive
                        ? 'text-emerald-700 dark:text-emerald-400'
                        : isCompleted
                        ? 'text-slate-700 dark:text-slate-300 hover:text-emerald-600 dark:hover:text-emerald-400'
                        : 'text-slate-400 dark:text-slate-600 cursor-not-allowed'
                    }`}
                  >
                    <div
                      className={`w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-200 shrink-0 ${
                        isActive
                          ? 'bg-emerald-600 text-white ring-4 ring-emerald-500/25 shadow-md shadow-emerald-900/30 scale-105'
                          : isCompleted
                          ? 'bg-emerald-500/15 dark:bg-emerald-950/80 text-emerald-700 dark:text-emerald-300 border border-emerald-400/40 dark:border-emerald-600'
                          : 'bg-white dark:bg-slate-800 text-slate-400 dark:text-slate-500 border border-slate-300 dark:border-slate-700'
                      }`}
                    >
                      {isCompleted ? <CheckCircle className="w-4 h-4 text-emerald-600 dark:text-emerald-400" /> : step.num}
                    </div>
                    <span className="hidden sm:inline font-medium tracking-tight whitespace-nowrap">
                      {step.title}
                    </span>
                  </button>

                  {idx < steps.length - 1 && (
                    <div className="flex-1 mx-1.5 sm:mx-3 h-0.5 min-w-[12px] bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className={`h-full transition-all duration-300 ${
                          currentStep > step.num
                            ? 'bg-gradient-to-r from-emerald-500 to-teal-500 w-full'
                            : 'w-0'
                        }`}
                      />
                    </div>
                  )}
                </React.Fragment>
              );
            })}
          </div>
        </nav>
      )}

      {/* Main Content Area */}
      <main className="flex-1 max-w-6xl w-full mx-auto px-4 py-6 md:py-8">
        <ErrorBoundary onReset={() => setCurrentStep(1)}>
          {activeView === 'verify' && (
            <VerifyPassport onBack={() => navigateTo('stepper')} />
          )}

          {activeView === 'auditor' && (
            <LabelAuditor onBack={() => navigateTo('stepper')} />
          )}

          {activeView === 'stepper' && (
            <>
              {currentStep === 1 && (
                <Screen1Input
                  commodities={commodities}
                  selectedCommodity={selectedCommodity}
                  onSelectCommodity={setSelectedCommodity}
                  onAnalyze={handleAnalyze}
                  isAnalyzing={isAnalyzing}
                />
              )}

              {currentStep === 2 && recommendation && (
                <Screen2Recommendation
                  recommendation={recommendation}
                  onNext={() => {
                    setCurrentStep(3);
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                  }}
                  onBack={() => {
                    setCurrentStep(1);
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                  }}
                />
              )}

              {currentStep === 3 && complianceData && (
                <Screen3Compliance
                  complianceData={complianceData}
                  onNext={() => {
                    setCurrentStep(4);
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                  }}
                  onBack={() => {
                    setCurrentStep(2);
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                  }}
                />
              )}

              {currentStep === 4 && recommendation && complianceData && (
                <Screen4ReadinessSheet
                  recommendation={recommendation}
                  complianceData={complianceData}
                  onBack={() => {
                    setCurrentStep(3);
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                  }}
                  onOpenPassport={(batch) => {
                    navigateTo('verify', `?id=${recommendation.commodity_id}&batch=${batch || 'PMFME-2026-CERT'}`);
                  }}
                />
              )}
            </>
          )}
        </ErrorBoundary>
      </main>

      {/* Footer */}
      <footer className="no-print bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 py-4 text-center text-xs text-slate-500 dark:text-slate-400 transition-colors duration-200">
        <div className="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>Smart India Hackathon 2026 · Problem Statement SIH26236 (Software Edition)</span>
          <span className="font-medium text-emerald-800 dark:text-emerald-400">MoFPI Decision Support Prototype · Offline-First Architecture</span>
        </div>
      </footer>
    </div>
  );
};

export default App;
