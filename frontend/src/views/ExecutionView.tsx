import React, { useState } from 'react';
import { 
  Play, 
  CheckCircle2, 
  XCircle, 
  Clock, 
  AlertTriangle, 
  Terminal, 
  Bug, 
  StopCircle,
  ArrowRight,
  ShieldAlert
} from 'lucide-react';
import { TestExecution } from '../types';

interface ExecutionViewProps {
  executions: TestExecution[];
  isExecuting: boolean;
  onExecuteTests: () => void;
  onAbortExecution?: () => void;
  onNavigateToInvestigation: () => void;
}

export const ExecutionView: React.FC<ExecutionViewProps> = ({
  executions,
  isExecuting,
  onExecuteTests,
  onNavigateToInvestigation,
}) => {
  const [selectedExecutionId, setSelectedExecutionId] = useState<string | null>(
    executions.length > 0 ? executions[0].id : null
  );

  const passedCount = executions.filter((e) => e.status === 'PASSED').length;
  const failedCount = executions.filter((e) => e.status === 'FAILED' || e.status === 'TIMED_OUT').length;
  const selectedExecution = executions.find((e) => e.id === selectedExecutionId) || executions[0];

  return (
    <div className="space-y-6">
      {/* Execution Command Bar */}
      <div className="glass-panel p-6 rounded-2xl border-command-border space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-command-border/60 pb-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <Play className="w-5 h-5 text-cyber-cyan" />
              <h2 className="text-sm font-bold font-mono uppercase tracking-wider text-white">
                Deterministic Playwright Execution Sandbox
              </h2>
            </div>
            <p className="text-xs text-slate-400">
              Runs approved scenarios in isolated browser contexts. Gathers step timings, network failures, console logs, and failure screenshots.
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={onExecuteTests}
              disabled={isExecuting}
              className={`px-4 py-2 rounded-xl text-xs font-mono font-semibold tracking-wide transition-all flex items-center space-x-2 ${
                isExecuting
                  ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                  : 'bg-cyber-cyan hover:bg-cyber-cyan/90 text-black shadow-glow-cyan active:scale-95'
              }`}
            >
              <Play className={`w-4 h-4 ${isExecuting ? 'animate-spin' : ''}`} />
              <span>{isExecuting ? 'EXECUTING SCENARIOS...' : 'RUN ALL APPROVED TESTS'}</span>
            </button>

            {failedCount > 0 && (
              <button
                onClick={onNavigateToInvestigation}
                className="px-4 py-2 rounded-xl bg-cyber-rose/20 text-cyber-rose border border-cyber-rose/40 hover:bg-cyber-rose/30 text-xs font-mono font-semibold tracking-wide shadow-glow-rose transition-all flex items-center space-x-2"
              >
                <Bug className="w-4 h-4" />
                <span>Investigate ({failedCount}) Failures</span>
              </button>
            )}
          </div>
        </div>

        {/* Live Counters */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-xs">
          <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <div className="text-[10px] text-slate-400 uppercase">Total Executions</div>
            <div className="text-lg font-bold text-white">{executions.length}</div>
          </div>
          <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <div className="text-[10px] text-slate-400 uppercase">Passed Scenarios</div>
            <div className="text-lg font-bold text-cyber-emerald">{passedCount}</div>
          </div>
          <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <div className="text-[10px] text-slate-400 uppercase">Failed / Timed Out</div>
            <div className="text-lg font-bold text-cyber-rose">{failedCount}</div>
          </div>
          <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <div className="text-[10px] text-slate-400 uppercase">Execution Status</div>
            <div className="text-xs font-semibold text-cyber-cyan flex items-center pt-1">
              <span className={`w-2 h-2 rounded-full mr-1.5 ${isExecuting ? 'bg-cyber-cyan animate-ping' : 'bg-cyber-emerald'}`}></span>
              {isExecuting ? 'ACTIVE' : 'IDLE'}
            </div>
          </div>
        </div>
      </div>

      {/* Main Execution Split Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Execution Scenarios List */}
        <div className="glass-panel p-5 rounded-2xl border-command-border space-y-4">
          <div className="flex items-center justify-between border-b border-command-border/60 pb-3">
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-white">
              Executed Scenarios
            </h3>
            <span className="text-[10px] font-mono text-slate-400">PLAYWRIGHT RUNNER</span>
          </div>

          <div className="space-y-2 max-h-[550px] overflow-y-auto pr-1">
            {executions.length === 0 ? (
              <div className="py-12 text-center text-slate-500 font-mono text-xs">
                No tests executed yet. Click "Run All Approved Tests" above.
              </div>
            ) : (
              executions.map((exec) => {
                const isSelected = selectedExecution?.id === exec.id;
                return (
                  <div
                    key={exec.id}
                    onClick={() => setSelectedExecutionId(exec.id)}
                    className={`p-3.5 rounded-xl cursor-pointer transition-all border space-y-2 ${
                      isSelected
                        ? 'bg-command-card border-cyber-cyan/50 shadow-glow-cyan'
                        : 'bg-command-card/40 border-command-border hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold uppercase ${
                        exec.status === 'PASSED' ? 'bg-cyber-emerald/10 text-cyber-emerald border border-cyber-emerald/30' :
                        exec.status === 'FAILED' ? 'bg-cyber-rose/10 text-cyber-rose border border-cyber-rose/30' :
                        'bg-cyber-amber/10 text-cyber-amber border border-cyber-amber/30'
                      }`}>
                        {exec.status}
                      </span>
                      <span className="text-[10px] font-mono text-slate-500 flex items-center">
                        <Clock className="w-3 h-3 mr-1" />
                        {exec.duration_ms}ms
                      </span>
                    </div>

                    <div className="text-xs font-semibold text-white truncate">
                      {exec.scenario_title}
                    </div>

                    {exec.error_message && (
                      <div className="text-[11px] font-mono text-cyber-rose bg-cyber-rose/5 p-1.5 rounded border border-cyber-rose/20 truncate">
                        {exec.error_message}
                      </div>
                    )}
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right: Step Timeline & Live Telemetry Inspector */}
        <div className="lg:col-span-2 glass-panel p-5 rounded-2xl border-command-border space-y-4">
          <div className="flex items-center justify-between border-b border-command-border/60 pb-3">
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-white">
              Step Execution Timeline & Diagnostics
            </h3>
            {selectedExecution && (
              <span className="text-[10px] font-mono text-slate-400">
                {selectedExecution.steps?.length || 0} Steps Recorded
              </span>
            )}
          </div>

          {!selectedExecution ? (
            <div className="py-20 text-center text-slate-500 font-mono text-xs">
              Select an executed scenario on the left to inspect step-by-step traces.
            </div>
          ) : (
            <div className="space-y-4">
              {/* Scenario Summary */}
              <div className="p-3.5 rounded-xl bg-command-card/60 border border-command-border space-y-2">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-bold text-white font-mono">{selectedExecution.scenario_title}</h4>
                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold ${
                    selectedExecution.status === 'PASSED' ? 'text-cyber-emerald' : 'text-cyber-rose'
                  }`}>
                    {selectedExecution.status} ({selectedExecution.duration_ms}ms)
                  </span>
                </div>
                {selectedExecution.error_message && (
                  <div className="text-xs font-mono text-cyber-rose bg-cyber-rose/10 p-2.5 rounded-lg border border-cyber-rose/30 space-y-1">
                    <div className="font-bold flex items-center space-x-1">
                      <ShieldAlert className="w-3.5 h-3.5" />
                      <span>FAILURE ENCOUNTERED AT STEP {selectedExecution.error_step_index || 1}:</span>
                    </div>
                    <div className="text-[11px] text-slate-300 break-all">{selectedExecution.error_message}</div>
                  </div>
                )}
              </div>

              {/* Step Sequence */}
              <div className="space-y-2 max-h-[400px] overflow-y-auto pr-1">
                {selectedExecution.steps?.map((step, idx) => (
                  <div
                    key={idx}
                    className={`p-3 rounded-xl border font-mono text-xs transition-all ${
                      step.status === 'PASSED'
                        ? 'bg-slate-900/50 border-slate-800'
                        : 'bg-cyber-rose/10 border-cyber-rose/40'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        {step.status === 'PASSED' ? (
                          <CheckCircle2 className="w-4 h-4 text-cyber-emerald" />
                        ) : (
                          <XCircle className="w-4 h-4 text-cyber-rose" />
                        )}
                        <span className="text-slate-400 font-bold">Step {step.step_index}:</span>
                        <span className="px-1.5 py-0.5 rounded bg-cyber-cyan/10 text-cyber-cyan uppercase font-bold text-[10px]">
                          {step.action}
                        </span>
                        <span className="text-slate-300">{step.selector || ''}</span>
                        {step.value && <span className="text-cyber-amber">("{step.value}")</span>}
                      </div>

                      <span className="text-[10px] text-slate-500">{step.duration_ms}ms</span>
                    </div>

                    {step.error_log && (
                      <div className="mt-2 text-[11px] font-mono text-cyber-rose bg-black/40 p-2 rounded border border-cyber-rose/20 whitespace-pre-wrap">
                        {step.error_log}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
