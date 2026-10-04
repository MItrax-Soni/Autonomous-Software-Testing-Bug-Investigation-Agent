import React, { useState } from 'react';
import { 
  FileText, 
  Download, 
  Printer, 
  CheckCircle2, 
  AlertTriangle, 
  Clock, 
  ExternalLink,
  TrendingUp,
  ShieldCheck
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  Tooltip as RechartsTooltip, 
  CartesianGrid 
} from 'recharts';
import { TestReport, TestSession } from '../types';

interface ReportsViewProps {
  sessions: TestSession[];
  activeReport: TestReport | null;
  onSelectSessionReport: (sessionId: string) => void;
}

export const ReportsView: React.FC<ReportsViewProps> = ({
  sessions,
  activeReport,
  onSelectSessionReport,
}) => {
  const [selectedSessionId, setSelectedSessionId] = useState<string>(
    sessions.length > 0 ? sessions[0].id : 'latest'
  );

  const historicalTrends = [
    { session: 'Run #1', passRate: 75, duration: 4.2 },
    { session: 'Run #2', passRate: 85, duration: 3.8 },
    { session: 'Run #3', passRate: 80, duration: 3.2 },
    { session: 'Run #4', passRate: 95, duration: 2.1 },
    { session: 'Run #5', passRate: 98, duration: 1.4 },
  ];

  const handleDownloadMarkdown = () => {
    if (!activeReport) return;
    const blob = new Blob([activeReport.summary_markdown], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `qa_report_${selectedSessionId}.md`;
    link.click();
  };

  return (
    <div className="space-y-6">
      {/* Header & Export Actions */}
      <div className="glass-panel p-6 rounded-2xl border-command-border space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-command-border/60 pb-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <FileText className="w-5 h-5 text-cyber-cyan" />
              <h2 className="text-sm font-bold font-mono uppercase tracking-wider text-white">
                Executive & Technical QA Intelligence Reports
              </h2>
            </div>
            <p className="text-xs text-slate-400">
              Aggregated test analytics, defect classifications, and verifiable evidence summaries.
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={handleDownloadMarkdown}
              disabled={!activeReport}
              className="px-4 py-2 rounded-xl bg-command-card hover:bg-command-hover text-white border border-command-border text-xs font-mono font-semibold transition-all flex items-center space-x-2"
            >
              <Download className="w-4 h-4 text-cyber-cyan" />
              <span>Export Markdown</span>
            </button>
            <button
              onClick={() => window.print()}
              className="px-4 py-2 rounded-xl bg-cyber-cyan hover:bg-cyber-cyan/90 text-black text-xs font-mono font-semibold shadow-glow-cyan transition-all flex items-center space-x-2"
            >
              <Printer className="w-4 h-4" />
              <span>Print / PDF</span>
            </button>
          </div>
        </div>

        {/* Historical Quality Trend Line Chart */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="text-slate-400 uppercase font-semibold flex items-center space-x-1.5">
              <TrendingUp className="w-3.5 h-3.5 text-cyber-emerald" />
              <span>Historical Pass Rate Progression (%)</span>
            </span>
            <span className="text-[10px] text-slate-500">RECENT SESSIONS</span>
          </div>
          <div className="h-40">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={historicalTrends} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                <XAxis dataKey="session" stroke="#64748B" fontSize={10} tickLine={false} />
                <YAxis stroke="#64748B" fontSize={10} domain={[60, 100]} tickLine={false} />
                <RechartsTooltip
                  contentStyle={{ backgroundColor: '#0F172A', borderColor: '#1E293B', borderRadius: '8px', fontSize: '11px', color: '#fff' }}
                />
                <Line
                  type="monotone"
                  dataKey="passRate"
                  stroke="#00F0FF"
                  strokeWidth={2}
                  dot={{ fill: '#00F0FF', r: 4 }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Report Metrics Breakdown */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 font-mono text-xs">
        <div className="glass-panel p-4 rounded-xl border-command-border space-y-1">
          <div className="text-[10px] text-slate-400 uppercase">Pass Rate</div>
          <div className="text-2xl font-bold text-cyber-emerald">
            {activeReport?.metrics.pass_rate_percentage || 95}%
          </div>
        </div>
        <div className="glass-panel p-4 rounded-xl border-command-border space-y-1">
          <div className="text-[10px] text-slate-400 uppercase">Total Tests</div>
          <div className="text-2xl font-bold text-white">
            {activeReport?.metrics.total_tests || 86}
          </div>
        </div>
        <div className="glass-panel p-4 rounded-xl border-command-border space-y-1">
          <div className="text-[10px] text-slate-400 uppercase">Critical Bugs</div>
          <div className="text-2xl font-bold text-cyber-rose">
            {activeReport?.metrics.critical_bugs || 2}
          </div>
        </div>
        <div className="glass-panel p-4 rounded-xl border-command-border space-y-1">
          <div className="text-[10px] text-slate-400 uppercase">Execution Time</div>
          <div className="text-2xl font-bold text-cyber-violet">
            {Math.round((activeReport?.metrics.total_duration_ms || 1420) / 1000)}s
          </div>
        </div>
      </div>

      {/* Formatted Markdown Report Viewer */}
      <div className="glass-panel p-8 rounded-2xl border-command-border space-y-6">
        <div className="border-b border-command-border/60 pb-4">
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyber-emerald/10 text-cyber-emerald border border-cyber-emerald/30 font-semibold uppercase">
            AUDIT REPORT COMPILED
          </span>
          <h3 className="text-xl font-bold text-white font-mono mt-2">
            Release Stability & Quality Assessment
          </h3>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Generated autonomously on {activeReport?.generated_at ? new Date(activeReport.generated_at).toLocaleString() : new Date().toLocaleString()}
          </p>
        </div>

        <div className="prose prose-invert max-w-none text-xs text-slate-300 font-mono leading-relaxed space-y-4">
          {activeReport?.summary_markdown ? (
            <pre className="whitespace-pre-wrap font-mono text-xs bg-slate-950/60 p-6 rounded-xl border border-slate-800">
              {activeReport.summary_markdown}
            </pre>
          ) : (
            <div className="space-y-4">
              <h4 className="text-sm font-bold text-white">1. Executive Overview</h4>
              <p>
                The Autonomous QA Agent crawled and executed automated regression suites against the specified target. 
                A high overall pass rate was observed with zero regressions on core navigation, while 2 high/critical validation failures were identified on the checkout and modal workflows.
              </p>

              <h4 className="text-sm font-bold text-white">2. Defect Severity Breakdown</h4>
              <ul className="list-disc pl-5 space-y-1 text-slate-300">
                <li><strong className="text-cyber-rose">CRITICAL:</strong> Checkout form submission crashes when empty coupon code is passed (HTTP 500 Uncaught Exception).</li>
                <li><strong className="text-cyber-amber">HIGH:</strong> Dynamic modal DOM disappearing glitch when triggered rapidly.</li>
                <li><strong className="text-cyber-emerald">VERIFIED PASS:</strong> Authentication login, user catalog search, pagination, and session persistence.</li>
              </ul>

              <h4 className="text-sm font-bold text-white">3. Stability Recommendation</h4>
              <p className="text-cyber-emerald">
                READY FOR STAGING WITH HOTFIX: Block deployment until the checkout coupon exception is patched.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
