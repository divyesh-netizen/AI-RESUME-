import React, { useState } from 'react';
import { GitCompare, Trophy, Sparkles, CheckCircle2, AlertTriangle, ArrowRight, ShieldCheck, Zap } from 'lucide-react';

export default function CandidateComparison({ sampleData }) {
  const [candidate1, setCandidate1] = useState('frontend_dev');
  const [candidate2, setCandidate2] = useState('fullstack_dev');
  const [comparisonResult, setComparisonResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const runComparison = async () => {
    if (!sampleData) return;
    setLoading(true);
    try {
      const c1Data = sampleData[candidate1];
      const c2Data = sampleData[candidate2];
      
      const payload = {
        job_description: c1Data.job_description,
        candidates: [
          { name: c1Data.candidate_name, resume_text: c1Data.resume },
          { name: c2Data.candidate_name, resume_text: c2Data.resume }
        ]
      };

      const res = await fetch('/api/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      setComparisonResult(data.comparisons);
    } catch (err) {
      console.error('Comparison error', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 shadow-xl">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
            <GitCompare className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-xl font-extrabold text-white">Multi-Candidate Benchmark & Comparison</h2>
            <p className="text-xs text-slate-400">Compare 2 applicants side-by-side against the same job description</p>
          </div>
        </div>

        {/* Candidate Selectors */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 my-6">
          <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800">
            <label className="block text-xs font-semibold text-slate-300 mb-2">Select Candidate 1:</label>
            <select
              value={candidate1}
              onChange={(e) => setCandidate1(e.target.value)}
              className="w-full glass-input rounded-xl p-2.5 text-xs sm:text-sm"
            >
              <option value="frontend_dev" className="bg-slate-900">Alex Morgan (Senior Frontend)</option>
              <option value="fullstack_dev" className="bg-slate-900">Samantha Chen (Full Stack Engineer)</option>
              <option value="ai_engineer" className="bg-slate-900">Dr. Marcus Vance (AI & ML Engineer)</option>
            </select>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800">
            <label className="block text-xs font-semibold text-slate-300 mb-2">Select Candidate 2:</label>
            <select
              value={candidate2}
              onChange={(e) => setCandidate2(e.target.value)}
              className="w-full glass-input rounded-xl p-2.5 text-xs sm:text-sm"
            >
              <option value="fullstack_dev" className="bg-slate-900">Samantha Chen (Full Stack Engineer)</option>
              <option value="frontend_dev" className="bg-slate-900">Alex Morgan (Senior Frontend)</option>
              <option value="ai_engineer" className="bg-slate-900">Dr. Marcus Vance (AI & ML Engineer)</option>
            </select>
          </div>
        </div>

        <button
          onClick={runComparison}
          disabled={loading}
          className="w-full py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-sm flex items-center justify-center gap-2 shadow-lg shadow-indigo-600/30 transition-all cursor-pointer"
        >
          {loading ? (
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <>
              <Sparkles className="w-4 h-4" />
              <span>Run Head-to-Head Benchmark</span>
            </>
          )}
        </button>
      </div>

      {/* Comparison Results Card */}
      {comparisonResult && comparisonResult.length >= 2 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {comparisonResult.map((c, idx) => {
            const isWinner = idx === 0;
            return (
              <div
                key={idx}
                className={`glass-panel rounded-3xl p-6 border relative overflow-hidden shadow-2xl ${
                  isWinner ? 'border-emerald-500/50 bg-emerald-950/10' : 'border-slate-800'
                }`}
              >
                {isWinner && (
                  <div className="absolute top-4 right-4 flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-extrabold border border-emerald-500/40">
                    <Trophy className="w-3.5 h-3.5 text-yellow-400" />
                    Top Match Winner
                  </div>
                )}

                <div className="mb-4">
                  <h3 className="text-xl font-extrabold text-white">{c.name}</h3>
                  <p className="text-xs text-slate-400">{c.target_role}</p>
                </div>

                {/* Score */}
                <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 mb-5 flex items-center justify-between">
                  <div>
                    <span className="text-xs text-slate-400 block font-medium">Overall AI Score</span>
                    <span className="text-3xl font-extrabold text-white">{c.overall_score}%</span>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                    c.overall_score >= 80 ? 'bg-emerald-500/20 text-emerald-300' : 'bg-indigo-500/20 text-indigo-300'
                  }`}>
                    {c.match_level}
                  </span>
                </div>

                {/* Metric Bars */}
                <div className="space-y-2.5 mb-5 text-xs">
                  <div>
                    <div className="flex justify-between text-slate-300 mb-1">
                      <span>Job Fit</span>
                      <span className="font-bold">{c.job_fit_score}%</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                      <div className="bg-indigo-500 h-full rounded-full" style={{ width: `${c.job_fit_score}%` }} />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-slate-300 mb-1">
                      <span>Technical Skills</span>
                      <span className="font-bold">{c.technical_score}%</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                      <div className="bg-emerald-500 h-full rounded-full" style={{ width: `${c.technical_score}%` }} />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-slate-300 mb-1">
                      <span>Cultural Fit</span>
                      <span className="font-bold">{c.cultural_score}%</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                      <div className="bg-purple-500 h-full rounded-full" style={{ width: `${c.cultural_score}%` }} />
                    </div>
                  </div>
                </div>

                {/* Skills */}
                <div>
                  <span className="text-xs font-bold text-slate-300 block mb-2">Matched Core Skills:</span>
                  <div className="flex flex-wrap gap-1.5">
                    {(c.matched_skills || []).slice(0, 6).map((s, i) => (
                      <span key={i} className="px-2 py-0.5 rounded-md text-[10px] bg-slate-900 border border-slate-700 text-slate-300">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>

              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
