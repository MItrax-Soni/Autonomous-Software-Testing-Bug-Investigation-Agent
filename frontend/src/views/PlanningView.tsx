import React, { useState } from 'react';
import { 
  Terminal, 
  Sparkles, 
  CheckCircle2, 
  XCircle, 
  Play, 
  ArrowRight, 
  ShieldCheck, 
  Layers, 
  Clock, 
  Filter,
  CheckSquare,
  Square
} from 'lucide-react';
import { TestScenario } from '../types';

interface PlanningViewProps {
  scenarios: TestScenario[];
  isGenerating: boolean;
  onGenerateScenarios: () => void;
  onToggleApproval: (scenarioId: string, isApproved: boolean) => void;
  onProceedToExecution: () => void;
}

export const PlanningView: React.FC<PlanningViewProps> = ({
  scenarios,
  isGenerating,
  onGenerateScenarios,
  onToggleApproval,
  onProceedToExecution,
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [expandedScenarioId, setExpandedScenarioId] = useState<string | null>(null);

  const filteredScenarios = scenarios.filter((s) => {
    if (selectedCategory === 'ALL') return true;
    return s.category === selectedCategory;
  });

  const approvedCount = scenarios.filter((s) => s.is_approved).length;

  return (
    <div className="space-y-6">
      {/* AI Scenario Formulation Header */}
      <div className="glass-panel p-6 rounded-2xl border-command-border space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-command-border/60 pb-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <Sparkles className="w-5 h-5 text-cyber-violet animate-pulse" />
              <h2 className="text-sm font-bold font-mono uppercase tracking-wider text-white">
                Gemini Generative QA Scenario Planner
              </h2>
            </div>
            <p className="text-xs text-slate-400">
              Formulates structured positive, negative, and edge-case journeys validated against strict deterministic DSL schemas.
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={onGenerateScenarios}
              disabled={isGenerating}
              className={`px-4 py-2 rounded-xl text-xs font-mono font-semibold tracking-wide transition-all flex items-center space-x-2 ${
                isGenerating
                  ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                  : 'bg-cyber-violet hover:bg-cyber-violet/90 text-white shadow-glow-violet active:scale-95'
              }`}
            >
              <Sparkles className={`w-4 h-4 ${isGenerating ? 'animate-spin' : ''}`} />
              <span>{isGenerating ? 'GEMINI REASONING...' : 'GENERATE WITH GEMINI'}</span>
            </button>

            {approvedCount > 0 && (
              <button
                onClick={onProceedToExecution}
                className="px-4 py-2 rounded-xl bg-cyber-cyan hover:bg-cyber-cyan/90 text-black text-xs font-mono font-semibold tracking-wide shadow-glow-cyan transition-all flex items-center space-x-2 active:scale-95"
              >
                <Play className="w-4 h-4" />
                <span>Execute ({approvedCount}) Approved</span>
              </button>
            )}
          </div>
        </div>

        {/* Filter bar & Approved tally */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 font-mono text-xs">
          <div className="flex items-center space-x-2">
            <span className="text-slate-400 text-[11px] uppercase">Categories:</span>
            {['ALL', 'POSITIVE', 'NEGATIVE', 'BOUNDARY', 'RESPONSIVENESS'].map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-2.5 py-1 rounded-lg text-[10px] font-semibold transition-all ${
                  selectedCategory === cat
                    ? 'bg-cyber-cyan/20 text-cyber-cyan border border-cyber-cyan/40'
                    : 'text-slate-400 hover:text-white bg-command-card border border-command-border'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          <div className="text-[11px] text-slate-400">
            Approved for Execution:{' '}
            <span className="text-cyber-emerald font-bold">{approvedCount}</span> /{' '}
            <span className="text-white">{scenarios.length}</span>
          </div>
        </div>
      </div>

      {/* Scenarios List */}
      <div className="space-y-4">
        {filteredScenarios.length === 0 ? (
          <div className="glass-panel p-12 rounded-2xl border-command-border text-center space-y-3">
            <div className="w-12 h-12 rounded-full bg-cyber-violet/10 border border-cyber-violet/30 text-cyber-violet flex items-center justify-center mx-auto">
              <Terminal className="w-6 h-6" />
            </div>
            <h3 className="text-sm font-semibold text-white">No Test Scenarios Planned</h3>
            <p className="text-xs text-slate-400 max-w-md mx-auto">
              Click "Generate with Gemini" above to formulate structured test journeys based on discovered interactive DOM elements.
            </p>
          </div>
        ) : (
          filteredScenarios.map((scenario) => {
            const isExpanded = expandedScenarioId === scenario.id;
            return (
              <div
                key={scenario.id}
                className={`glass-panel rounded-2xl border transition-all overflow-hidden ${
                  scenario.is_approved
                    ? 'border-command-border hover:border-cyber-cyan/40'
                    : 'border-slate-800 opacity-60'
                }`}
              >
                {/* Header */}
                <div className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-command-card/40">
                  <div className="flex items-start space-x-3">
                    <button
                      onClick={() => onToggleApproval(scenario.id, !scenario.is_approved)}
                      className="mt-0.5 text-cyber-cyan hover:text-white transition-colors"
                      title={scenario.is_approved ? 'Unapprove Scenario' : 'Approve Scenario'}
                    >
                      {scenario.is_approved ? (
                        <CheckSquare className="w-5 h-5 text-cyber-emerald" />
                      ) : (
                        <Square className="w-5 h-5 text-slate-500" />
                      )}
                    </button>

                    <div className="space-y-1">
                      <div className="flex items-center space-x-2">
                        <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-semibold uppercase ${
                          scenario.category === 'POSITIVE' ? 'bg-cyber-emerald/10 text-cyber-emerald border border-cyber-emerald/30' :
                          scenario.category === 'NEGATIVE' ? 'bg-cyber-amber/10 text-cyber-amber border border-cyber-amber/30' :
                          'bg-cyber-violet/10 text-cyber-violet border border-cyber-violet/30'
                        }`}>
                          {scenario.category}
                        </span>
                        <h3 className="text-xs font-bold text-white font-mono">{scenario.title}</h3>
                      </div>
                      <p className="text-[11px] text-slate-400">{scenario.description}</p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-3 font-mono text-xs">
                    <span className="text-[11px] text-slate-400">
                      {scenario.steps?.length || 0} DSL Steps
                    </span>
                    <button
                      onClick={() => setExpandedScenarioId(isExpanded ? null : scenario.id)}
                      className="px-2.5 py-1 rounded bg-command-hover text-[11px] text-cyber-cyan border border-command-border hover:border-cyber-cyan/30 transition-all"
                    >
                      {isExpanded ? 'Hide Steps' : 'Inspect Steps'}
                    </button>
                  </div>
                </div>

                {/* Expanded Steps View */}
                {isExpanded && (
                  <div className="p-4 border-t border-command-border/60 bg-slate-950/40 space-y-3 font-mono text-xs">
                    <div className="text-[11px] text-slate-400 uppercase font-semibold">
                      Deterministic Execution Trace:
                    </div>

                    <div className="space-y-2">
                      {scenario.steps?.map((step, idx) => (
                        <div
                          key={idx}
                          className="flex items-center justify-between p-2 rounded-lg bg-slate-900/80 border border-slate-800 text-[11px]"
                        >
                          <div className="flex items-center space-x-2">
                            <span className="text-slate-500 w-4 text-right">{idx + 1}.</span>
                            <span className="px-1.5 py-0.5 rounded bg-cyber-cyan/10 text-cyber-cyan font-bold uppercase text-[10px]">
                              {step.action}
                            </span>
                            <span className="text-slate-300">{step.selector || step.expected || ''}</span>
                            {step.value && (
                              <span className="text-cyber-amber">("{step.value}")</span>
                            )}
                          </div>
                          <span className="text-[10px] text-slate-500">
                            {step.timeout_ms || 5000}ms
                          </span>
                        </div>
                      ))}
                    </div>

                    <div className="p-2.5 rounded-lg bg-cyber-emerald/5 border border-cyber-emerald/20 text-[11px] text-slate-300">
                      <span className="text-cyber-emerald font-semibold uppercase mr-1">Expected Outcome:</span>
                      {scenario.expected_result}
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
