import React from 'react';
import { Briefcase, Code, Users, MessageSquare, TrendingUp, CheckCircle, AlertCircle, HelpCircle } from 'lucide-react';

export default function SubScoreBreakdown({ data }) {
  if (!data) return null;

  const {
    job_fit_score = 0,
    technical_score = 0,
    cultural_score = 0,
    communication_score = 0,
    detailed_analysis = {}
  } = data;

  const getStatus = (score) => {
    if (score >= 80) return { label: 'Excellent', color: 'text-emerald-400', bg: 'bg-emerald-500/10 border-emerald-500/30', bar: 'bg-emerald-500' };
    if (score >= 60) return { label: 'Good', color: 'text-indigo-400', bg: 'bg-indigo-500/10 border-indigo-500/30', bar: 'bg-indigo-500' };
    return { label: 'Needs Improvement', color: 'text-amber-400', bg: 'bg-amber-500/10 border-amber-500/30', bar: 'bg-amber-500' };
  };

  const cards = [
    {
      id: 'job_fit',
      title: 'Job Fit',
      score: job_fit_score,
      icon: Briefcase,
      description: 'Alignment with role scope, experience level & responsibilities',
      ...getStatus(job_fit_score)
    },
    {
      id: 'technical',
      title: 'Technical Skills',
      score: technical_score,
      icon: Code,
      description: 'Match with required tech stack, libraries & domain tools',
      ...getStatus(technical_score)
    },
    {
      id: 'cultural',
      title: 'Cultural Fit',
      score: cultural_score,
      icon: Users,
      description: 'Collaboration, agile mindset, leadership & teamwork',
      ...getStatus(cultural_score)
    },
    {
      id: 'communication',
      title: 'Communication',
      score: communication_score,
      icon: MessageSquare,
      description: 'Action verb usage, quantifiable metrics & ATS readability',
      ...getStatus(communication_score)
    },
  ];

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-indigo-400" />
            Performance Breakdown
          </h3>
          <p className="text-xs text-slate-400">Detailed metric indicators across four core hiring pillars</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {cards.map((card) => {
          const Icon = card.icon;
          return (
            <div
              key={card.id}
              className="glass-card rounded-2xl p-5 border border-slate-800 flex flex-col justify-between"
            >
              <div>
                {/* Header with Icon and Rating Chip */}
                <div className="flex items-center justify-between mb-3">
                  <div className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-indigo-400">
                    <Icon className="w-4 h-4" />
                  </div>
                  <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${card.bg} ${card.color}`}>
                    {card.label}
                  </span>
                </div>

                {/* Title & Score */}
                <div className="mb-3">
                  <div className="text-xs text-slate-400 font-medium">{card.title}</div>
                  <div className="text-2xl font-extrabold text-white mt-0.5">
                    {card.score}%
                  </div>
                </div>

                {/* Progress Bar */}
                <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden mb-3">
                  <div
                    className={`h-full rounded-full transition-all duration-1000 ${card.bar}`}
                    style={{ width: `${card.score}%` }}
                  />
                </div>
              </div>

              {/* Sub-description */}
              <p className="text-[11px] text-slate-400 leading-snug">
                {card.description}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
