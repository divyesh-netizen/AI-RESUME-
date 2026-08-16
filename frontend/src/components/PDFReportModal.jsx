import React from 'react';
import { Download, Printer, X, Sparkles, CheckCircle2, AlertTriangle, FileText, Award } from 'lucide-react';

export default function PDFReportModal({ data, onClose }) {
  if (!data) return null;

  const handlePrint = () => {
    window.print();
  };

  const {
    name = 'Candidate',
    email = '',
    phone = '',
    target_role = 'Software Role',
    overall_score = 0,
    match_level = 'Moderate Match',
    job_fit_score = 0,
    technical_score = 0,
    cultural_score = 0,
    communication_score = 0,
    matched_skills = [],
    missing_skills = [],
    strengths = [],
    weaknesses = [],
    ats_recommendations = [],
    detailed_analysis = {},
    filename = 'resume.pdf'
  } = data;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md overflow-y-auto">
      <div className="bg-slate-900 border border-slate-700 rounded-3xl p-6 sm:p-8 max-w-3xl w-full shadow-2xl my-8 text-slate-100 max-h-[90vh] overflow-y-auto">
        
        {/* Modal Controls (Hidden in Print) */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-6 no-print">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-indigo-400" />
            <h3 className="text-base font-bold text-white">AI Screening & ATS Audit Report</h3>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handlePrint}
              className="px-3.5 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs flex items-center gap-1.5 shadow-md"
            >
              <Printer className="w-4 h-4" />
              <span>Print / Save as PDF</span>
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Printable Report Header */}
        <div className="text-center pb-6 border-b border-slate-800 mb-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-bold mb-2">
            <Sparkles className="w-3.5 h-3.5" /> ResumeIQ AI Screening Report
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">{name}</h1>
          <p className="text-sm font-semibold text-indigo-300 mt-0.5">{target_role}</p>
          <p className="text-xs text-slate-400 mt-1">
            {email && `${email} • `}{phone && `${phone} • `}Evaluated from: {filename}
          </p>
        </div>

        {/* Big Score Card */}
        <div className="p-6 rounded-2xl bg-slate-800/80 border border-slate-700 mb-6 flex flex-col sm:flex-row items-center justify-between gap-6 text-center sm:text-left">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400 block">Overall AI Match Score</span>
            <div className="text-4xl font-extrabold text-white mt-1">
              {overall_score}% <span className="text-base font-semibold text-indigo-300">({match_level})</span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Evaluated with hybrid TF-IDF cosine similarity & skill taxonomy coverage.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-2 text-center text-xs">
            <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-[10px] text-slate-400 block">Job Fit</span>
              <span className="font-bold text-white text-sm">{job_fit_score}%</span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-[10px] text-slate-400 block">Technical</span>
              <span className="font-bold text-emerald-400 text-sm">{technical_score}%</span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-[10px] text-slate-400 block">Cultural</span>
              <span className="font-bold text-indigo-300 text-sm">{cultural_score}%</span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-[10px] text-slate-400 block">Communication</span>
              <span className="font-bold text-purple-300 text-sm">{communication_score}%</span>
            </div>
          </div>
        </div>

        {/* Strengths & Weaknesses */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div className="p-4 rounded-2xl bg-slate-800/50 border border-slate-700">
            <div className="flex items-center gap-2 text-emerald-400 font-bold text-sm mb-3">
              <CheckCircle2 className="w-4 h-4" />
              <span>Key Strengths</span>
            </div>
            <ul className="space-y-2 text-xs text-slate-300">
              {strengths.map((s, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-emerald-400">•</span>
                  <span><strong>{s.title}:</strong> {s.desc}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="p-4 rounded-2xl bg-slate-800/50 border border-slate-700">
            <div className="flex items-center gap-2 text-amber-400 font-bold text-sm mb-3">
              <AlertTriangle className="w-4 h-4" />
              <span>Areas for Improvement</span>
            </div>
            <ul className="space-y-2 text-xs text-slate-300">
              {weaknesses.map((w, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-amber-400">•</span>
                  <span><strong>{w.title}:</strong> {w.desc}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Skills Breakdown */}
        <div className="mb-6 space-y-3">
          <div>
            <span className="text-xs font-bold text-slate-300 block mb-1.5">Matched Skills ({matched_skills.length}):</span>
            <div className="flex flex-wrap gap-1.5">
              {matched_skills.map((s, i) => (
                <span key={i} className="px-2 py-0.5 rounded-md text-[11px] bg-emerald-950/60 text-emerald-300 border border-emerald-500/30">
                  {s}
                </span>
              ))}
            </div>
          </div>

          {missing_skills.length > 0 && (
            <div>
              <span className="text-xs font-bold text-slate-300 block mb-1.5">Missing Skills / Keywords ({missing_skills.length}):</span>
              <div className="flex flex-wrap gap-1.5">
                {missing_skills.map((s, i) => (
                  <span key={i} className="px-2 py-0.5 rounded-md text-[11px] bg-amber-950/60 text-amber-300 border border-amber-500/30">
                    {s}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* ATS Suggestions */}
        <div className="p-4 rounded-2xl bg-slate-800/40 border border-slate-700 text-xs">
          <span className="font-bold text-indigo-300 block mb-2">Priority ATS Optimization Checklist:</span>
          <div className="space-y-2">
            {ats_recommendations.map((rec, idx) => (
              <div key={idx} className="flex items-start gap-2 text-slate-300">
                <span className="text-indigo-400 font-bold">{idx + 1}.</span>
                <span><strong>{rec.category}:</strong> {rec.recommendation}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Report Footer */}
        <div className="mt-6 pt-4 border-t border-slate-800 text-center text-[11px] text-slate-500">
          Generated automatically by ResumeIQ AI Platform • Confidential Screening Assessment
        </div>

      </div>
    </div>
  );
}
