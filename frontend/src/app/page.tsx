"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import { BrainCircuit, LayoutDashboard, FileText, Settings, Database, Activity, Search, AlertCircle, CheckCircle, Clock, ToggleLeft, ToggleRight, MessageSquare, RotateCcw } from "lucide-react";

export default function Dashboard() {
  const [incidents, setIncidents] = useState<any[]>([]);
  const [activeIncident, setActiveIncident] = useState<any>(null);
  const [reportText, setReportText] = useState("");
  const [diagnosis, setDiagnosis] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [memoryEnabled, setMemoryEnabled] = useState(true);
  const [feedback, setFeedback] = useState("");
  const [feedbackSubmitting, setFeedbackSubmitting] = useState(false);

  useEffect(() => {
    fetchIncidents();
  }, []);

  const fetchIncidents = async () => {
    try {
      const res = await axios.get("http://localhost:8001/api/incidents");
      setIncidents(res.data);
      const active = res.data.find((i: any) => i.status === "active");
      if (active) setActiveIncident(active);
    } catch (e) {
      console.error(e);
    }
  };

  const seedDemoMemory = async () => {
    try {
      const res = await axios.post("http://localhost:8001/api/demo/seed");
      alert("Demo memories seeded: " + res.data.message);
    } catch (e) {
      console.error(e);
      alert("Failed to seed demo memories");
    }
  };

  const resetDemo = async () => {
    try {
      await axios.post("http://localhost:8001/api/demo/reset");
    } catch (e) {
      console.error(e);
    }
    setDiagnosis(null);
    setReportText("");
    setFeedback("");
    await fetchIncidents();
  };

  const handleDiagnose = async () => {
    if (!reportText) return;
    setLoading(true);
    setDiagnosis(null);
    try {
      const res = await axios.post("http://localhost:8001/api/diagnose", {
        description: reportText,
        services: ["prod-api"],
        memory_enabled: memoryEnabled
      });
      setDiagnosis(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (isCorrect: boolean) => {
    setFeedbackSubmitting(true);
    try {
      await axios.post("http://localhost:8001/api/feedback", {
        incident_id: activeIncident?.id || "INC-DEMO",
        is_correct: isCorrect,
        correction: feedback
      });
      setFeedback("");
      alert("Feedback retained in Hindsight memory.");
    } catch (e) {
      console.error(e);
    } finally {
      setFeedbackSubmitting(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-900 text-slate-50 font-sans">
      {/* Sidebar */}
      <div className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col">
        <div className="p-6 flex items-center gap-3">
          <BrainCircuit className="w-8 h-8 text-blue-500" />
          <span className="text-xl font-semibold tracking-tight">Déjà Vu</span>
        </div>
        <nav className="flex-1 px-4 py-4 space-y-1">
          <a href="#" className="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:text-slate-50 hover:bg-slate-800 transition">
            <LayoutDashboard className="w-5 h-5" /> Dashboard
          </a>
          <a href="#" className="flex items-center gap-3 px-3 py-2 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20">
            <AlertCircle className="w-5 h-5" /> Incidents
          </a>
          <a href="#" className="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:text-slate-50 hover:bg-slate-800 transition">
            <Database className="w-5 h-5" /> Memory Explorer
          </a>
          <a href="#" className="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:text-slate-50 hover:bg-slate-800 transition">
            <Activity className="w-5 h-5" /> Services
          </a>
        </nav>
        <div className="p-4 border-t border-slate-800 space-y-3">
          <button onClick={resetDemo} className="w-full flex items-center justify-center gap-2 px-3 py-2 bg-slate-800 hover:bg-slate-700 rounded text-sm text-slate-300 transition">
            <RotateCcw className="w-4 h-4" /> Reset Demo
          </button>
          <button onClick={seedDemoMemory} className="w-full flex items-center justify-center gap-2 px-3 py-2 bg-slate-700 hover:bg-slate-600 rounded text-sm text-slate-400 transition">
            <FileText className="w-4 h-4" /> Seed Memory
          </button>
          <div className="flex items-center gap-2 text-sm text-slate-500">
            <Settings className="w-4 h-4" /> Settings
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Topbar */}
        <header className="h-16 border-b border-slate-800 flex items-center justify-between px-8 bg-slate-900/50 backdrop-blur-sm z-10">
          <h1 className="text-xl font-medium flex items-center gap-3">
            Incident Workspace
            <span className="text-xs bg-indigo-500/20 text-indigo-400 px-2 py-0.5 rounded-full border border-indigo-500/30">
              Demo Mode
            </span>
          </h1>
          <div className="flex items-center gap-6">
            
            {/* Memory Toggle */}
            <div className="flex items-center gap-2 bg-slate-800/50 px-4 py-1.5 rounded-full border border-slate-700/50 cursor-pointer hover:bg-slate-800 transition" onClick={() => setMemoryEnabled(!memoryEnabled)}>
              <span className="text-sm text-slate-300 font-medium">Hindsight Memory</span>
              {memoryEnabled ? <ToggleRight className="w-6 h-6 text-emerald-400" /> : <ToggleLeft className="w-6 h-6 text-slate-500" />}
            </div>

            <div className="flex items-center gap-2 bg-slate-800/50 px-3 py-1.5 rounded-full border border-slate-700/50 text-sm text-slate-300">
              <Database className="w-4 h-4 text-emerald-400" />
              <span>{incidents.filter(i => i.status === 'resolved').length} retained</span>
            </div>
            <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center font-medium">
              JD
            </div>
          </div>
        </header>

        {/* Dashboard Area */}
        <main className="flex-1 p-8 overflow-y-auto flex gap-6">
          {/* Left Panel: Active Incident Chat */}
          <div className="flex-[3] flex flex-col gap-4">
            <h2 className="text-lg font-medium text-slate-300 flex items-center gap-2">
              Active Incident: <span className="text-white">{activeIncident?.title || "New Investigation"}</span>
            </h2>
            
            <div className="bg-slate-800/40 rounded-xl border border-slate-700/50 p-6 flex-1 flex flex-col">
              <div className="flex-1 overflow-y-auto space-y-6">
                
                {/* User Report */}
                <div className="flex gap-4">
                  <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center shrink-0">
                    <span className="text-sm">JD</span>
                  </div>
                  <div className="bg-slate-700/50 rounded-2xl rounded-tl-sm px-5 py-3 text-slate-200">
                    <p>{activeIncident ? activeIncident.description : "No active incident. Paste symptoms below to start."}</p>
                    <p className="mt-2 text-slate-400 text-sm italic">{reportText}</p>
                  </div>
                </div>

                {/* Agent Response (Diagnosis) */}
                {loading && (
                  <div className="flex gap-4">
                    <div className="w-8 h-8 rounded-full bg-blue-900/50 border border-blue-500/30 flex items-center justify-center shrink-0">
                      <BrainCircuit className="w-4 h-4 text-blue-400 animate-pulse" />
                    </div>
                    <div className="bg-slate-800 rounded-2xl rounded-tl-sm px-5 py-3 text-slate-400 border border-slate-700">
                      {memoryEnabled ? "Recalling similar incidents from Hindsight memory..." : "Analyzing incident with base LLM knowledge (Memory OFF)..."}
                    </div>
                  </div>
                )}

                {diagnosis && (
                  <div className="flex gap-4">
                    <div className="w-8 h-8 rounded-full bg-blue-900 border border-blue-500/50 flex items-center justify-center shrink-0">
                      <BrainCircuit className="w-4 h-4 text-blue-400" />
                    </div>
                    <div className="bg-slate-800 rounded-2xl rounded-tl-sm p-5 border border-slate-700 w-full shadow-lg shadow-black/20">
                      
                      {memoryEnabled && diagnosis.pattern_match && (
                        <div className="flex items-center justify-between mb-4 bg-amber-500/10 p-3 rounded-lg border border-amber-500/20">
                          <div className="flex items-center gap-2 text-amber-400 font-medium text-sm">
                            <Activity className="w-4 h-4" />
                            PATTERN MATCH: {(diagnosis.confidence_score * 100).toFixed(0)}% similar to past incidents
                          </div>
                          <div className="text-xs text-amber-500/70">Memory Influenced Result</div>
                        </div>
                      )}

                      {!memoryEnabled && (
                        <div className="flex items-center justify-between mb-4 bg-slate-700/30 p-3 rounded-lg border border-slate-600/50">
                          <div className="flex items-center gap-2 text-slate-400 font-medium text-sm">
                            <BrainCircuit className="w-4 h-4" />
                            Generic LLM Output (No historical context)
                          </div>
                        </div>
                      )}

                      <div className="space-y-4">
                        <div>
                          <h4 className="text-xs font-semibold text-slate-400 tracking-wider mb-1">ROOT CAUSE ANALYSIS</h4>
                          <p className="text-slate-200">{diagnosis.root_cause_analysis}</p>
                        </div>
                        
                        <div>
                          <h4 className="text-xs font-semibold text-slate-400 tracking-wider mb-1">RECOMMENDED FIX</h4>
                          <div className="bg-slate-900 border border-slate-700/50 rounded-lg p-3 font-mono text-sm text-emerald-400 mt-2">
                            {diagnosis.recommended_fix.split('\n').map((line: string, i: number) => (
                              <div key={i}>{line}</div>
                            ))}
                          </div>
                        </div>

                        {diagnosis.failed_approaches?.length > 0 && memoryEnabled && (
                          <div className="bg-rose-950/20 border border-rose-900/30 rounded-lg p-4 mt-4">
                            <h4 className="text-xs font-semibold text-rose-400 tracking-wider flex items-center gap-2 mb-2">
                              <AlertCircle className="w-4 h-4" />
                              DO NOT TRY (Based on past failures)
                            </h4>
                            <ul className="list-none space-y-1">
                              {diagnosis.failed_approaches.map((app: string, idx: number) => (
                                <li key={idx} className="text-slate-300 text-sm flex items-start gap-2 line-through opacity-70">
                                  <span className="text-rose-500 mt-0.5">✗</span> {app}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>

                      {/* Feedback Loop UI */}
                      <div className="mt-6 pt-4 border-t border-slate-700/50">
                        <h4 className="text-xs font-semibold text-slate-400 tracking-wider mb-3">WAS THIS HELPFUL?</h4>
                        <div className="flex gap-2 mb-3">
                          <button onClick={() => handleFeedback(true)} disabled={feedbackSubmitting} className="flex-1 bg-slate-700/50 hover:bg-emerald-900/30 text-slate-300 hover:text-emerald-400 border border-slate-600 hover:border-emerald-500/50 py-2 rounded transition flex justify-center items-center gap-2 text-sm">
                            <CheckCircle className="w-4 h-4" /> Yes, resolved it
                          </button>
                          <button disabled className="flex-1 bg-slate-700/50 text-slate-500 border border-slate-600 py-2 rounded text-sm cursor-not-allowed">
                            No, didn't work
                          </button>
                        </div>
                        <div className="flex gap-2">
                          <input 
                            type="text" 
                            placeholder="Add correction to memory (e.g., 'Actually needed to bump memory limit too')" 
                            value={feedback}
                            onChange={(e) => setFeedback(e.target.value)}
                            className="flex-1 bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500 text-slate-300"
                          />
                          <button onClick={() => handleFeedback(false)} disabled={!feedback || feedbackSubmitting} className="bg-slate-700 hover:bg-blue-600 disabled:opacity-50 text-white px-4 py-2 rounded text-sm transition">
                            Correct
                          </button>
                        </div>
                      </div>

                    </div>
                  </div>
                )}
              </div>

              {/* Input Area */}
              <div className="mt-4 pt-4 border-t border-slate-700/50">
                <div className="flex gap-2">
                  <input 
                    type="text" 
                    value={reportText}
                    onChange={(e) => setReportText(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleDiagnose()}
                    placeholder="Describe symptoms, paste logs, or paste an alert..."
                    className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
                  />
                  <button 
                    onClick={handleDiagnose}
                    disabled={loading || !reportText}
                    className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded-lg font-medium transition disabled:opacity-50"
                  >
                    Diagnose
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Right Panel: Recalled Incidents */}
          <div className="flex-[2] flex flex-col gap-4">
            <h2 className="text-lg font-medium text-slate-300 flex items-center gap-2">
              <Database className="w-5 h-5 text-emerald-500" />
              Retrieved Context
            </h2>
            <div className="flex flex-col gap-3">
              {!memoryEnabled ? (
                <div className="text-sm text-slate-500 p-6 text-center border border-dashed border-slate-700 rounded-xl bg-slate-800/20">
                  <ToggleLeft className="w-8 h-8 mx-auto mb-2 opacity-50" />
                  Memory is currently OFF.<br/>The agent will respond generically.
                </div>
              ) : diagnosis?.similar_incidents?.length > 0 ? (
                diagnosis.similar_incidents.map((inc: any, i: number) => (
                  <div key={i} className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-4 hover:bg-slate-800 hover:border-slate-600 transition cursor-pointer relative overflow-hidden">
                    {i === 0 && <div className="absolute top-0 left-0 w-1 h-full bg-amber-500"></div>}
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-slate-200">{inc.id}</span>
                      <span className="text-xs bg-slate-700 text-slate-300 px-2 py-0.5 rounded-full border border-slate-600">
                        {i === 0 ? "Strong Match" : "Partial Match"}
                      </span>
                    </div>
                    <p className="text-sm text-slate-400 line-clamp-2 mb-3">{inc.symptoms}</p>
                    <div className="bg-slate-900/50 p-2 rounded border border-slate-700/50 text-xs text-slate-300">
                      <span className="text-emerald-400 font-semibold mr-1">Root cause:</span> 
                      {inc.root_cause}
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-sm text-slate-500 italic p-6 text-center border border-dashed border-slate-700 rounded-xl">
                  Run a diagnosis to retrieve relevant past incidents from Hindsight.
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
