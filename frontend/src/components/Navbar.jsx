import React from 'react';
import { Sparkles, Users, GitCompare, MessageSquareCode, FileText, Zap, Key } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, candidateCount, onOpenSettings, onLoadSample }) {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Logo */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('screener')}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center shadow-lg shadow-indigo-500/25">
            <Sparkles className="w-5 h-5 text-white animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-white via-slate-200 to-indigo-300 bg-clip-text text-transparent">
                ResumeIQ
              </span>
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                AI SaaS
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block">Intelligent Screening & Match Scoring</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="hidden md:flex items-center gap-1.5 p-1 rounded-xl bg-slate-900/90 border border-slate-800">
          <button
            onClick={() => setActiveTab('screener')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'screener'
                ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <Zap className="w-3.5 h-3.5" />
            <span>Screen & Score</span>
          </button>

          <button
            onClick={() => setActiveTab('recruiter')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all relative ${
              activeTab === 'recruiter'
                ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <Users className="w-3.5 h-3.5" />
            <span>Recruiter Board</span>
            {candidateCount > 0 && (
              <span className="ml-1 px-1.5 py-0.2 rounded-full bg-indigo-500/20 text-indigo-300 text-[10px] font-bold border border-indigo-500/30">
                {candidateCount}
              </span>
            )}
          </button>

          <button
            onClick={() => setActiveTab('compare')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'compare'
                ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <GitCompare className="w-3.5 h-3.5" />
            <span>Compare</span>
          </button>

          <button
            onClick={() => setActiveTab('coach')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'coach'
                ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <MessageSquareCode className="w-3.5 h-3.5" />
            <span>AI Coach</span>
          </button>
        </nav>

        {/* Right Actions */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => onLoadSample('frontend_dev')}
            className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-900 border border-slate-700/80 text-slate-300 hover:text-white hover:border-indigo-500/50 transition-all shadow-sm"
          >
            <FileText className="w-3.5 h-3.5 text-indigo-400" />
            <span>Load Demo</span>
          </button>

          <button
            onClick={onOpenSettings}
            className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:border-slate-700 transition-all"
            title="Settings"
          >
            <Key className="w-4 h-4" />
          </button>
        </div>

      </div>

      {/* Mobile Tab Bar */}
      <div className="md:hidden flex items-center justify-around border-t border-slate-800/60 bg-slate-950/95 px-2 py-2">
        <button
          onClick={() => setActiveTab('screener')}
          className={`flex flex-col items-center gap-1 text-[10px] font-medium ${activeTab === 'screener' ? 'text-indigo-400' : 'text-slate-400'}`}
        >
          <Zap className="w-4 h-4" />
          <span>Screener</span>
        </button>
        <button
          onClick={() => setActiveTab('recruiter')}
          className={`flex flex-col items-center gap-1 text-[10px] font-medium ${activeTab === 'recruiter' ? 'text-indigo-400' : 'text-slate-400'}`}
        >
          <Users className="w-4 h-4" />
          <span>Pipeline</span>
        </button>
        <button
          onClick={() => setActiveTab('compare')}
          className={`flex flex-col items-center gap-1 text-[10px] font-medium ${activeTab === 'compare' ? 'text-indigo-400' : 'text-slate-400'}`}
        >
          <GitCompare className="w-4 h-4" />
          <span>Compare</span>
        </button>
        <button
          onClick={() => setActiveTab('coach')}
          className={`flex flex-col items-center gap-1 text-[10px] font-medium ${activeTab === 'coach' ? 'text-indigo-400' : 'text-slate-400'}`}
        >
          <MessageSquareCode className="w-4 h-4" />
          <span>AI Coach</span>
        </button>
      </div>
    </header>
  );
}
