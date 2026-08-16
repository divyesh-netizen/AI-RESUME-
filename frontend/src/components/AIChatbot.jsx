import React, { useState, useRef, useEffect } from 'react';
import { MessageSquareCode, Send, Sparkles, User, Bot, Trash2, Copy, Check, CornerDownLeft, Lightbulb } from 'lucide-react';

export default function AIChatbot({ currentScreening, apiKey }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'ai',
      text: `### 👋 Hi there! I'm your AI Resume & Career Coach.
I have analyzed your resume against the target job description. You can ask me anything, such as:
- **"How can I boost my match score to 90%+?"**
- **"What high-priority skills am I missing?"**
- **"Rewrite my work experience bullets with quantifiable metrics"**
- **"Am I ready for an interview for this position?"**

Click any suggestion below or type your question to get started!`,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  const messagesEndRef = useRef(null);

  const quickPrompts = [
    'How can I improve my resume?',
    'What skills should I add?',
    'Am I fit for this role?',
    'Rewrite bullet points with high-impact action verbs',
    'What certifications and projects should I pursue?'
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSendMessage = async (textToSend) => {
    const text = textToSend || inputMessage;
    if (!text.trim() || loading) return;

    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text: text.trim(),
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text.trim(),
          resume_text: currentScreening?.resume_text || '',
          job_description: currentScreening?.job_description || '',
          screening_data: currentScreening || null,
          api_key: apiKey || null
        })
      });

      const result = await response.json();
      if (result.success) {
        const aiMsg = {
          id: Date.now() + 1,
          sender: 'ai',
          text: result.reply,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        setMessages((prev) => [...prev, aiMsg]);
      } else {
        throw new Error('Failed to generate response');
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'ai',
          text: 'I apologize, but I encountered an error communicating with the coaching engine. Please ensure the backend server is running and try again.',
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (id, text) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const clearChat = () => {
    setMessages([
      {
        id: Date.now(),
        sender: 'ai',
        text: 'Chat history cleared. How can I assist you with your resume and career strategy today?',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
    ]);
  };

  // Simple markdown renderer helper for AI messages
  const renderMessageContent = (text) => {
    const lines = text.split('\n');
    return lines.map((line, i) => {
      if (line.startsWith('### ')) {
        return <h4 key={i} className="text-sm sm:text-base font-extrabold text-white mt-2 mb-1">{line.replace('### ', '')}</h4>;
      }
      if (line.startsWith('#### ')) {
        return <h5 key={i} className="text-xs sm:text-sm font-bold text-indigo-300 mt-2 mb-1">{line.replace('#### ', '')}</h5>;
      }
      if (line.startsWith('- ') || line.startsWith('* ')) {
        return (
          <li key={i} className="text-xs sm:text-sm text-slate-200 ml-4 list-disc my-0.5 leading-relaxed">
            {formatBold(line.substring(2))}
          </li>
        );
      }
      if (line.startsWith('> ')) {
        return (
          <blockquote key={i} className="border-l-2 border-indigo-500 pl-3 py-1 my-1.5 text-xs text-indigo-200 bg-indigo-500/10 rounded-r-lg">
            {line.replace('> ', '')}
          </blockquote>
        );
      }
      if (line.trim() === '') {
        return <div key={i} className="h-1.5" />;
      }
      return <p key={i} className="text-xs sm:text-sm text-slate-200 my-0.5 leading-relaxed">{formatBold(line)}</p>;
    });
  };

  const formatBold = (str) => {
    const parts = str.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, index) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={index} className="font-bold text-white">{part.slice(2, -2)}</strong>;
      }
      return part;
    });
  };

  return (
    <div className="glass-panel rounded-3xl p-6 border border-slate-800 shadow-2xl flex flex-col h-[700px]">
      
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-indigo-600/30">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-base font-bold text-white">AI Resume & Career Coach</h3>
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-[10px] text-emerald-400 font-bold uppercase">Live Assistant</span>
            </div>
            <p className="text-xs text-slate-400">
              Personalized feedback grounded in candidate resume & target job description
            </p>
          </div>
        </div>

        <button
          onClick={clearChat}
          className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-rose-400 hover:border-slate-700 transition-colors"
          title="Clear Conversation"
        >
          <Trash2 className="w-4 h-4" />
        </button>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto py-4 px-1 space-y-4">
        {messages.map((msg) => {
          const isAi = msg.sender === 'ai';
          return (
            <div
              key={msg.id}
              className={`flex items-start gap-3 ${isAi ? '' : 'flex-row-reverse'}`}
            >
              <div
                className={`w-8 h-8 rounded-xl shrink-0 flex items-center justify-center text-xs font-bold ${
                  isAi
                    ? 'bg-gradient-to-tr from-indigo-600 to-purple-600 text-white shadow-md shadow-indigo-600/20'
                    : 'bg-slate-700 text-slate-200 border border-slate-600'
                }`}
              >
                {isAi ? <Sparkles className="w-4 h-4" /> : <User className="w-4 h-4" />}
              </div>

              <div
                className={`group relative max-w-[82%] rounded-2xl p-4 text-xs sm:text-sm shadow-md ${
                  isAi
                    ? 'bg-slate-900/90 border border-slate-800 text-slate-200'
                    : 'bg-indigo-600 text-white font-medium'
                }`}
              >
                {/* Content */}
                {isAi ? renderMessageContent(msg.text) : <p className="whitespace-pre-wrap">{msg.text}</p>}

                {/* Footer Time & Copy */}
                <div className={`mt-2 pt-1.5 flex items-center justify-between text-[10px] ${
                  isAi ? 'text-slate-400 border-t border-slate-800/60' : 'text-indigo-200 border-t border-indigo-500/50'
                }`}>
                  <span>{msg.time}</span>
                  {isAi && (
                    <button
                      onClick={() => handleCopy(msg.id, msg.text)}
                      className="opacity-0 group-hover:opacity-100 transition-opacity hover:text-white flex items-center gap-1"
                      title="Copy response"
                    >
                      {copiedId === msg.id ? (
                        <>
                          <Check className="w-3 h-3 text-emerald-400" />
                          <span className="text-emerald-400">Copied</span>
                        </>
                      ) : (
                        <>
                          <Copy className="w-3 h-3" />
                          <span>Copy</span>
                        </>
                      )}
                    </button>
                  )}
                </div>
              </div>
            </div>
          );
        })}

        {loading && (
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center text-white shrink-0">
              <Sparkles className="w-4 h-4 animate-spin" />
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce" />
              <div className="w-2 h-2 rounded-full bg-purple-400 animate-bounce [animation-delay:0.2s]" />
              <div className="w-2 h-2 rounded-full bg-pink-400 animate-bounce [animation-delay:0.4s]" />
              <span className="text-xs text-slate-400 ml-1">AI Coach is reviewing your profile...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompt Pills */}
      <div className="pt-2 pb-3 border-t border-slate-800/80">
        <div className="text-[11px] font-semibold text-slate-400 mb-2 flex items-center gap-1">
          <Lightbulb className="w-3.5 h-3.5 text-yellow-400" /> Quick Prompts:
        </div>
        <div className="flex flex-wrap gap-1.5 overflow-x-auto pb-1">
          {quickPrompts.map((prompt, idx) => (
            <button
              key={idx}
              onClick={() => handleSendMessage(prompt)}
              disabled={loading}
              className="text-[11px] px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:border-indigo-500/50 hover:bg-slate-800 transition-all text-left whitespace-nowrap cursor-pointer"
            >
              {prompt}
            </button>
          ))}
        </div>
      </div>

      {/* Input Box */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage();
        }}
        className="flex items-center gap-2 bg-slate-900 p-2 rounded-2xl border border-slate-800 focus-within:border-indigo-500/80 transition-all"
      >
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Ask AI Coach for resume improvements, interview questions, or project tips..."
          className="flex-1 bg-transparent px-3 py-2 text-xs sm:text-sm text-white placeholder:text-slate-500 focus:outline-none"
        />
        <button
          type="submit"
          disabled={!inputMessage.trim() || loading}
          className={`p-2.5 rounded-xl font-semibold flex items-center justify-center transition-all cursor-pointer ${
            inputMessage.trim() && !loading
              ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md hover:scale-105'
              : 'bg-slate-800 text-slate-500 cursor-not-allowed'
          }`}
        >
          <Send className="w-4 h-4" />
        </button>
      </form>

    </div>
  );
}
