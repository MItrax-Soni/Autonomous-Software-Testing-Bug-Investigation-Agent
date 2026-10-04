import React, { useState } from 'react';
import { 
  Bug, 
  ShieldCheck, 
  Sparkles, 
  AlertTriangle, 
  Terminal, 
  Globe, 
  Image, 
  FileCode, 
  ExternalLink,
  CheckCircle2,
  XCircle,
  HelpCircle,
  Maximize2
} from 'lucide-react';
import { BugFinding } from '../types';

interface InvestigationViewProps {
  bugs: BugFinding[];
  onSelectBug?: (bugId: string) => void;
}

export const InvestigationView: React.FC<InvestigationViewProps> = ({ bugs }) => {
  const [selectedBugId, setSelectedBugId] = useState<string | null>(
    bugs.length > 0 ? bugs[0].id : null
  );
  const [evidenceTab, setEvidenceTab] = useState<'console' | 'network' | 'screenshot' | 'dom'>('console');
  const [screenshotModalUrl, setScreenshotModalUrl] = useState<string | null>(null);

  const selectedBug = bugs.find((b) => b.id === selectedBugId) || bugs[0];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-panel p-6 rounded-2xl border-command-border space-y-3">
        <div className="flex items-center space-x-2">
          <Bug className="w-5 h-5 text-cyber-rose" />
          <h2 className="text-sm font-bold font-mono uppercase tracking-wider text-white">
            Root-Cause Diagnostic & Bug Investigation Lab
          </h2>
        </div>
        <p className="text-xs text-slate-400 max-w-3xl">
          Multi-angle diagnostic analysis of failed test executions. Strict boundary enforced between <span className="text-cyber-cyan font-semibold">Verified Evidence</span> (proven facts) and <span className="text-cyber-violet font-semibold">AI Hypotheses</span> (probabilistic root causes).
        </p>
      </div>

      {bugs.length === 0 ? (
        <div className="glass-panel p-16 rounded-2xl border-command-border text-center space-y-4">
          <div className="w-12 h-12 rounded-full bg-cyber-emerald/10 border border-cyber-emerald/30 text-cyber-emerald flex items-center justify-center mx-auto">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <h3 className="text-sm font-semibold text-white">No Defects Detected</h3>
          <p className="text-xs text-slate-400 max-w-md mx-auto">
            All executed test scenarios passed without failures, console errors, or network regressions.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left: Bug List */}
          <div className="glass-panel p-5 rounded-2xl border-command-border space-y-4">
            <div className="flex items-center justify-between border-b border-command-border/60 pb-3">
              <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-white">
                Detected Bugs ({bugs.length})
              </h3>
              <span className="text-[10px] font-mono text-slate-400">TRIAGED BY GEMINI</span>
            </div>

            <div className="space-y-2.5 max-h-[600px] overflow-y-auto pr-1">
              {bugs.map((bug) => {
                const isSelected = selectedBug?.id === bug.id;
                return (
                  <div
                    key={bug.id}
                    onClick={() => setSelectedBugId(bug.id)}
                    className={`p-3.5 rounded-xl cursor-pointer transition-all border space-y-2 ${
                      isSelected
                        ? 'bg-command-card border-cyber-rose/60 shadow-glow-rose'
                        : 'bg-command-card/40 border-command-border hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold uppercase ${
                        bug.severity === 'CRITICAL' ? 'bg-cyber-rose/10 text-cyber-rose border border-cyber-rose/30' :
                        bug.severity === 'HIGH' ? 'bg-cyber-amber/10 text-cyber-amber border border-cyber-amber/30' :
                        'bg-cyber-blue/10 text-cyber-blue border border-cyber-blue/30'
                      }`}>
                        {bug.severity}
                      </span>
                      <span className="text-[10px] font-mono text-slate-500">
                        {bug.category}
                      </span>
                    </div>

                    <div className="text-xs font-semibold text-white truncate">{bug.title}</div>
                    <div className="text-[11px] text-slate-400 truncate font-mono">
                      {bug.ai_hypotheses.probable_root_cause}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Right: Detailed Split Analysis & Evidence Vault */}
          <div className="lg:col-span-2 space-y-6">
            {selectedBug && (
              <>
                {/* Bug Card Header */}
                <div className="glass-panel p-6 rounded-2xl border-command-border space-y-3">
                  <div className="flex items-center justify-between">
                    <span className={`text-[11px] font-mono px-2.5 py-0.5 rounded font-bold uppercase ${
                      selectedBug.severity === 'CRITICAL' ? 'bg-cyber-rose/20 text-cyber-rose border border-cyber-rose/40' :
                      selectedBug.severity === 'HIGH' ? 'bg-cyber-amber/20 text-cyber-amber border border-cyber-amber/40' :
                      'bg-cyber-blue/20 text-cyber-blue border border-cyber-blue/40'
                    }`}>
                      {selectedBug.severity} SEVERITY
                    </span>
                    <span className="text-xs font-mono text-slate-400">
                      ID: {selectedBug.id.slice(0, 10)}
                    </span>
                  </div>
                  <h3 className="text-base font-bold text-white font-mono">{selectedBug.title}</h3>
                </div>

                {/* THE MANDATORY SPLIT: Verified Evidence vs AI Hypothesis */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Verified Evidence Panel (Deterministic Code Facts) */}
                  <div className="glass-panel p-5 rounded-2xl border-cyber-cyan/30 bg-cyber-cyan/5 space-y-3">
                    <div className="flex items-center space-x-2 border-b border-cyber-cyan/20 pb-2">
                      <ShieldCheck className="w-4 h-4 text-cyber-cyan" />
                      <h4 className="text-xs font-bold font-mono uppercase text-cyber-cyan tracking-wider">
                        Verified Evidence (Deterministic)
                      </h4>
                    </div>
                    <p className="text-[11px] text-slate-300">
                      Factual findings captured directly by Playwright listeners during execution:
                    </p>

                    <div className="space-y-2 font-mono text-xs">
                      {selectedBug.verified_evidence.http_errors?.map((err, idx) => (
                        <div key={idx} className="p-2 rounded bg-slate-900/90 border border-slate-800 text-cyber-rose text-[11px]">
                          <span className="font-bold">HTTP {err.status}:</span> {err.url}
                        </div>
                      ))}

                      {selectedBug.verified_evidence.console_errors?.map((err, idx) => (
                        <div key={idx} className="p-2 rounded bg-slate-900/90 border border-slate-800 text-cyber-amber text-[11px]">
                          <span className="font-bold">[{err.type}]:</span> {err.text}
                        </div>
                      ))}

                      {selectedBug.verified_evidence.failing_selector && (
                        <div className="p-2 rounded bg-slate-900/90 border border-slate-800 text-slate-300 text-[11px]">
                          <span className="text-slate-400">Target Selector:</span>{' '}
                          <code className="text-cyber-cyan">{selectedBug.verified_evidence.failing_selector}</code>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* AI Hypotheses Panel (Gemini Diagnostic Deductions) */}
                  <div className="glass-panel p-5 rounded-2xl border-cyber-violet/30 bg-cyber-violet/5 space-y-3">
                    <div className="flex items-center space-x-2 border-b border-cyber-violet/20 pb-2">
                      <Sparkles className="w-4 h-4 text-cyber-violet" />
                      <h4 className="text-xs font-bold font-mono uppercase text-cyber-violet tracking-wider">
                        AI Hypotheses (Probabilistic)
                      </h4>
                    </div>
                    <p className="text-[11px] text-slate-300">
                      Reasoning generated by Gemini based on diagnostic logs:
                    </p>

                    <div className="space-y-2 text-xs">
                      <div className="p-2.5 rounded bg-slate-900/90 border border-slate-800 space-y-1">
                        <div className="text-[10px] font-mono text-cyber-violet font-semibold uppercase">Probable Root Cause</div>
                        <div className="text-slate-200">{selectedBug.ai_hypotheses.probable_root_cause}</div>
                      </div>

                      <div className="p-2.5 rounded bg-slate-900/90 border border-slate-800 space-y-1">
                        <div className="text-[10px] font-mono text-cyber-violet font-semibold uppercase">Impact Analysis</div>
                        <div className="text-slate-300 text-[11px]">{selectedBug.ai_hypotheses.impact_analysis}</div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Multimodal Diagnostic Evidence Vault Tabs */}
                <div className="glass-panel p-5 rounded-2xl border-command-border space-y-4">
                  <div className="flex items-center justify-between border-b border-command-border/60 pb-3">
                    <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-white">
                      Multimodal Diagnostic Evidence Vault
                    </h4>
                    <div className="flex items-center space-x-1.5 font-mono text-xs">
                      {[
                        { id: 'console', label: 'Console Logs', icon: Terminal },
                        { id: 'network', label: 'Network Requests', icon: Globe },
                        { id: 'screenshot', label: 'Screenshot', icon: Image },
                        { id: 'dom', label: 'DOM State', icon: FileCode },
                      ].map((t) => {
                        const Icon = t.icon;
                        const isActive = evidenceTab === t.id;
                        return (
                          <button
                            key={t.id}
                            onClick={() => setEvidenceTab(t.id as any)}
                            className={`flex items-center space-x-1 px-2.5 py-1 rounded-lg text-[11px] transition-all ${
                              isActive
                                ? 'bg-cyber-cyan/20 text-cyber-cyan border border-cyber-cyan/40'
                                : 'text-slate-400 hover:text-white'
                            }`}
                          >
                            <Icon className="w-3.5 h-3.5" />
                            <span>{t.label}</span>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  {/* Tab Contents */}
                  <div className="font-mono text-xs">
                    {evidenceTab === 'console' && (
                      <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 max-h-48 overflow-y-auto space-y-1.5">
                        {selectedBug.verified_evidence.console_errors?.length === 0 ? (
                          <span className="text-slate-500">No console errors registered.</span>
                        ) : (
                          selectedBug.verified_evidence.console_errors?.map((log, idx) => (
                            <div key={idx} className="text-cyber-amber text-[11px]">
                              <span className="text-slate-500">[{log.type}]</span> {log.text}
                            </div>
                          ))
                        )}
                      </div>
                    )}

                    {evidenceTab === 'network' && (
                      <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 max-h-48 overflow-y-auto space-y-1.5">
                        {selectedBug.verified_evidence.http_errors?.length === 0 ? (
                          <span className="text-slate-500">No network failures registered.</span>
                        ) : (
                          selectedBug.verified_evidence.http_errors?.map((req, idx) => (
                            <div key={idx} className="text-cyber-rose text-[11px] flex justify-between">
                              <span>HTTP {req.status} {req.text}</span>
                              <span className="text-slate-400">{req.url}</span>
                            </div>
                          ))
                        )}
                      </div>
                    )}

                    {evidenceTab === 'screenshot' && (
                      <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-center space-y-2">
                        {selectedBug.screenshot_url ? (
                          <div className="relative group max-w-md mx-auto">
                            <img
                              src={selectedBug.screenshot_url}
                              alt="Failure Screenshot"
                              className="rounded-lg border border-slate-700 max-h-56 mx-auto object-cover cursor-pointer"
                              onClick={() => setScreenshotModalUrl(selectedBug.screenshot_url || null)}
                            />
                            <div className="text-[10px] text-slate-400 mt-1">Click image to expand</div>
                          </div>
                        ) : (
                          <div className="py-8 text-slate-500 text-xs">
                            Failure viewport captured in /artifacts session store.
                          </div>
                        )}
                      </div>
                    )}

                    {evidenceTab === 'dom' && (
                      <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 max-h-48 overflow-y-auto">
                        <pre className="text-[11px] text-slate-300 whitespace-pre-wrap">
                          {selectedBug.verified_evidence.dom_snippet || '&lt;!-- Captured DOM snapshot available in artifacts --&gt;'}
                        </pre>
                      </div>
                    )}
                  </div>
                </div>

                {/* Remediation Advice */}
                <div className="glass-panel p-5 rounded-2xl border-command-border space-y-2">
                  <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-cyber-emerald flex items-center space-x-1.5">
                    <CheckCircle2 className="w-4 h-4" />
                    <span>Recommended Developer Remediation</span>
                  </h4>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    {selectedBug.remediation_advice}
                  </p>
                </div>
              </>
            )}
          </div>
        </div>
      )}

      {/* Screenshot Zoom Modal */}
      {screenshotModalUrl && (
        <div
          className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-6"
          onClick={() => setScreenshotModalUrl(null)}
        >
          <div className="max-w-4xl max-h-[90vh] bg-slate-900 p-2 rounded-2xl border border-slate-700 overflow-hidden">
            <img src={screenshotModalUrl} alt="Zoomed Screenshot" className="max-h-[85vh] object-contain rounded-xl" />
          </div>
        </div>
      )}
    </div>
  );
};
