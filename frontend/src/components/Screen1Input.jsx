import React, { useState, useEffect } from 'react';
import { Mic, MicOff, Sparkles, MapPin, Tag, Sliders, ArrowRight, RefreshCw, Volume2, ListFilter, PlusCircle, Edit3 } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useVoiceInput } from '../hooks/useVoiceInput';

export const Screen1Input = ({ commodities, selectedCommodity, onSelectCommodity, onAnalyze, isAnalyzing }) => {
  const { language, t } = useLanguage();
  const { isListening, isSupported, startListening, stopListening } = useVoiceInput(language);

  // Custom commodity state
  const [isCustomMode, setIsCustomMode] = useState(false);
  const [customName, setCustomName] = useState('');
  const [customRegion, setCustomRegion] = useState('');
  const [customCategory, setCustomCategory] = useState('Dry Food / Snack');
  const [customRespiration, setCustomRespiration] = useState('Very Low');

  // Sliders state initialized from selectedCommodity
  const [moisture, setMoisture] = useState(7.0);
  const [fat, setFat] = useState(0.1);
  const [ph, setPh] = useState(6.5);
  const [shelfLife, setShelfLife] = useState(180);
  const [storageType, setStorageType] = useState('ambient');
  const [tempC, setTempC] = useState(27);
  const [ambientRh, setAmbientRh] = useState(65);
  const [voiceNotice, setVoiceNotice] = useState('');

  // Sync sliders when selectedCommodity changes
  useEffect(() => {
    if (selectedCommodity && !isCustomMode) {
      setMoisture(selectedCommodity.moisture_pct);
      setFat(selectedCommodity.fat_oil_pct);
      setPh(selectedCommodity.ph_value);
      setShelfLife(selectedCommodity.shelf_life_days);
      setStorageType(selectedCommodity.storage_type || 'ambient');
      setTempC(27);
      setAmbientRh(65);
    }
  }, [selectedCommodity, isCustomMode]);

  const handleVoiceSearch = () => {
    if (isListening) {
      stopListening();
      return;
    }

    setVoiceNotice(t('listening'));
    startListening((spokenText) => {
      setVoiceNotice(`"${spokenText}"`);
      const q = spokenText.toLowerCase().trim();

      // Find matching commodity in seeds
      const match = commodities.find(c =>
        c.name_en.toLowerCase().includes(q) ||
        c.name_hi.includes(q) ||
        c.id.toLowerCase().includes(q) ||
        q.includes(c.id.toLowerCase()) ||
        q.includes(c.name_en.toLowerCase().split(' ')[0])
      );

      if (match) {
        setIsCustomMode(false);
        onSelectCommodity(match);
        setVoiceNotice(language === 'hi' ? `पहचाना गया: ${match.name_hi}` : `Matched: ${match.name_en}`);
      } else {
        setVoiceNotice(language === 'hi' ? `मेल नहीं मिला: "${spokenText}"` : `No direct match for: "${spokenText}"`);
      }
    });
  };

  const handleResetDefaults = () => {
    if (!isCustomMode && selectedCommodity) {
      setMoisture(selectedCommodity.moisture_pct);
      setFat(selectedCommodity.fat_oil_pct);
      setPh(selectedCommodity.ph_value);
      setShelfLife(selectedCommodity.shelf_life_days);
      setStorageType(selectedCommodity.storage_type || 'ambient');
      setTempC(27);
      setAmbientRh(65);
    } else {
      setMoisture(10.0);
      setFat(1.0);
      setPh(6.5);
      setShelfLife(180);
      setStorageType('ambient');
      setTempC(27);
      setAmbientRh(65);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isCustomMode) {
      const cleanName = customName.trim() || 'Custom Food Commodity';
      const cleanId = 'custom_' + cleanName.toLowerCase().replace(/[^a-z0-9]/g, '_');
      onAnalyze({
        commodity_id: cleanId,
        commodity_name: cleanName,
        category: customCategory,
        odop_region: customRegion.trim() || 'Custom Micro-Enterprise Cluster',
        respiration_class: customRespiration,
        moisture_pct: parseFloat(moisture),
        fat_oil_pct: parseFloat(fat),
        ph_value: parseFloat(ph),
        shelf_life_days: parseFloat(shelfLife),
        storage_type: storageType,
        storage_temp_c: parseFloat(tempC),
        ambient_rh: parseFloat(ambientRh)
      });
      return;
    }

    if (!selectedCommodity) return;

    onAnalyze({
      commodity_id: selectedCommodity.id,
      commodity_name: language === 'hi' ? selectedCommodity.name_hi : selectedCommodity.name_en,
      category: selectedCommodity.category,
      odop_region: selectedCommodity.odop_region,
      respiration_class: selectedCommodity.respiration_class,
      moisture_pct: parseFloat(moisture),
      fat_oil_pct: parseFloat(fat),
      ph_value: parseFloat(ph),
      shelf_life_days: parseFloat(shelfLife),
      storage_type: storageType,
      storage_temp_c: parseFloat(tempC),
      ambient_rh: parseFloat(ambientRh)
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-emerald-800 to-green-900 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-emerald-700/60 rounded-full text-xs font-semibold text-emerald-200 mb-2">
              <Sparkles className="w-3.5 h-3.5" />
              {t('pmfme_scheme_tag')}
            </div>
            <h1 className="text-2xl md:text-3xl font-bold tracking-tight">
              {t('app_title')}
            </h1>
            <p className="text-emerald-200 text-sm mt-1 max-w-2xl">
              {t('app_subtitle')}
            </p>
          </div>

          <div className="flex items-center gap-2 bg-emerald-950/40 p-3 rounded-xl border border-emerald-700/50">
            <span className="text-xs text-emerald-300 font-medium">Bilingual Mode:</span>
            <span className="px-2 py-0.5 bg-emerald-600 text-white rounded text-xs font-bold uppercase">
              {language === 'hi' ? 'हिंदी (hi-IN)' : 'English (en-IN)'}
            </span>
          </div>
        </div>
      </div>

      {/* Main Selection Form */}
      <form onSubmit={handleSubmit} className="bg-white rounded-2xl border border-slate-200 p-6 md:p-8 shadow-sm space-y-6">
        {/* Mode Toggle: Seeded ODOP vs Custom Unlisted */}
        <div className="flex items-center gap-2 p-1 bg-slate-100 rounded-xl max-w-md">
          <button
            type="button"
            onClick={() => setIsCustomMode(false)}
            className={`flex-1 py-2 px-3 text-xs font-bold rounded-lg transition flex items-center justify-center gap-1.5 ${
              !isCustomMode
                ? 'bg-white text-emerald-800 shadow-sm'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <ListFilter className="w-3.5 h-3.5" />
            <span>Seeded ODOP Crops ({commodities.length})</span>
          </button>
          <button
            type="button"
            onClick={() => setIsCustomMode(true)}
            className={`flex-1 py-2 px-3 text-xs font-bold rounded-lg transition flex items-center justify-center gap-1.5 ${
              isCustomMode
                ? 'bg-emerald-700 text-white shadow-sm'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <PlusCircle className="w-3.5 h-3.5" />
            <span>Custom / Unlisted Commodity</span>
          </button>
        </div>

        {!isCustomMode ? (
          /* Dropdown & Voice Recognition Bar for Seeded Crops */
          <div>
            <label className="block text-sm font-semibold text-slate-800 mb-2">
              {t('select_commodity')} <span className="text-emerald-600 font-normal">({commodities.length} Seeded ODOP Crops)</span>
            </label>
            <div className="flex items-center gap-3">
              <div className="relative flex-1">
                <select
                  value={selectedCommodity ? selectedCommodity.id : ''}
                  onChange={(e) => {
                    const found = commodities.find(c => c.id === e.target.value);
                    if (found) onSelectCommodity(found);
                  }}
                  className="w-full bg-slate-50 border border-slate-300 rounded-xl px-4 py-3 text-slate-800 font-medium focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none transition"
                >
                  <option value="" disabled>{t('select_placeholder')}</option>
                  {commodities.map((item) => (
                    <option key={item.id} value={item.id}>
                      {language === 'hi' ? item.name_hi : item.name_en} — {item.odop_region}
                    </option>
                  ))}
                </select>
              </div>

              {/* Mic Button */}
              <button
                type="button"
                onClick={handleVoiceSearch}
                title={t('voice_search_tooltip')}
                className={`p-3.5 rounded-xl border transition flex items-center justify-center ${
                  isListening
                    ? 'bg-red-500 text-white border-red-600 animate-pulse ring-4 ring-red-200'
                    : 'bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100 hover:border-emerald-300'
                }`}
              >
                {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
              </button>
            </div>

            {/* Voice Notification / Spoken Text */}
            {voiceNotice && (
              <div className="mt-2 flex items-center gap-2 text-xs font-medium text-emerald-800 bg-emerald-50 px-3 py-1.5 rounded-lg border border-emerald-200">
                <Volume2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>{voiceNotice}</span>
              </div>
            )}
            {!isSupported && (
              <p className="mt-1 text-xs text-amber-600">{t('speech_unsupported')}</p>
            )}

            {/* Selected Commodity Info Badges */}
            {selectedCommodity && (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 p-4 bg-slate-50 rounded-xl border border-slate-200 text-sm mt-4">
                <div className="flex items-center gap-2">
                  <MapPin className="w-4 h-4 text-emerald-600 shrink-0" />
                  <div>
                    <span className="text-xs text-slate-500 block">{t('odop_cluster')}</span>
                    <span className="font-semibold text-slate-800">{selectedCommodity.odop_region}</span>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Tag className="w-4 h-4 text-emerald-600 shrink-0" />
                  <div>
                    <span className="text-xs text-slate-500 block">{t('category')}</span>
                    <span className="font-semibold text-slate-800">{selectedCommodity.category}</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        ) : (
          /* Custom Commodity Input Panel */
          <div className="space-y-4 p-5 bg-emerald-50/50 rounded-xl border border-emerald-200">
            <div className="flex items-center gap-2 text-xs font-bold text-emerald-800 uppercase tracking-wide">
              <Sparkles className="w-4 h-4 text-emerald-600" />
              <span>Custom Agro-Commodity Specification (AI Heuristic & Barrier Synthesis)</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Commodity / Crop Name *
                </label>
                <input
                  type="text"
                  placeholder="e.g., Red Dragonfruit, Moringa Energy Bar, Aonla Murabba"
                  value={customName}
                  onChange={(e) => setCustomName(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded-xl px-3.5 py-2.5 text-sm text-slate-800 focus:ring-2 focus:ring-emerald-500 outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  ODOP Cluster / Enterprise District
                </label>
                <input
                  type="text"
                  placeholder="e.g., Kutch (Gujarat), Wayanad (Kerala)"
                  value={customRegion}
                  onChange={(e) => setCustomRegion(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded-xl px-3.5 py-2.5 text-sm text-slate-800 focus:ring-2 focus:ring-emerald-500 outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Commodity Food Category
                </label>
                <select
                  value={customCategory}
                  onChange={(e) => setCustomCategory(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded-xl px-3.5 py-2.5 text-sm text-slate-800 focus:ring-2 focus:ring-emerald-500 outline-none"
                >
                  <option value="Dry Food / Snack">Dry Food / Snack / Savouries</option>
                  <option value="Fresh Produce">Fresh Produce (Fruits / Vegetables / Mushrooms)</option>
                  <option value="Liquid / Pickle">Pickle, Chutney, Sauce, or Preserves</option>
                  <option value="Dairy / Fat">Dairy / High-Fat Oil / Ghee</option>
                  <option value="Spices / Powder">Spices / Seasonings / Powders</option>
                  <option value="Cereals / Grains">Cereals / Grains / Pulses</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Respiration & Perishability Profile
                </label>
                <select
                  value={customRespiration}
                  onChange={(e) => setCustomRespiration(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded-xl px-3.5 py-2.5 text-sm text-slate-800 focus:ring-2 focus:ring-emerald-500 outline-none"
                >
                  <option value="Very Low">Very Low / Inert (Dried snacks, powders, oils)</option>
                  <option value="Low">Low (Apples, citrus, onions, potatoes)</option>
                  <option value="Moderate">Moderate (Carrots, cabbage, tomatoes)</option>
                  <option value="High">High (Berries, leafy greens, avocados)</option>
                  <option value="Extremely High">Extremely High (Mushrooms, sweet corn, cut produce)</option>
                </select>
              </div>
            </div>
          </div>
        )}

        {/* Customization Sliders Section */}
        <div className="pt-2 border-t border-slate-100 space-y-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm font-semibold text-slate-800">
              <Sliders className="w-4 h-4 text-emerald-600" />
              <span>{t('customize_parameters')}</span>
            </div>
            <button
              type="button"
              onClick={handleResetDefaults}
              className="text-xs text-slate-500 hover:text-emerald-700 flex items-center gap-1 font-medium transition"
            >
              <RefreshCw className="w-3 h-3" />
              Reset ODOP Defaults
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {/* Slider 1: Moisture */}
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
              <div className="flex justify-between items-center text-xs">
                <span className="font-medium text-slate-700">{t('moisture_label')}</span>
                <span className="font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">
                  {moisture}%
                </span>
              </div>
              <input
                type="range"
                min="0.1"
                max="95.0"
                step="0.5"
                value={moisture}
                onChange={(e) => setMoisture(parseFloat(e.target.value))}
                className="w-full accent-emerald-600 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400">
                <span>0.1% (Dry powder)</span>
                <span>95% (Fresh fruit/vegetable)</span>
              </div>
            </div>

            {/* Slider 2: Fat / Oil */}
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
              <div className="flex justify-between items-center text-xs">
                <span className="font-medium text-slate-700">{t('fat_label')}</span>
                <span className="font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">
                  {fat}%
                </span>
              </div>
              <input
                type="range"
                min="0.0"
                max="99.9"
                step="0.5"
                value={fat}
                onChange={(e) => setFat(parseFloat(e.target.value))}
                className="w-full accent-emerald-600 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400">
                <span>0% (Oil-free)</span>
                <span>99.9% (Pure Ghee/Fat)</span>
              </div>
            </div>

            {/* Slider 3: pH Level */}
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
              <div className="flex justify-between items-center text-xs">
                <span className="font-medium text-slate-700">{t('ph_label')}</span>
                <span className="font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">
                  pH {ph}
                </span>
              </div>
              <input
                type="range"
                min="2.0"
                max="8.5"
                step="0.1"
                value={ph}
                onChange={(e) => setPh(parseFloat(e.target.value))}
                className="w-full accent-emerald-600 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400">
                <span>pH 2.0 (Acidic Pickle)</span>
                <span>pH 7.0+ (Neutral)</span>
              </div>
            </div>

            {/* Slider 4: Shelf Life */}
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
              <div className="flex justify-between items-center text-xs">
                <span className="font-medium text-slate-700">{t('shelf_life_label')}</span>
                <span className="font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">
                  {shelfLife} {t('days')}
                </span>
              </div>
              <input
                type="range"
                min="7"
                max="730"
                step="7"
                value={shelfLife}
                onChange={(e) => setShelfLife(parseInt(e.target.value))}
                className="w-full accent-emerald-600 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400">
                <span>7 days (Chilled)</span>
                <span>730 days (2 Years)</span>
              </div>
            </div>

            {/* Slider 5: Storage Temperature */}
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
              <div className="flex justify-between items-center text-xs">
                <span className="font-medium text-slate-700">Storage Temperature (°C)</span>
                <span className="font-bold text-rose-700 bg-rose-100 px-2 py-0.5 rounded">
                  {tempC}°C
                </span>
              </div>
              <input
                type="range"
                min="4"
                max="45"
                step="1"
                value={tempC}
                onChange={(e) => setTempC(parseFloat(e.target.value))}
                className="w-full accent-rose-600 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400">
                <span>4°C (Cold Chain)</span>
                <span>27°C (Standard)</span>
                <span>45°C (Extreme)</span>
              </div>
            </div>

            {/* Slider 6: Ambient Humidity */}
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
              <div className="flex justify-between items-center text-xs">
                <span className="font-medium text-slate-700">Ambient Relative Humidity (% RH)</span>
                <span className="font-bold text-blue-700 bg-blue-100 px-2 py-0.5 rounded">
                  {ambientRh}% RH
                </span>
              </div>
              <input
                type="range"
                min="20"
                max="95"
                step="1"
                value={ambientRh}
                onChange={(e) => setAmbientRh(parseFloat(e.target.value))}
                className="w-full accent-blue-600 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400">
                <span>20% (Arid Zone)</span>
                <span>65% (IS Standard)</span>
                <span>95% (Monsoon Coastal)</span>
              </div>
            </div>
          </div>

          {/* Storage Conditions Radios */}
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <span className="block text-xs font-semibold text-slate-700 mb-1">
              {t('storage_condition')}
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs">
              {[
                { id: 'ambient', label: t('storage_ambient') },
                { id: 'chilled', label: t('storage_chilled') },
                { id: 'frozen', label: t('storage_frozen') }
              ].map((opt) => (
                <label
                  key={opt.id}
                  className={`flex items-center gap-2 p-2.5 rounded-lg border cursor-pointer transition ${
                    storageType === opt.id
                      ? 'bg-emerald-100/70 border-emerald-500 font-semibold text-emerald-900'
                      : 'bg-white border-slate-200 text-slate-700 hover:border-slate-300'
                  }`}
                >
                  <input
                    type="radio"
                    name="storageType"
                    value={opt.id}
                    checked={storageType === opt.id}
                    onChange={(e) => setStorageType(e.target.value)}
                    className="accent-emerald-600"
                  />
                  <span>{opt.label}</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        {/* Action Button */}
        <div className="pt-2">
          <button
            type="submit"
            disabled={isCustomMode ? (!customName.trim() || isAnalyzing) : (!selectedCommodity || isAnalyzing)}
            className="w-full bg-emerald-700 hover:bg-emerald-800 disabled:bg-slate-300 text-white font-bold py-3.5 px-6 rounded-xl shadow-md hover:shadow-lg flex items-center justify-center gap-2 transition duration-200 text-base"
          >
            {isAnalyzing ? (
              <>
                <RefreshCw className="w-5 h-5 animate-spin" />
                <span>Analyzing Barrier Equations & ML Model...</span>
              </>
            ) : (
              <>
                <span>{t('btn_get_recommendation')}</span>
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
