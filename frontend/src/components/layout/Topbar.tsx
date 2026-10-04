import { Globe, Compass, ExternalLink } from 'lucide-react';

interface TopbarProps {
  targetUrl: string;
  setTargetUrl: (url: string) => void;
  onLaunchScan: () => void;
  environment?: string;
  isScanning?: boolean;
}

export const Topbar = ({
  targetUrl,
  setTargetUrl,
  onLaunchScan,
  environment = 'development',
  isScanning = false,
}: TopbarProps) => {
  return (
    <header className="h-16 border-b border-command-border bg-command-surface/40 backdrop-blur-md px-6 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <span className="text-[11px] font-mono px-2.5 py-1 rounded-md bg-slate-800 text-slate-300 border border-slate-700">
          NODE: {environment.toUpperCase()}
        </span>
        <span className="text-[11px] font-mono text-slate-400">
          SANDBOX: CHROMIUM_HEADLESS
        </span>
      </div>

      <div className="flex items-center space-x-3">
        {/* Controlled Target Quick Button */}
        <button
          onClick={() => setTargetUrl('http://localhost:8088')}
          className="hidden md:flex items-center space-x-1.5 px-2.5 py-1.5 rounded-lg bg-command-hover text-[11px] font-mono text-slate-300 border border-command-border hover:text-cyber-cyan hover:border-cyber-cyan/30 transition-all"
          title="Quickly fill the controlled defective test app address"
        >
          <ExternalLink className="w-3.5 h-3.5" />
          <span>Local Target (:8088)</span>
        </button>

        {/* Target URL Input */}
        <div className="flex items-center space-x-2 bg-command-card border border-command-border focus-within:border-cyber-cyan/50 focus-within:shadow-glow-cyan rounded-lg px-3 py-1.5 transition-all">
          <Globe className="w-4 h-4 text-cyber-cyan" />
          <input
            type="url"
            value={targetUrl}
            onChange={(e) => setTargetUrl(e.target.value)}
            placeholder="http://localhost:8088"
            className="bg-transparent text-xs text-white placeholder-slate-500 focus:outline-none w-72 font-mono"
          />
        </div>

        {/* Launch Action */}
        <button
          onClick={onLaunchScan}
          disabled={isScanning || !targetUrl}
          className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold font-mono tracking-wide transition-all ${
            isScanning
              ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
              : 'bg-cyber-cyan hover:bg-cyber-cyan/90 text-black shadow-glow-cyan active:scale-95'
          }`}
        >
          <Compass className={`w-3.5 h-3.5 ${isScanning ? 'animate-spin' : ''}`} />
          <span>{isScanning ? 'SCANNING...' : 'SCAN TARGET'}</span>
        </button>
      </div>
    </header>
  );
};
