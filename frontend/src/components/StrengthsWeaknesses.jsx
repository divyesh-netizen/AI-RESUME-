import React from 'react';
import { CheckCircle2, AlertTriangle, Sparkles, TrendingUp, ArrowUpRight, ShieldCheck, Zap, X } from 'lucide-react';

export default function StrengthsWeaknesses({ data }) {
  if (!data) return null;

  const {
    strengths = [],
    weaknesses = [],
    matched_skills = [],
    missing_skills = []
  } = data;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      
      {/* LEFT CARD: Strengths */}
      <div className="glass-panel rounded-2xl p-6 border border-slate-800 relative overflow-hidden shadow-xl">
        <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-2xl pointer-events-none" />
        
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
              <CheckCircle2 className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-1.5">
                Key Strengths & Competitive Edges
              </h3>
              <p className="text-xs text-slate-400">Standout qualifications matching the job description</p>
            </div>
          </div>
          <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
            {strengths.length} highlights
          </span>
        </div>

        {/* Strengths List */}
        <div className="space-y-3.5 mb-5">
          {strengths.map((item, index) => (
            <div
              key={index}
              className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/80 hover:border-emerald-500/30 transition-all flex items-start gap-3"
            >
              <div className="mt-0.5 p-1 rounded-lg bg-emerald-500/10 text-emerald-400 shrink-0">
                <Sparkles className="w-3.5 h-3.5" />
              </div>
              <div>
                <h4 className="text-xs sm:text-sm font-bold text-slate-100">{item.title}</h4>
                <p className="text-xs text-slate-400 mt-0.5 leading-relaxed">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Top Matched Skills Quick Tags */}
        {matched_skills.length > 0 && (
          <div className="pt-3 border-t border-slate-800">
            <div className="text-[11px] font-semibold text-slate-400 mb-2 flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              Top Matched Tech Proficiencies:
            </div>
            <div className="flex flex-wrap gap-1.5">
              {matched_skills.slice(0, 8).map((skill, i) => (
                <span
                  key={i}
                  className="px-2.5 py-1 rounded-lg text-xs font-medium bg-emerald-950/40 text-emerald-300 border border-emerald-500/20 flex items-center gap-1"
                >
                  <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                  {skill}
                </span>
              ))}
              {matched_skills.length > 8 && (
                <span className="px-2 py-1 rounded-lg text-xs font-medium bg-slate-900 text-slate-400 border border-slate-800">
                  +{matched_skills.length - 8} more
                </span>
              )}
            </div>
          </div>
        )}
      </div>

      {/* RIGHT CARD: Areas for Growth */}
      <div className="glass-panel rounded-2xl p-6 border border-slate-800 relative overflow-hidden shadow-xl">
        <div className="absolute top-0 right-0 w-32 h-32 bg-amber-500/10 rounded-full blur-2xl pointer-events-none" />

        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
              <AlertTriangle className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-1.5">
                Areas for Growth & Missing Skills
              </h3>
              <p className="text-xs text-slate-400">High-priority skill gaps and resume enhancements</p>
            </div>
          </div>
          <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-300 border border-amber-500/20">
            {weaknesses.length} gaps identified
          </span>
        </div>

        {/* Areas for Growth List */}
        <div className="space-y-3.5 mb-5">
          {weaknesses.map((item, index) => (
            <div
              key={index}
              className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/80 hover:border-amber-500/30 transition-all flex items-start gap-3"
            >
              <div className="mt-0.5 p-1 rounded-lg bg-amber-500/10 text-amber-400 shrink-0">
                <ArrowUpRight className="w-3.5 h-3.5" />
              </div>
              <div>
                <h4 className="text-xs sm:text-sm font-bold text-slate-100">{item.title}</h4>
                <p className="text-xs text-slate-400 mt-0.5 leading-relaxed">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Missing Target Skills Badges */}
        {missing_skills.length > 0 ? (
          <div className="pt-3 border-t border-slate-800">
            <div className="text-[11px] font-semibold text-slate-400 mb-2 flex items-center gap-1">
              <Zap className="w-3.5 h-3.5 text-amber-400" />
              Recommended Keywords to Add:
            </div>
            <div className="flex flex-wrap gap-1.5">
              {missing_skills.map((skill, i) => (
                <span
                  key={i}
                  className="px-2.5 py-1 rounded-lg text-xs font-medium bg-amber-950/40 text-amber-300 border border-amber-500/20 flex items-center gap-1"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />
                  {skill}
                </span>
              ))}
            </div>
          </div>
        ) : (
          <div className="pt-3 border-t border-slate-800 text-xs text-emerald-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4" />
            No major technical keyword gaps detected for this job description!
          </div>
        )}
      </div>

    </div>
  );
}
