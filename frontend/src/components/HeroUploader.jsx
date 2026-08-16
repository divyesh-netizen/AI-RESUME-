import React, { useState, useRef } from 'react';
import { UploadCloud, FileText, Sparkles, Check, ArrowRight, X, Briefcase, FileCheck, Layers } from 'lucide-react';

export default function HeroUploader({
  resumeFile,
  setResumeFile,
  resumeText,
  setResumeText,
  jobDescription,
  setJobDescription,
  candidateName,
  setCandidateName,
  onScreen,
  loading,
  sampleData,
  onLoadSample
}) {
  const [inputMode, setInputMode] = useState('upload'); // 'upload' or 'paste'
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setResumeFile(file);
      setInputMode('upload');
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      setResumeFile(e.target.files[0]);
      setInputMode('upload');
    }
  };

  const clearFile = () => {
    setResumeFile(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="relative">
      {/* Background glow orb */}
      <div className="absolute -top-12 left-1/2 -translate-x-1/2 w-96 h-96 bg-indigo-600/15 rounded-full blur-3xl pointer-events-none -z-10 animate-pulse-glow" />

      {/* Hero Header */}
      <div className="text-center max-w-3xl mx-auto pt-6 pb-8">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-gradient-to-r from-indigo-500/10 via-purple-500/10 to-pink-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold mb-4 shadow-sm">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
          <span>Hybrid TF-IDF + 500+ Skills Taxonomy Engine</span>
        </div>
        <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight mb-3">
          Screen resumes in seconds with{' '}
          <span className="bg-gradient-to-r from-indigo-400 via-purple-300 to-pink-400 bg-clip-text text-transparent">
            AI Precision
          </span>
        </h1>
        <p className="text-sm sm:text-base text-slate-300 max-w-2xl mx-auto leading-relaxed">
          Upload any resume and paste a job description. Get deep match scores, skills gap breakdown, ATS optimization suggestions, and personalized AI coaching.
        </p>

        {/* Quick Sample Selector Pills */}
        {sampleData && (
          <div className="mt-5 flex flex-wrap items-center justify-center gap-2">
            <span className="text-xs text-slate-400 flex items-center gap-1">
              <Layers className="w-3.5 h-3.5" /> Try Sample Role:
            </span>
            <button
              onClick={() => onLoadSample('frontend_dev')}
              className="text-xs px-3 py-1.5 rounded-full bg-slate-900/90 border border-slate-700/80 text-slate-300 hover:text-white hover:border-indigo-500/50 hover:bg-slate-800 transition-all cursor-pointer"
            >
              ⚡ Senior Frontend (React/TS)
            </button>
            <button
              onClick={() => onLoadSample('fullstack_dev')}
              className="text-xs px-3 py-1.5 rounded-full bg-slate-900/90 border border-slate-700/80 text-slate-300 hover:text-white hover:border-purple-500/50 hover:bg-slate-800 transition-all cursor-pointer"
            >
              💻 Full Stack (Python/React)
            </button>
            <button
              onClick={() => onLoadSample('ai_engineer')}
              className="text-xs px-3 py-1.5 rounded-full bg-slate-900/90 border border-slate-700/80 text-slate-300 hover:text-white hover:border-pink-500/50 hover:bg-slate-800 transition-all cursor-pointer"
            >
              🧠 AI & ML Engineer (LLMs)
            </button>
          </div>
        )}
      </div>

      {/* Main Upload Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-7xl mx-auto">
        
        {/* LEFT: Resume Upload Card */}
        <div className="glass-panel rounded-2xl p-6 relative border border-slate-800 flex flex-col justify-between shadow-xl">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <div className="p-2 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
                  <FileCheck className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-white">1. Candidate Resume</h3>
                  <p className="text-xs text-slate-400">Drop PDF, DOCX, or paste resume text</p>
                </div>
              </div>

              {/* Mode Toggle */}
              <div className="flex items-center bg-slate-900 p-1 rounded-lg border border-slate-800 text-xs">
                <button
                  type="button"
                  onClick={() => setInputMode('upload')}
                  className={`px-2.5 py-1 rounded-md transition-all ${
                    inputMode === 'upload' ? 'bg-indigo-600 text-white font-medium shadow-sm' : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  File Upload
                </button>
                <button
                  type="button"
                  onClick={() => setInputMode('paste')}
                  className={`px-2.5 py-1 rounded-md transition-all ${
                    inputMode === 'paste' ? 'bg-indigo-600 text-white font-medium shadow-sm' : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  Paste Text
                </button>
              </div>
            </div>

            {/* Candidate Name Input (Optional) */}
            <div className="mb-4">
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                Candidate Name <span className="text-slate-500 font-normal">(optional, auto-detected)</span>
              </label>
              <input
                type="text"
                value={candidateName}
                onChange={(e) => setCandidateName(e.target.value)}
                placeholder="e.g. Jane Doe"
                className="w-full glass-input rounded-xl px-3.5 py-2 text-sm placeholder:text-slate-600"
              />
            </div>

            {/* Upload Mode UI */}
            {inputMode === 'upload' ? (
              <div>
                {!resumeFile ? (
                  <div
                    onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                    onDragLeave={() => setDragOver(false)}
                    onDrop={handleFileDrop}
                    onClick={() => fileInputRef.current?.click()}
                    className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all flex flex-col items-center justify-center min-h-[210px] ${
                      dragOver
                        ? 'border-indigo-500 bg-indigo-500/10'
                        : 'border-slate-700/80 hover:border-indigo-500/50 hover:bg-slate-900/50'
                    }`}
                  >
                    <input
                      type="file"
                      ref={fileInputRef}
                      onChange={handleFileSelect}
                      accept=".pdf,.docx,.doc,.txt"
                      className="hidden"
                    />
                    <div className="w-12 h-12 rounded-full bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-3 shadow-inner">
                      <UploadCloud className="w-6 h-6 animate-bounce" />
                    </div>
                    <p className="text-sm font-semibold text-white mb-1">
                      Click to upload or drag & drop
                    </p>
                    <p className="text-xs text-slate-400 mb-3">
                      Supports PDF, DOCX, or TXT (Max 10MB)
                    </p>
                    <div className="flex items-center gap-2 text-[10px] text-slate-400">
                      <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700">PDF</span>
                      <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700">DOCX</span>
                      <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700">TXT</span>
                    </div>
                  </div>
                ) : (
                  <div className="rounded-xl border border-indigo-500/30 bg-indigo-500/5 p-4 flex items-center justify-between min-h-[210px]">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
                        <FileText className="w-6 h-6" />
                      </div>
                      <div>
                        <p className="text-sm font-bold text-white truncate max-w-xs">{resumeFile.name}</p>
                        <p className="text-xs text-slate-400">
                          {(resumeFile.size / 1024).toFixed(1)} KB • Ready for AI screening
                        </p>
                        <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-400 mt-1">
                          <Check className="w-3 h-3" /> File attached
                        </span>
                      </div>
                    </div>
                    <button
                      onClick={clearFile}
                      className="p-2 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-rose-400 transition-colors"
                      title="Remove file"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </div>
                )}
              </div>
            ) : (
              /* Paste Mode UI */
              <div>
                <textarea
                  rows={8}
                  value={resumeText}
                  onChange={(e) => setResumeText(e.target.value)}
                  placeholder="Paste complete candidate resume text here (Summary, Skills, Experience, Education)..."
                  className="w-full glass-input rounded-xl p-3.5 text-xs sm:text-sm font-mono leading-relaxed placeholder:text-slate-600 resize-none min-h-[210px]"
                />
                <div className="flex justify-between items-center mt-1 text-[11px] text-slate-400">
                  <span>{resumeText ? `${resumeText.split(/\s+/).length} words` : '0 words'}</span>
                  {resumeText && (
                    <button onClick={() => setResumeText('')} className="text-rose-400 hover:underline">
                      Clear text
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* RIGHT: Job Description Card */}
        <div className="glass-panel rounded-2xl p-6 relative border border-slate-800 flex flex-col justify-between shadow-xl">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <div className="p-2 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-400">
                  <Briefcase className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-white">2. Target Job Description</h3>
                  <p className="text-xs text-slate-400">Paste job requirements, roles & qualifications</p>
                </div>
              </div>
            </div>

            <div className="mb-2">
              <textarea
                rows={11}
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the target job description here (Responsibilities, Required Skills, Qualifications, Tech Stack)..."
                className="w-full glass-input rounded-xl p-3.5 text-xs sm:text-sm leading-relaxed placeholder:text-slate-600 resize-none min-h-[275px]"
              />
            </div>
            <div className="flex justify-between items-center text-[11px] text-slate-400">
              <span>{jobDescription ? `${jobDescription.split(/\s+/).length} words` : '0 words'}</span>
              {jobDescription && (
                <button onClick={() => setJobDescription('')} className="text-rose-400 hover:underline">
                  Clear description
                </button>
              )}
            </div>
          </div>
        </div>

      </div>

      {/* Screen Action Button */}
      <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4 max-w-md mx-auto">
        <button
          onClick={onScreen}
          disabled={loading || (!resumeFile && !resumeText.trim()) || !jobDescription.trim()}
          className={`w-full py-4 px-8 rounded-xl font-bold text-base flex items-center justify-center gap-3 transition-all duration-300 shadow-xl cursor-pointer ${
            loading || (!resumeFile && !resumeText.trim()) || !jobDescription.trim()
              ? 'bg-slate-800 text-slate-500 border border-slate-700 cursor-not-allowed'
              : 'bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white hover:from-indigo-500 hover:via-purple-500 hover:to-pink-500 hover:shadow-indigo-500/30 hover:scale-[1.02]'
          }`}
        >
          {loading ? (
            <>
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              <span>Analyzing Resume & Keywords...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5 text-yellow-300 animate-pulse" />
              <span>Screen Resume with AI</span>
              <ArrowRight className="w-5 h-5" />
            </>
          )}
        </button>
      </div>

    </div>
  );
}
