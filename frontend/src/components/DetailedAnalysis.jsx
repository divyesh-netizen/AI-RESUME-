import React, { useState } from 'react';
import { ChevronDown, ChevronUp, FileSearch, CheckCircle2, AlertCircle, Award, Lightbulb, Sparkles, BookOpen, Layers, ArrowRight } from 'lucide-react';

export default function DetailedAnalysis({ data }) {
  if (!data) return null;

  const [openSections, setOpenSections] = useState({
    explanation: true,
    atsChecklist: true,
    roadmap: true,
    bulletRewriter: false
  });

  const toggleSection = (key) => {
    setOpenSections((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const {
    overall_score = 0,
    job_fit_score = 0,
    technical_score = 0,
    cultural_score = 0,
    communication_score = 0,
    matched_skills = [],
    missing_skills = [],
    ats_recommendations = [],
    detailed_analysis = {}
  } = data;

  const {
    score_explanation = '',
    semantic_similarity_pct = 0,
    skill_coverage_pct = 0,
    action_verb_count = 0,
    metrics_found_count = 0,
    recommended_certifications = [],
    recommended_projects = []
  } = detailed_analysis;

  return (
    <div className="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 shadow-xl mb-8">
      <div className="flex items-center justify-between mb-6 pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
            <FileSearch className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-xl font-extrabold text-white">Comprehensive ATS & Match Audit</h3>
            <p className="text-xs text-slate-400">In-depth mathematical breakdown, ATS checklist & career improvement roadmap</p>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        
        {/* ACCORDION 1: Mathematical & Semantic Score Explanation */}
        <div className="border border-slate-800 rounded-2xl overflow-hidden bg-slate-900/40">
          <button
            onClick={() => toggleSection('explanation')}
            className="w-full px-5 py-4 flex items-center justify-between text-left hover:bg-slate-900/80 transition-colors"
          >
            <div className="flex items-center gap-2.5">
              <Sparkles className="w-4 h-4 text-indigo-400" />
              <span className="text-sm font-bold text-white">Score Calculation & Mathematical Breakdown</span>
            </div>
            {openSections.explanation ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
          </button>

          {openSections.explanation && (
            <div className="px-5 pb-5 pt-1 text-xs sm:text-sm text-slate-300 space-y-4 border-t border-slate-800/60">
              <p className="leading-relaxed text-slate-300 bg-slate-900/80 p-3.5 rounded-xl border border-slate-800">
                {score_explanation}
              </p>

              {/* 4 Metric Badges Grid */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="text-[11px] text-slate-400 block">TF-IDF Vector Relevance</span>
                  <span className="text-base font-bold text-indigo-300">{semantic_similarity_pct}%</span>
                </div>
                <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="text-[11px] text-slate-400 block">Skill Coverage Ratio</span>
                  <span className="text-base font-bold text-emerald-400">{skill_coverage_pct}%</span>
                </div>
                <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="text-[11px] text-slate-400 block">Active Action Verbs</span>
                  <span className="text-base font-bold text-purple-300">{action_verb_count} verbs</span>
                </div>
                <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="text-[11px] text-slate-400 block">Quantifiable Metrics</span>
                  <span className="text-base font-bold text-cyan-300">{metrics_found_count} data points</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* ACCORDION 2: ATS Optimization Recommendations */}
        <div className="border border-slate-800 rounded-2xl overflow-hidden bg-slate-900/40">
          <button
            onClick={() => toggleSection('atsChecklist')}
            className="w-full px-5 py-4 flex items-center justify-between text-left hover:bg-slate-900/80 transition-colors"
          >
            <div className="flex items-center gap-2.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span className="text-sm font-bold text-white">ATS Compliance & Resume Optimization Suggestions</span>
            </div>
            {openSections.atsChecklist ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
          </button>

          {openSections.atsChecklist && (
            <div className="px-5 pb-5 pt-1 space-y-3 border-t border-slate-800/60">
              {ats_recommendations.map((item, idx) => (
                <div
                  key={idx}
                  className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
                >
                  <div className="flex items-start gap-2.5">
                    <div className="p-1 rounded-md bg-indigo-500/10 text-indigo-400 mt-0.5">
                      <Lightbulb className="w-4 h-4" />
                    </div>
                    <div>
                      <span className="text-xs font-bold text-indigo-300 block">{item.category}</span>
                      <p className="text-xs text-slate-300 mt-0.5 leading-relaxed">{item.recommendation}</p>
                    </div>
                  </div>
                  <span className={`text-[10px] font-extrabold uppercase px-2.5 py-1 rounded-full shrink-0 self-start sm:self-center ${
                    item.impact === 'High' ? 'bg-rose-500/10 text-rose-300 border border-rose-500/30' : 'bg-amber-500/10 text-amber-300 border border-amber-500/30'
                  }`}>
                    {item.impact} Impact
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* ACCORDION 3: Recommended Certifications & Projects */}
        <div className="border border-slate-800 rounded-2xl overflow-hidden bg-slate-900/40">
          <button
            onClick={() => toggleSection('roadmap')}
            className="w-full px-5 py-4 flex items-center justify-between text-left hover:bg-slate-900/80 transition-colors"
          >
            <div className="flex items-center gap-2.5">
              <Award className="w-4 h-4 text-purple-400" />
              <span className="text-sm font-bold text-white">Recommended Certifications & Portfolio Roadmap</span>
            </div>
            {openSections.roadmap ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
          </button>

          {openSections.roadmap && (
            <div className="px-5 pb-5 pt-1 space-y-4 border-t border-slate-800/60">
              {/* Certifications */}
              <div>
                <h5 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <Award className="w-3.5 h-3.5 text-purple-400" /> Target Industry Certifications:
                </h5>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                  {recommended_certifications.map((cert, idx) => (
                    <div key={idx} className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs font-semibold text-purple-200 flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-purple-400 shrink-0" />
                      <span>{cert}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Standout Projects */}
              <div>
                <h5 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <Layers className="w-3.5 h-3.5 text-indigo-400" /> Standout Projects to Bridge Gaps:
                </h5>
                <div className="space-y-2">
                  {recommended_projects.map((proj, idx) => (
                    <div key={idx} className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300 flex items-start gap-2.5">
                      <ArrowRight className="w-3.5 h-3.5 text-indigo-400 shrink-0 mt-0.5" />
                      <span>{proj}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* ACCORDION 4: Interactive Bullet Point Rewriter */}
        <div className="border border-slate-800 rounded-2xl overflow-hidden bg-slate-900/40">
          <button
            onClick={() => toggleSection('bulletRewriter')}
            className="w-full px-5 py-4 flex items-center justify-between text-left hover:bg-slate-900/80 transition-colors"
          >
            <div className="flex items-center gap-2.5">
              <BookOpen className="w-4 h-4 text-cyan-400" />
              <span className="text-sm font-bold text-white">Before vs After Bullet Point Formulas (X-Y-Z Method)</span>
            </div>
            {openSections.bulletRewriter ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
          </button>

          {openSections.bulletRewriter && (
            <div className="px-5 pb-5 pt-1 space-y-3 border-t border-slate-800/60">
              <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800">
                <div className="text-[11px] font-bold text-rose-400 mb-1">❌ Weak / Passive Bullet:</div>
                <p className="text-xs text-slate-400 italic mb-2">"Worked on frontend performance and fixed React components."</p>
                <div className="text-[11px] font-bold text-emerald-400 mb-1">✅ High-Impact ATS Rewrite:</div>
                <p className="text-xs text-slate-200 font-medium">"Spearheaded React and TypeScript performance refactoring, slashing average bundle size by 42% and raising Lighthouse score to 96 for 250k+ active users."</p>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800">
                <div className="text-[11px] font-bold text-rose-400 mb-1">❌ Weak / Passive Bullet:</div>
                <p className="text-xs text-slate-400 italic mb-2">"Helped with database optimizations and API calls."</p>
                <div className="text-[11px] font-bold text-emerald-400 mb-1">✅ High-Impact ATS Rewrite:</div>
                <p className="text-xs text-slate-200 font-medium">"Architected RESTful microservices with PostgreSQL and Redis caching, cutting p99 database query latency from 420ms to 65ms across 12M+ monthly transactions."</p>
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
