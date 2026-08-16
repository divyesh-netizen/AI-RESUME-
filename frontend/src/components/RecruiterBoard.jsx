import React, { useState, useEffect } from 'react';
import { Users, Search, Filter, ArrowUpDown, Trash2, Eye, Download, Sparkles, CheckCircle2, AlertTriangle, XCircle, RefreshCw, Layers, Calendar } from 'lucide-react';

export default function RecruiterBoard({ onSelectCandidate, onViewDetails }) {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [minScore, setMinScore] = useState('all');
  const [skillFilter, setSkillFilter] = useState('');
  const [sortBy, setSortBy] = useState('score');
  const [sortOrder, setSortOrder] = useState('desc');
  const [selectedCandidateModal, setSelectedCandidateModal] = useState(null);

  const fetchCandidates = async () => {
    setLoading(true);
    try {
      let url = `/api/candidates?sort_by=${sortBy}&order=${sortOrder}`;
      if (search) url += `&search=${encodeURIComponent(search)}`;
      if (minScore === '80') url += `&min_score=80`;
      else if (minScore === '60') url += `&min_score=60`;
      if (skillFilter) url += `&skill=${encodeURIComponent(skillFilter)}`;

      const res = await fetch(url);
      const data = await res.json();
      setCandidates(data.candidates || []);
    } catch (err) {
      console.error('Failed to fetch candidates', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCandidates();
  }, [search, minScore, skillFilter, sortBy, sortOrder]);

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm('Are you sure you want to delete this candidate record?')) return;
    try {
      await fetch(`/api/candidates/${id}`, { method: 'DELETE' });
      setCandidates((prev) => prev.filter((c) => c.id !== id));
      if (selectedCandidateModal?.id === id) {
        setSelectedCandidateModal(null);
      }
    } catch (err) {
      console.error('Failed to delete candidate', err);
    }
  };

  const exportCSV = () => {
    if (!candidates.length) return;
    const headers = ['ID', 'Name', 'Email', 'Target Role', 'Overall Score', 'Match Level', 'Job Fit', 'Technical', 'Cultural', 'Communication', 'Matched Skills', 'Date'];
    const rows = candidates.map(c => [
      c.id,
      `"${c.name}"`,
      `"${c.email || ''}"`,
      `"${c.target_role || ''}"`,
      c.overall_score,
      `"${c.match_level}"`,
      c.job_fit_score,
      c.technical_score,
      c.cultural_score,
      c.communication_score,
      `"${(c.matched_skills || []).join(', ')}"`,
      `"${c.created_at}"`
    ]);

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `resumeiq_candidates_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Metric stats
  const totalCount = candidates.length;
  const strongCount = candidates.filter(c => c.overall_score >= 80).length;
  const avgScore = totalCount ? Math.round(candidates.reduce((a, b) => a + b.overall_score, 0) / totalCount) : 0;
  const topCandidate = candidates.length ? [...candidates].sort((a,b) => b.overall_score - a.overall_score)[0] : null;

  return (
    <div className="space-y-6">
      
      {/* Top Metrics Header Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass-panel rounded-2xl p-5 border border-slate-800">
          <span className="text-xs text-slate-400 font-medium">Total Screened</span>
          <div className="text-2xl font-extrabold text-white mt-1 flex items-center justify-between">
            <span>{totalCount}</span>
            <Users className="w-5 h-5 text-indigo-400" />
          </div>
          <span className="text-[11px] text-indigo-400 mt-1 block">Active pipeline pool</span>
        </div>

        <div className="glass-panel rounded-2xl p-5 border border-slate-800">
          <span className="text-xs text-slate-400 font-medium">Strong Matches (80%+)</span>
          <div className="text-2xl font-extrabold text-emerald-400 mt-1 flex items-center justify-between">
            <span>{strongCount}</span>
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          </div>
          <span className="text-[11px] text-emerald-400 mt-1 block">
            {totalCount ? `${Math.round((strongCount / totalCount) * 100)}% of candidates` : '0%'}
          </span>
        </div>

        <div className="glass-panel rounded-2xl p-5 border border-slate-800">
          <span className="text-xs text-slate-400 font-medium">Average Match Score</span>
          <div className="text-2xl font-extrabold text-purple-300 mt-1 flex items-center justify-between">
            <span>{avgScore}%</span>
            <Sparkles className="w-5 h-5 text-purple-400" />
          </div>
          <span className="text-[11px] text-purple-400 mt-1 block">Across all positions</span>
        </div>

        <div className="glass-panel rounded-2xl p-5 border border-slate-800">
          <span className="text-xs text-slate-400 font-medium">Top Rank Candidate</span>
          <div className="text-xl font-extrabold text-white mt-1 truncate">
            {topCandidate ? topCandidate.name : 'N/A'}
          </div>
          <span className="text-[11px] text-emerald-400 mt-1 block truncate">
            {topCandidate ? `${topCandidate.overall_score}% • ${topCandidate.target_role}` : 'No records'}
          </span>
        </div>
      </div>

      {/* Filter and Action Toolbar */}
      <div className="glass-panel rounded-2xl p-4 sm:p-5 border border-slate-800 flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-4">
        
        {/* Search & Filters */}
        <div className="flex flex-wrap items-center gap-3 flex-1">
          {/* Search Input */}
          <div className="relative flex-1 min-w-[200px]">
            <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search candidate name or role..."
              className="w-full glass-input rounded-xl pl-9 pr-3 py-2 text-xs sm:text-sm placeholder:text-slate-500"
            />
          </div>

          {/* Min Score Filter */}
          <div className="flex items-center gap-1.5 bg-slate-900 px-3 py-1.5 rounded-xl border border-slate-800 text-xs">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={minScore}
              onChange={(e) => setMinScore(e.target.value)}
              className="bg-transparent text-slate-300 focus:outline-none cursor-pointer"
            >
              <option value="all" className="bg-slate-900">All Scores</option>
              <option value="80" className="bg-slate-900">Strong (80%+)</option>
              <option value="60" className="bg-slate-900">Moderate (60%+)</option>
            </select>
          </div>

          {/* Sort By Selector */}
          <div className="flex items-center gap-1.5 bg-slate-900 px-3 py-1.5 rounded-xl border border-slate-800 text-xs">
            <ArrowUpDown className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={`${sortBy}_${sortOrder}`}
              onChange={(e) => {
                const [sb, so] = e.target.value.split('_');
                setSortBy(sb);
                setSortOrder(so);
              }}
              className="bg-transparent text-slate-300 focus:outline-none cursor-pointer"
            >
              <option value="score_desc" className="bg-slate-900">Score: High to Low</option>
              <option value="score_asc" className="bg-slate-900">Score: Low to High</option>
              <option value="created_at_desc" className="bg-slate-900">Date: Newest</option>
              <option value="created_at_asc" className="bg-slate-900">Date: Oldest</option>
            </select>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={fetchCandidates}
            className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white transition-colors"
            title="Refresh Candidate Pipeline"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>

          <button
            onClick={exportCSV}
            disabled={!candidates.length}
            className="px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700/80 hover:border-indigo-500/50 text-slate-200 text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer"
          >
            <Download className="w-3.5 h-3.5 text-indigo-400" />
            <span>Export CSV</span>
          </button>
        </div>

      </div>

      {/* Candidate Pipeline Table */}
      <div className="glass-panel rounded-3xl border border-slate-800 overflow-hidden shadow-2xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-800/80 bg-slate-900/60 text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                <th className="py-4 px-6">Candidate</th>
                <th className="py-4 px-4">Target Role</th>
                <th className="py-4 px-4">Match Score</th>
                <th className="py-4 px-4 hidden md:table-cell">Sub-Score Breakdown</th>
                <th className="py-4 px-4 hidden lg:table-cell">Matched Skills</th>
                <th className="py-4 px-4 hidden sm:table-cell">Date</th>
                <th className="py-4 px-6 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs sm:text-sm">
              {candidates.length > 0 ? (
                candidates.map((cand) => {
                  const isStrong = cand.overall_score >= 80;
                  const isModerate = cand.overall_score >= 60 && cand.overall_score < 80;
                  const scoreBadgeBg = isStrong
                    ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30'
                    : isModerate
                    ? 'bg-indigo-500/10 text-indigo-300 border-indigo-500/30'
                    : 'bg-rose-500/10 text-rose-300 border-rose-500/30';

                  return (
                    <tr
                      key={cand.id}
                      onClick={() => setSelectedCandidateModal(cand)}
                      className="hover:bg-slate-900/50 transition-colors cursor-pointer group"
                    >
                      {/* Candidate Column */}
                      <td className="py-4 px-6">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center font-bold text-white shadow-md shadow-indigo-600/20 shrink-0">
                            {cand.name.charAt(0)}
                          </div>
                          <div>
                            <div className="font-bold text-white group-hover:text-indigo-300 transition-colors">
                              {cand.name}
                            </div>
                            <div className="text-xs text-slate-400 font-mono">
                              {cand.email || cand.filename || 'Direct Text Screening'}
                            </div>
                          </div>
                        </div>
                      </td>

                      {/* Target Role */}
                      <td className="py-4 px-4">
                        <span className="font-medium text-slate-200">{cand.target_role}</span>
                      </td>

                      {/* Match Score */}
                      <td className="py-4 px-4">
                        <div className="flex items-center gap-2">
                          <span className={`text-base font-extrabold px-2.5 py-1 rounded-xl border ${scoreBadgeBg}`}>
                            {cand.overall_score}%
                          </span>
                          <span className="text-[11px] text-slate-400 hidden xl:inline">
                            {cand.match_level}
                          </span>
                        </div>
                      </td>

                      {/* Sub-Score Breakdown */}
                      <td className="py-4 px-4 hidden md:table-cell">
                        <div className="flex items-center gap-1.5 text-[10px]">
                          <span className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300" title="Job Fit">
                            Fit: {cand.job_fit_score}%
                          </span>
                          <span className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-emerald-300" title="Technical Skills">
                            Tech: {cand.technical_score}%
                          </span>
                          <span className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-indigo-300" title="Cultural Fit">
                            Cult: {cand.cultural_score}%
                          </span>
                        </div>
                      </td>

                      {/* Matched Skills */}
                      <td className="py-4 px-4 hidden lg:table-cell">
                        <div className="flex flex-wrap gap-1 max-w-xs">
                          {(cand.matched_skills || []).slice(0, 3).map((skill, i) => (
                            <span key={i} className="px-2 py-0.5 rounded-md text-[10px] font-medium bg-emerald-950/40 text-emerald-300 border border-emerald-500/20">
                              {skill}
                            </span>
                          ))}
                          {(cand.matched_skills || []).length > 3 && (
                            <span className="px-1.5 py-0.5 rounded-md text-[10px] text-slate-400 bg-slate-900 border border-slate-800">
                              +{(cand.matched_skills || []).length - 3}
                            </span>
                          )}
                        </div>
                      </td>

                      {/* Date */}
                      <td className="py-4 px-4 hidden sm:table-cell text-slate-400 text-xs">
                        <div className="flex items-center gap-1">
                          <Calendar className="w-3.5 h-3.5 text-slate-500" />
                          <span>{cand.created_at ? cand.created_at.slice(0, 10) : 'Today'}</span>
                        </div>
                      </td>

                      {/* Actions */}
                      <td className="py-4 px-6 text-right">
                        <div className="flex items-center justify-end gap-2" onClick={(e) => e.stopPropagation()}>
                          <button
                            onClick={() => onSelectCandidate(cand)}
                            className="p-2 rounded-lg bg-slate-900 hover:bg-indigo-600 hover:text-white text-slate-400 transition-colors"
                            title="Load into Screener & AI Coach"
                          >
                            <Eye className="w-4 h-4" />
                          </button>
                          <button
                            onClick={(e) => handleDelete(cand.id, e)}
                            className="p-2 rounded-lg bg-slate-900 hover:bg-rose-600 hover:text-white text-slate-400 transition-colors"
                            title="Delete Candidate"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-400">
                    {loading ? (
                      <div className="flex flex-col items-center justify-center gap-2">
                        <div className="w-6 h-6 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
                        <span>Loading candidate database...</span>
                      </div>
                    ) : (
                      <div className="flex flex-col items-center justify-center gap-2">
                        <Users className="w-8 h-8 text-slate-600" />
                        <p className="text-sm font-semibold text-slate-300">No candidates found</p>
                        <p className="text-xs text-slate-500">Screen your first resume or adjust your filters above</p>
                      </div>
                    )}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Candidate Profile Modal */}
      {selectedCandidateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
          <div className="glass-panel rounded-3xl p-6 sm:p-8 max-w-2xl w-full border border-slate-700 shadow-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-5">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center font-bold text-lg text-white">
                  {selectedCandidateModal.name.charAt(0)}
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white">{selectedCandidateModal.name}</h3>
                  <p className="text-xs text-slate-400">{selectedCandidateModal.target_role} • Score: {selectedCandidateModal.overall_score}% ({selectedCandidateModal.match_level})</p>
                </div>
              </div>
              <button
                onClick={() => setSelectedCandidateModal(null)}
                className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            {/* Score Grid */}
            <div className="grid grid-cols-4 gap-2.5 mb-5 text-center">
              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                <div className="text-[10px] text-slate-400">Job Fit</div>
                <div className="text-sm font-bold text-white">{selectedCandidateModal.job_fit_score}%</div>
              </div>
              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                <div className="text-[10px] text-slate-400">Technical</div>
                <div className="text-sm font-bold text-emerald-400">{selectedCandidateModal.technical_score}%</div>
              </div>
              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                <div className="text-[10px] text-slate-400">Cultural</div>
                <div className="text-sm font-bold text-indigo-300">{selectedCandidateModal.cultural_score}%</div>
              </div>
              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                <div className="text-[10px] text-slate-400">Comm</div>
                <div className="text-sm font-bold text-purple-300">{selectedCandidateModal.communication_score}%</div>
              </div>
            </div>

            {/* Matched & Missing Skills */}
            <div className="space-y-4 mb-6">
              <div>
                <span className="text-xs font-bold text-emerald-400 block mb-1.5">Matched Skills ({selectedCandidateModal.matched_skills?.length || 0}):</span>
                <div className="flex flex-wrap gap-1.5">
                  {(selectedCandidateModal.matched_skills || []).map((s, i) => (
                    <span key={i} className="px-2.5 py-1 rounded-lg text-xs bg-emerald-950/40 text-emerald-300 border border-emerald-500/20">
                      {s}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <span className="text-xs font-bold text-amber-400 block mb-1.5">Missing Skills ({selectedCandidateModal.missing_skills?.length || 0}):</span>
                <div className="flex flex-wrap gap-1.5">
                  {(selectedCandidateModal.missing_skills || []).map((s, i) => (
                    <span key={i} className="px-2.5 py-1 rounded-lg text-xs bg-amber-950/40 text-amber-300 border border-amber-500/20">
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Modal Actions */}
            <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
              <button
                onClick={() => {
                  onSelectCandidate(selectedCandidateModal);
                  setSelectedCandidateModal(null);
                }}
                className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-colors"
              >
                Load into Screener View
              </button>
            </div>

          </div>
        </div>
      )}

    </div>
  );
}
