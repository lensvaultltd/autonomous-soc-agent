import React, { useState } from 'react';
import { Shield, Activity, AlertTriangle, CheckCircle, Clock, Server, Terminal, Lock, ChevronRight, User } from 'lucide-react';

// MOCK INCIDENT DATA
const mockIncidents = [
  {
    id: "INC-2026-8891",
    title: "Suspicious PowerShell Execution",
    severity: "Critical",
    status: "Awaiting Human Review",
    host: "FINANCE-LAPTOP-01",
    ai_summary: "Mimikatz detected executing via PowerShell. Tier 2 Agent has isolated the host and paused for human confirmation.",
    timeline: [
      { agent: "Tier 1", action: "Triaged alert from CrowdStrike. Escalated due to high risk score.", time: "10:00 AM" },
      { agent: "Tier 2", action: "Queried Splunk. Found multiple failed logins from IP 198.51.100.4.", time: "10:02 AM" },
      { agent: "Tier 2", action: "RAG Playbook retrieved. Executing step 1: Host Isolation.", time: "10:03 AM" },
      { agent: "Tier 2", action: "Host isolated. Waiting for SOC Manager to approve AD password reset.", time: "10:05 AM" }
    ]
  },
  {
    id: "INC-2026-8892",
    title: "Anomalous Lateral Movement",
    severity: "High",
    status: "Investigating",
    host: "DB-SERVER-04",
    ai_summary: "Threat Hunter detected unusual lateral movement originating from the HR subnet.",
    timeline: [
      { agent: "Threat Hunter", action: "Proactive SPL query detected anomaly. Alert generated.", time: "09:15 AM" },
      { agent: "Tier 1", action: "Triaged and confirmed anomaly. Escalated to Tier 2.", time: "09:16 AM" },
      { agent: "Tier 2", action: "Currently querying Wazuh logs for process trees.", time: "09:18 AM" }
    ]
  }
];

export default function App() {
  const [selectedIncident, setSelectedIncident] = useState(mockIncidents[0]);

  return (
    <div className="min-h-screen flex bg-slate-950">
      
      {/* Sidebar Navigation */}
      <div className="w-64 border-r border-slate-800 bg-slate-900/50 flex flex-col">
        <div className="p-6 border-b border-slate-800 flex items-center gap-3">
          <Shield className="w-8 h-8 text-indigo-500" />
          <div>
            <h1 className="font-bold text-white leading-tight">Lens Vault</h1>
            <p className="text-xs text-slate-500 font-mono tracking-widest uppercase">Project Sentinel</p>
          </div>
        </div>
        <nav className="p-4 space-y-2 flex-1">
          <button className="w-full flex items-center gap-3 px-4 py-3 bg-indigo-500/10 text-indigo-400 rounded-lg font-bold border border-indigo-500/20">
            <Activity className="w-5 h-5" /> SOC Dashboard
          </button>
          <button className="w-full flex items-center gap-3 px-4 py-3 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors">
            <Terminal className="w-5 h-5" /> Active Hunts
          </button>
          <button className="w-full flex items-center gap-3 px-4 py-3 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors">
            <Lock className="w-5 h-5" /> Playbooks
          </button>
        </nav>
        <div className="p-6 border-t border-slate-800 flex items-center gap-3 text-sm">
          <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center border border-slate-700">
            <User className="w-4 h-4 text-slate-400" />
          </div>
          <div>
            <div className="text-white font-bold">Admin User</div>
            <div className="text-slate-500 text-xs">Lens Vault MSSP</div>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar */}
        <header className="h-16 border-b border-slate-800 bg-slate-900/30 flex items-center justify-between px-8">
          <h2 className="text-xl font-bold text-white">Active Incidents</h2>
          <div className="flex gap-4">
            <span className="px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/20 text-rose-500 text-xs font-bold flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>
              2 Critical
            </span>
            <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 text-xs font-bold flex items-center gap-2">
              <CheckCircle className="w-3 h-3" />
              14 Closed Today
            </span>
          </div>
        </header>

        {/* Dashboard Grid */}
        <div className="flex-1 grid grid-cols-12 gap-0 overflow-hidden">
          
          {/* Incident Feed (Left) */}
          <div className="col-span-4 border-r border-slate-800 bg-slate-900/20 overflow-y-auto">
            {mockIncidents.map(inc => (
              <div 
                key={inc.id}
                onClick={() => setSelectedIncident(inc)}
                className={`p-6 border-b border-slate-800 cursor-pointer transition-colors ${selectedIncident.id === inc.id ? 'bg-indigo-900/20 border-l-4 border-l-indigo-500' : 'hover:bg-slate-800/50 border-l-4 border-l-transparent'}`}
              >
                <div className="flex justify-between items-start mb-2">
                  <span className="font-mono text-xs text-slate-500">{inc.id}</span>
                  {inc.severity === 'Critical' ? (
                    <span className="px-2 py-0.5 bg-rose-500/20 text-rose-400 text-[10px] uppercase tracking-wider font-bold rounded">Critical</span>
                  ) : (
                    <span className="px-2 py-0.5 bg-orange-500/20 text-orange-400 text-[10px] uppercase tracking-wider font-bold rounded">High</span>
                  )}
                </div>
                <h3 className="font-bold text-white mb-2">{inc.title}</h3>
                <div className="flex items-center gap-4 text-xs text-slate-400">
                  <span className="flex items-center gap-1"><Server className="w-3 h-3" /> {inc.host}</span>
                  <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {inc.status}</span>
                </div>
              </div>
            ))}
          </div>

          {/* Deep Analysis View (Right) */}
          <div className="col-span-8 p-8 overflow-y-auto bg-slate-950">
            {selectedIncident ? (
              <div className="max-w-4xl mx-auto">
                <div className="flex justify-between items-end mb-8">
                  <div>
                    <h2 className="text-3xl font-bold text-white mb-2">{selectedIncident.title}</h2>
                    <p className="text-slate-400 font-mono text-sm">{selectedIncident.id} • {selectedIncident.host}</p>
                  </div>
                  {selectedIncident.status === "Awaiting Human Review" && (
                    <button className="px-6 py-2 bg-rose-600 hover:bg-rose-500 text-white font-bold rounded-lg transition-colors flex items-center gap-2 shadow-lg shadow-rose-900/20">
                      <AlertTriangle className="w-5 h-5" /> Approve Containment
                    </button>
                  )}
                </div>

                {/* AI Summary Card */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-8">
                  <h3 className="text-sm font-bold text-white uppercase tracking-widest mb-4 flex items-center gap-2">
                    <Activity className="w-4 h-4 text-indigo-400" /> AI Investigation Summary
                  </h3>
                  <p className="text-slate-300 leading-relaxed">
                    {selectedIncident.ai_summary}
                  </p>
                </div>

                {/* AI Execution Timeline */}
                <div>
                  <h3 className="text-sm font-bold text-white uppercase tracking-widest mb-6 flex items-center gap-2">
                    <Clock className="w-4 h-4 text-slate-400" /> LangGraph Execution Timeline
                  </h3>
                  <div className="space-y-6">
                    {selectedIncident.timeline.map((step, i) => (
                      <div key={i} className="flex gap-4">
                        <div className="flex flex-col items-center">
                          <div className="w-3 h-3 rounded-full bg-indigo-500 ring-4 ring-indigo-500/20"></div>
                          {i !== selectedIncident.timeline.length - 1 && (
                            <div className="w-0.5 h-full bg-slate-800 my-2"></div>
                          )}
                        </div>
                        <div className="pb-6">
                          <div className="flex items-center gap-3 mb-1">
                            <span className="font-bold text-white">{step.agent} Agent</span>
                            <span className="text-xs font-mono text-slate-500">{step.time}</span>
                          </div>
                          <p className="text-slate-400 text-sm">{step.action}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

              </div>
            ) : (
              <div className="h-full flex items-center justify-center text-slate-600">
                Select an incident to view AI timeline.
              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}
