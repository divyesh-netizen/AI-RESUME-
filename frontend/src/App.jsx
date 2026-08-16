import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import HeroUploader from './components/HeroUploader';
import MatchScoreCard from './components/MatchScoreCard';
import SubScoreBreakdown from './components/SubScoreBreakdown';
import StrengthsWeaknesses from './components/StrengthsWeaknesses';
import DetailedAnalysis from './components/DetailedAnalysis';
import AIChatbot from './components/AIChatbot';
import RecruiterBoard from './components/RecruiterBoard';
import CandidateComparison from './components/CandidateComparison';
import PDFReportModal from './components/PDFReportModal';
import SettingsModal from './components/SettingsModal';
import { Sparkles, Shield, Check, AlertCircle } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('screener'); // 'screener', 'recruiter', 'compare', 'coach'
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [candidateName, setCandidateName] = useState('');
  
  const [screeningResult, setScreeningResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const [sampleData, setSampleData] = useState(null);
  const [candidateCount, setCandidateCount] = useState(0);
  
  const [showPdfModal, setShowPdfModal] = useState(false);
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [apiKey, setApiKey] = useState(localStorage.getItem('resumeiq_api_key') || '');

  // Fetch initial sample data and candidate count
  useEffect(() => {
    fetch('/api/sample-data')
      .then(res => res.json())
      .then(data => {
        setSampleData(data);
        // Preload default sample for an immediate impressive first impression
        if (data?.frontend_dev) {
          setResumeText(data.frontend_dev.resume);
          setJobDescription(data.frontend_dev.job_description);
          setCandidateName(data.frontend_dev.candidate_name);
        }
      })
      .catch(err => console.log('Sample data load notice:', err));

    fetchCandidateCount();
  }, []);

  const fetchCandidateCount = async () => {
    try {
      const res = await fetch('/api/candidates');
      const data = await res.json();
      setCandidateCount(data.total || 0);
    } catch (err) {
      console.log('Count fetch notice:', err);
    }
  };

  const handleLoadSample = (sampleKey) => {
    if (!sampleData || !sampleData[sampleKey]) return;
    const sample = sampleData[sampleKey];
    setResumeFile(null);
    setResumeText(sample.resume);
    setJobDescription(sample.job_description);
    setCandidateName(sample.candidate_name);
    setActiveTab('screener');
    setError(null);
  };

  const handleScreen = async () => {
    setError(null);
    setLoading(true);

    try {
      const formData = new FormData();
      if (resumeFile) {
        formData.append('resume_file', resumeFile);
      } else if (resumeText.trim()) {
        formData.append('resume_text', resumeText.trim());
      } else {
        throw new Error('Please provide a resume file or paste resume text.');
      }

      formData.append('job_description', jobDescription.trim());
      if (candidateName.trim()) {
        formData.append('candidate_name', candidateName.trim());
      }
      formData.append('save_to_db', 'true');

      const response = await fetch('/api/screen', {
        method: 'POST',
        body: formData
      });

      const resData = await response.json();

      if (!response.ok || !resData.success) {
        throw new Error(resData.detail || 'Screening failed. Please check inputs.');
      }

      setScreeningResult(resData.data);
      fetchCandidateCount();

      // Scroll smoothly to score results
      setTimeout(() => {
        const resultsElement = document.getElementById('screening-results');
        if (resultsElement) {
          resultsElement.scrollIntoView({ behavior: 'smooth' });
        }
      }, 150);

    } catch (err) {
      setError(err.message || 'An error occurred during resume screening.');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectCandidate = (candidate) => {
    setScreeningResult(candidate);
    setResumeText(candidate.resume_text || '');
    setJobDescription(candidate.job_description || '');
    setCandidateName(candidate.name || '');
    setResumeFile(null);
    setActiveTab('screener');
    setTimeout(() => {
      const resultsElement = document.getElementById('screening-results');
      if (resultsElement) {
        resultsElement.scrollIntoView({ behavior: 'smooth' });
      }
    }, 150);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-indigo-500/30 selection:text-indigo-200">
      
      {/* SaaS Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        candidateCount={candidateCount}
        onOpenSettings={() => setShowSettingsModal(true)}
        onLoadSample={handleLoadSample}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Error Notification Alert */}
        {error && (
          <div className="mb-6 p-4 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-300 flex items-center justify-between text-xs sm:text-sm">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5 shrink-0" />
              <span>{error}</span>
            </div>
            <button onClick={() => setError(null)} className="text-rose-400 hover:text-white font-bold">
              ✕
            </button>
          </div>
        )}

        {/* TAB 1: SCREENER & SCORE ANALYZER */}
        {activeTab === 'screener' && (
          <div className="space-y-10">
            
            {/* Input Hero Section */}
            <HeroUploader
              resumeFile={resumeFile}
              setResumeFile={setResumeFile}
              resumeText={resumeText}
              setResumeText={setResumeText}
              jobDescription={jobDescription}
              setJobDescription={setJobDescription}
              candidateName={candidateName}
              setCandidateName={setCandidateName}
              onScreen={handleScreen}
              loading={loading}
              sampleData={sampleData}
              onLoadSample={handleLoadSample}
            />

            {/* Results Dashboard Section */}
            {screeningResult && (
              <div id="screening-results" className="pt-6 space-y-8 animate-fadeIn">
                
                {/* 1. Large Top Match Score Card */}
                <MatchScoreCard
                  data={screeningResult}
                  onOpenChat={() => setActiveTab('coach')}
                  onDownloadPdf={() => setShowPdfModal(true)}
                />

                {/* 2. 4 Sub-Score Metric Breakdown Cards */}
                <SubScoreBreakdown data={screeningResult} />

                {/* 3. Strengths & Areas for Growth (2 Columns) */}
                <StrengthsWeaknesses data={screeningResult} />

                {/* 4. Collapsible In-Depth ATS Audit & Roadmap */}
                <DetailedAnalysis data={screeningResult} />

              </div>
            )}

          </div>
        )}

        {/* TAB 2: RECRUITER PIPELINE BOARD */}
        {activeTab === 'recruiter' && (
          <div className="space-y-6 animate-fadeIn">
            <RecruiterBoard
              onSelectCandidate={handleSelectCandidate}
            />
          </div>
        )}

        {/* TAB 3: CANDIDATE COMPARISON */}
        {activeTab === 'compare' && (
          <div className="space-y-6 animate-fadeIn">
            <CandidateComparison sampleData={sampleData} />
          </div>
        )}

        {/* TAB 4: AI COACH CHATBOT */}
        {activeTab === 'coach' && (
          <div className="max-w-4xl mx-auto space-y-6 animate-fadeIn">
            <AIChatbot
              currentScreening={screeningResult}
              apiKey={apiKey}
            />
          </div>
        )}

      </main>

      {/* Printable PDF Report Modal */}
      {showPdfModal && screeningResult && (
        <PDFReportModal
          data={screeningResult}
          onClose={() => setShowPdfModal(false)}
        />
      )}

      {/* Settings Modal */}
      {showSettingsModal && (
        <SettingsModal
          apiKey={apiKey}
          setApiKey={setApiKey}
          onClose={() => setShowSettingsModal(false)}
        />
      )}

      {/* SaaS Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-8 mt-16 text-center text-xs text-slate-400 no-print">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-indigo-400" />
            <span className="font-semibold text-slate-300">ResumeIQ SaaS Platform</span>
            <span>• AI-Powered Resume Screening Engine</span>
          </div>
          <p className="text-slate-400">
            Powered by TF-IDF Semantic Embeddings & 500+ Skill Taxonomy
          </p>
        </div>
      </footer>

    </div>
  );
}
