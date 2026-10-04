import { 
  Activity, 
  Compass, 
  Terminal, 
  Play, 
  Bug, 
  FileText, 
  Cpu, 
  ShieldCheck
} from 'lucide-react';

export type NavTab = 'dashboard' | 'scanner' | 'planning' | 'execution' | 'investigation' | 'reports';

interface SidebarProps {
  activeTab: NavTab;
  setActiveTab: (tab: NavTab) => void;
  systemStatus: { status: string; environment: string; gemini_configured: boolean } | null;
}

export const Sidebar = ({ activeTab, setActiveTab, systemStatus }: SidebarProps) => {
  const navItems: { id: NavTab; label: string; icon: any; desc: string }[] = [
    { id: 'dashboard', label: 'Executive Metrics', icon: Activity, desc: 'KPIs & Telemetry' },
    { id: 'scanner', label: 'Website Scanner', icon: Compass, desc: 'Topology & Elements' },
    { id: 'planning', label: 'AI Test Planning', icon: Terminal, desc: 'Scenario Generator' },
    { id: 'execution', label: 'Test Execution', icon: Play, desc: 'Deterministic Runner' },
    { id: 'investigation', label: 'Bug Investigation', icon: Bug, desc: 'Root Cause & Evidence' },
    { id: 'reports', label: 'Historical Reports', icon: FileText, desc: 'Trends & Export' },
  ];

  return (
    <aside className="w-64 border-r border-command-border bg-command-surface/60 backdrop-blur-md flex flex-col justify-between p-4 select-none">
      <div>
        {/* Brand Header */}
        <div className="flex items-center space-x-3 px-2 py-4 border-b border-command-border mb-6">
          <div className="p-2.5 rounded-xl bg-cyber-cyan/10 border border-cyber-cyan/30 text-cyber-cyan shadow-glow-cyan">
            <Cpu className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <h1 className="text-xs font-bold tracking-wider uppercase text-white font-mono flex items-center space-x-1.5">
              <span>ANTIGRAVITY</span>
              <span className="text-[10px] px-1.5 py-0.5 rounded bg-cyber-cyan/20 text-cyber-cyan font-mono">AI</span>
            </h1>
            <p className="text-[10px] text-slate-400 font-mono tracking-tight">AUTONOMOUS QA AGENT</p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-medium transition-all group ${
                  isActive
                    ? 'bg-cyber-cyan/10 text-cyber-cyan border border-cyber-cyan/40 shadow-glow-cyan'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-command-hover/40 border border-transparent'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <Icon className={`w-4 h-4 transition-transform group-hover:scale-110 ${isActive ? 'text-cyber-cyan' : 'text-slate-400'}`} />
                  <div className="text-left">
                    <div className="leading-tight">{item.label}</div>
                    <div className="text-[10px] text-slate-500 font-mono">{item.desc}</div>
                  </div>
                </div>
                {isActive && (
                  <div className="w-1.5 h-1.5 rounded-full bg-cyber-cyan animate-pulse"></div>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* System Status Readout */}
      <div className="glass-panel p-3.5 rounded-xl text-xs font-mono space-y-2.5">
        <div className="text-[10px] text-slate-400 uppercase tracking-widest font-semibold border-b border-command-border/60 pb-1 flex items-center justify-between">
          <span>Engine Telemetry</span>
          <span className="text-cyber-cyan text-[9px]">v0.1.0</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-slate-400">STATUS</span>
          <span className="flex items-center text-cyber-emerald text-[11px]">
            <span className="w-1.5 h-1.5 rounded-full bg-cyber-emerald mr-1.5 animate-ping"></span>
            ACTIVE
          </span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-slate-400">SSRF GUARD</span>
          <span className="text-cyber-cyan flex items-center text-[11px]">
            <ShieldCheck className="w-3.5 h-3.5 mr-1" /> ENFORCED
          </span>
        </div>
        <div className="flex items-center justify-between text-[11px]">
          <span className="text-slate-400">GEMINI LLM</span>
          <span className={systemStatus?.gemini_configured ? 'text-cyber-emerald' : 'text-cyber-amber'}>
            {systemStatus?.gemini_configured ? 'CONNECTED' : 'STANDBY'}
          </span>
        </div>
      </div>
    </aside>
  );
};
