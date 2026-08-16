import React, { useEffect } from 'react';
import { Sparkles, Download, MessageSquareCode, CheckCircle2, AlertTriangle, XCircle, Share2, Award, UserCheck } from 'lucide-react';
import confetti from 'canvas-confetti';

export default function MatchScoreCard({ data, onOpenChat, onDownloadPdf }) {
  if (!data) return null;

  const {
    overall_score = 0,
    match_level = 'Moderate Match',
    name = 'Candidate',
    target_role = 'Target Role',
    matched_skills = [],
    missing_skills = [],
    filename = 'resume.pdf'
  } = data;

  // Trigger celebration confetti for high match scores!
  useEffect(() => {
    if (overall_score >= 75) {
      try {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 },
          colors: ['#6366f1', '#a855f7', '#ec4899', '#10b981']
        });
      } catch (e) {
        // Safe fallback
      }
    }
  }, [overall_score]);

  // Color scheme based on score
  const isStrong = overall_score >= 80;
  const isModerate = overall_score >= 60 && overall_score < 80;
  const isWeak = overall_score < 60;

  const scoreColor = isStrong
    ? 'from-emerald-400 to-teal-300 text-emerald-400 stroke-emerald-400'
    : isModerate
    ? 'from-indigo-400 to-purple-400 text-indigo-400 stroke-indigo-500'
    : 'from-amber-400 to-rose-400 text-rose-400 stroke-rose-500';

  const badgeBg = isStrong
    ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30'
    : isModerate
    ? 'bg-indigo-500/10 text-indigo-300 border-indigo-500/30'
    : 'bg-rose-500/10 text-rose-300 border-rose-500/30';

  const StatusIcon = isStrong ? CheckCircle2 : isModerate ? AlertTriangle : XCircle;

  // SVG Circular Ring calculations
  const radius = 68;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (overall_score / 100) * circumference;

  return (
    <div className="relative glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 shadow-2xl overflow-hidden mb-8">
      {/* Ambient background glow */}
      <div className={`absolute -right-16 -top-16 w-80 h-80 rounded-full blur-3xl opacity-20 pointer-events-none ${
        isStrong ? 'bg-emerald-500' : isModerate ? 'bg-indigo-600' : 'bg-rose-500'
      }`} />

      <div className="flex flex-col lg:flex-row items-center justify-between gap-8">
        
        {/* Left Side: Score Details & Candidate Meta */}
        <div className="flex-1 text-center lg:text-left space-y-4">
          
          <div className="flex flex-wrap items-center justify-center lg:justify-start gap-2.5">
            <span className="px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-slate-900 border border-slate-700/80 text-slate-300 flex items-center gap-1.5">
              <Award className="w-3.5 h-3.5 text-indigo-400" />
              AI Match Score
            </span>
            <span className={`px-3 py-1 rounded-full text-xs font-bold border flex items-center gap-1.5 shadow-sm ${badgeBg}`}>
              <StatusIcon className="w-3.5 h-3.5" />
              {match_level}
            </span>
          </div>

          <div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex flex-wrap items-center justify-center lg:justify-start gap-2">
              <span>{name}</span>
              <span className="text-slate-500 font-normal text-xl sm:text-2xl">•</span>
              <span className="text-indigo-300 font-semibold text-lg sm:text-2xl">{target_role}</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Source file: <span className="font-mono text-slate-300">{filename}</span> • Evaluated with TF-IDF semantic review
            </p>
          </div>

          {/* Quick Stats Pill row */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-2 max-w-lg mx-auto lg:mx-0">
            <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
              <div className="text-[11px] text-slate-400 font-medium">Matched Skills</div>
              <div className="text-lg font-bold text-emerald-400 flex items-center gap-1">
                {matched_skills.length}
                <span className="text-[11px] text-slate-400 font-normal">skills</span>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
              <div className="text-[11px] text-slate-400 font-medium">Missing Skills</div>
              <div className="text-lg font-bold text-amber-400 flex items-center gap-1">
                {missing_skills.length}
                <span className="text-[11px] text-slate-400 font-normal">gaps</span>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 col-span-2 sm:col-span-1">
              <div className="text-[11px] text-slate-400 font-medium">ATS Readiness</div>
              <div className="text-lg font-bold text-indigo-300">
                {overall_score >= 80 ? 'High' : overall_score >= 60 ? 'Medium' : 'Needs Work'}
              </div>
            </div>
          </div>

          {/* Action Button CTA Bar */}
          <div className="flex flex-wrap items-center justify-center lg:justify-start gap-3 pt-2">
            <button
              onClick={onOpenChat}
              className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold text-xs sm:text-sm flex items-center gap-2 shadow-lg shadow-indigo-600/30 hover:scale-[1.02] transition-all cursor-pointer"
            >
              <MessageSquareCode className="w-4 h-4" />
              <span>Ask AI Coach</span>
            </button>

            <button
              onClick={onDownloadPdf}
              className="px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 hover:border-indigo-500/50 text-slate-200 hover:text-white font-semibold text-xs sm:text-sm flex items-center gap-2 hover:bg-slate-800 transition-all cursor-pointer"
            >
              <Download className="w-4 h-4 text-indigo-400" />
              <span>Export PDF Report</span>
            </button>
          </div>

        </div>

        {/* Right Side: Circular Gauge Progress Indicator */}
        <div className="relative flex flex-col items-center justify-center p-4">
          <div className="relative w-48 h-48 sm:w-56 sm:h-56 flex items-center justify-center">
            
            <svg className="w-full h-full -rotate-90 transform" viewBox="0 0 160 160">
              {/* Background Track Circle */}
              <circle
                cx="80"
                cy="80"
                r={radius}
                className="stroke-slate-800"
                strokeWidth="12"
                fill="transparent"
              />
              {/* Animated Progress Circle */}
              <circle
                cx="80"
                cy="80"
                r={radius}
                className={`score-circle ${isStrong ? 'stroke-emerald-400' : isModerate ? 'stroke-indigo-500' : 'stroke-rose-500'}`}
                strokeWidth="12"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
                fill="transparent"
              />
            </svg>

            {/* Centered Score Number Display */}
            <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
              <span className="text-4xl sm:text-5xl font-extrabold tracking-tight text-white glow-text">
                {overall_score}%
              </span>
              <span className={`text-xs sm:text-sm font-bold uppercase tracking-wider mt-0.5 ${
                isStrong ? 'text-emerald-400' : isModerate ? 'text-indigo-400' : 'text-rose-400'
              }`}>
                {match_level}
              </span>
            </div>

          </div>

          <p className="text-[11px] text-slate-400 mt-2 text-center">
            Composite AI Match Rating
          </p>
        </div>

      </div>
    </div>
  );
}
