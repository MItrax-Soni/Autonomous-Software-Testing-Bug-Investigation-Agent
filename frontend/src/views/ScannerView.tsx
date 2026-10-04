import React, { useState } from 'react';
import { 
  Compass, 
  Globe, 
  Layers, 
  ShieldCheck, 
  Search, 
  ArrowRight, 
  CheckCircle2, 
  FileCode, 
  Sliders,
  ExternalLink,
  Tag
} from 'lucide-react';
import { DiscoveredPage, DiscoveredElement } from '../types';

interface ScannerViewProps {
  targetUrl: string;
  setTargetUrl: (url: string) => void;
  isScanning: boolean;
  pages: DiscoveredPage[];
  elements: DiscoveredElement[];
  onStartScan: () => void;
  onProceedToPlanning: () => void;
}

export const ScannerView: React.FC<ScannerViewProps> = ({
  targetUrl,
  setTargetUrl,
  isScanning,
  pages,
  elements,
  onStartScan,
  onProceedToPlanning,
}) => {
  const [maxDepth, setMaxDepth] = useState(2);
  const [maxPages, setMaxPages] = useState(10);
  const [filterQuery, setFilterQuery] = useState('');
  const [selectedTag, setSelectedTag] = useState('ALL');

  const filteredElements = elements.filter((el) => {
    const matchesSearch =
      el.selector.toLowerCase().includes(filterQuery.toLowerCase()) ||
      (el.semantic_label && el.semantic_label.toLowerCase().includes(filterQuery.toLowerCase())) ||
      el.tag_name.toLowerCase().includes(filterQuery.toLowerCase());
    const matchesTag = selectedTag === 'ALL' || el.element_type?.toUpperCase() === selectedTag;
    return matchesSearch && matchesTag;
  });

  return (
    <div className="space-y-6">
      {/* Scanner Control Panel */}
      <div className="glass-panel p-6 rounded-2xl border-command-border space-y-4">
        <div className="flex items-center justify-between border-b border-command-border/60 pb-3">
          <div className="flex items-center space-x-2">
            <Compass className="w-5 h-5 text-cyber-cyan" />
            <h2 className="text-sm font-bold font-mono uppercase tracking-wider text-white">
              Autonomous Crawler & Surface Discovery Engine
            </h2>
          </div>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyber-cyan/10 text-cyber-cyan border border-cyber-cyan/30">
            CHROMIUM ENGINE ACTIVE
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
          {/* Target URL */}
          <div className="md:col-span-2 space-y-1.5">
            <label className="text-[11px] font-mono text-slate-400 uppercase">Target Web Application URL</label>
            <div className="flex items-center space-x-2 bg-command-card border border-command-border rounded-xl px-3 py-2 focus-within:border-cyber-cyan/50 focus-within:shadow-glow-cyan transition-all">
              <Globe className="w-4 h-4 text-cyber-cyan flex-shrink-0" />
              <input
                type="url"
                value={targetUrl}
                onChange={(e) => setTargetUrl(e.target.value)}
                placeholder="http://localhost:8088"
                className="bg-transparent text-xs text-white focus:outline-none w-full font-mono"
              />
            </div>
          </div>

          {/* Depth Limit */}
          <div className="space-y-1.5">
            <label className="text-[11px] font-mono text-slate-400 uppercase">Crawl Depth Limit</label>
            <select
              value={maxDepth}
              onChange={(e) => setMaxDepth(Number(e.target.value))}
              className="w-full bg-command-card border border-command-border rounded-xl px-3 py-2 text-xs font-mono text-white focus:outline-none focus:border-cyber-cyan/50"
            >
              <option value={1}>Depth 1 (Single Page)</option>
              <option value={2}>Depth 2 (Immediate Links)</option>
              <option value={3}>Depth 3 (Deep Discovery)</option>
            </select>
          </div>

          {/* Max Pages */}
          <div className="space-y-1.5">
            <label className="text-[11px] font-mono text-slate-400 uppercase">Max Page Count</label>
            <select
              value={maxPages}
              onChange={(e) => setMaxPages(Number(e.target.value))}
              className="w-full bg-command-card border border-command-border rounded-xl px-3 py-2 text-xs font-mono text-white focus:outline-none focus:border-cyber-cyan/50"
            >
              <option value={5}>5 Pages</option>
              <option value={10}>10 Pages</option>
              <option value={15}>15 Pages</option>
              <option value={25}>25 Pages</option>
            </select>
          </div>
        </div>

        {/* Scan Actions and Security Indicator */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2">
          <div className="flex items-center space-x-2 text-[11px] font-mono text-cyber-cyan">
            <ShieldCheck className="w-4 h-4 text-cyber-emerald" />
            <span>Pre-flight SSRF Validation & DNS Pinning Active</span>
          </div>

          <div className="flex items-center space-x-3 w-full sm:w-auto">
            <button
              onClick={() => setTargetUrl('http://localhost:8088')}
              className="px-3 py-2 rounded-xl bg-command-hover text-xs font-mono text-slate-300 border border-command-border hover:border-slate-600 transition-all"
            >
              Set Local Test Target (:8088)
            </button>
            <button
              onClick={onStartScan}
              disabled={isScanning || !targetUrl}
              className={`flex-1 sm:flex-initial px-5 py-2 rounded-xl text-xs font-mono font-semibold tracking-wide transition-all flex items-center justify-center space-x-2 ${
                isScanning
                  ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                  : 'bg-cyber-cyan hover:bg-cyber-cyan/90 text-black shadow-glow-cyan active:scale-95'
              }`}
            >
              <Compass className={`w-4 h-4 ${isScanning ? 'animate-spin' : ''}`} />
              <span>{isScanning ? 'CRAWLING APPLICATION...' : 'START TOPOLOGY CRAWL'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Progress Banner while scanning */}
      {isScanning && (
        <div className="glass-panel p-4 rounded-xl border-cyber-cyan/40 bg-cyber-cyan/5 flex items-center space-x-4 animate-pulse">
          <div className="p-2 rounded-lg bg-cyber-cyan/20 text-cyber-cyan">
            <Compass className="w-5 h-5 animate-spin" />
          </div>
          <div className="space-y-0.5">
            <div className="text-xs font-bold font-mono text-white">Chromium Headless Crawler Running</div>
            <div className="text-[11px] text-slate-400 font-mono">
              Extracting DOM nodes, semantic ARIA roles, internal routes, and interactive input forms...
            </div>
          </div>
        </div>
      )}

      {/* Discovered Topology & Interactive Elements Columns */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Discovered Pages */}
        <div className="glass-panel p-5 rounded-2xl border-command-border space-y-4">
          <div className="flex items-center justify-between border-b border-command-border/60 pb-3">
            <div className="flex items-center space-x-2">
              <Layers className="w-4 h-4 text-cyber-cyan" />
              <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-white">
                Discovered Pages ({pages.length})
              </h3>
            </div>
          </div>

          <div className="space-y-2 max-h-[500px] overflow-y-auto pr-1">
            {pages.length === 0 ? (
              <div className="py-12 text-center text-slate-500 font-mono text-xs">
                No pages scanned yet. Click "Start Topology Crawl" to begin mapping the application.
              </div>
            ) : (
              pages.map((p) => (
                <div
                  key={p.id}
                  className="p-3 rounded-xl bg-command-card/70 border border-command-border hover:border-cyber-cyan/30 transition-all space-y-1.5"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyber-emerald/10 text-cyber-emerald border border-cyber-emerald/30 font-semibold">
                      HTTP {p.http_status}
                    </span>
                    <span className="text-[10px] font-mono text-slate-500">Depth {p.depth}</span>
                  </div>
                  <div className="text-xs font-semibold text-white truncate">{p.title || 'Untitled Route'}</div>
                  <div className="text-[11px] font-mono text-slate-400 truncate flex items-center space-x-1">
                    <ExternalLink className="w-3 h-3 text-slate-500 flex-shrink-0" />
                    <span>{p.url}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right: Discovered Interactive Elements */}
        <div className="lg:col-span-2 glass-panel p-5 rounded-2xl border-command-border space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-command-border/60 pb-3">
            <div className="flex items-center space-x-2">
              <FileCode className="w-4 h-4 text-cyber-cyan" />
              <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-white">
                Interactive Elements ({elements.length})
              </h3>
            </div>

            {/* Filter Controls */}
            <div className="flex items-center space-x-2">
              <div className="flex items-center space-x-1.5 bg-command-card border border-command-border rounded-lg px-2.5 py-1 text-xs">
                <Search className="w-3.5 h-3.5 text-slate-500" />
                <input
                  type="text"
                  value={filterQuery}
                  onChange={(e) => setFilterQuery(e.target.value)}
                  placeholder="Filter selectors..."
                  className="bg-transparent text-white focus:outline-none text-[11px] font-mono w-32"
                />
              </div>

              {/* Tag type filter */}
              <select
                value={selectedTag}
                onChange={(e) => setSelectedTag(e.target.value)}
                className="bg-command-card border border-command-border rounded-lg px-2 py-1 text-[11px] font-mono text-white focus:outline-none"
              >
                <option value="ALL">All Elements</option>
                <option value="BUTTON">Buttons</option>
                <option value="INPUT">Inputs</option>
                <option value="SELECT">Selects</option>
                <option value="LINK">Links</option>
              </select>
            </div>
          </div>

          <div className="space-y-2 max-h-[500px] overflow-y-auto pr-1">
            {filteredElements.length === 0 ? (
              <div className="py-12 text-center text-slate-500 font-mono text-xs">
                No interactive elements extracted yet.
              </div>
            ) : (
              filteredElements.map((el) => (
                <div
                  key={el.id}
                  className="p-3 rounded-xl bg-command-card/50 border border-command-border hover:border-slate-600 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-2"
                >
                  <div className="space-y-1">
                    <div className="flex items-center space-x-2">
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyber-cyan/10 text-cyber-cyan border border-cyber-cyan/30 uppercase font-semibold">
                        {el.element_type || el.tag_name}
                      </span>
                      {el.semantic_label && (
                        <span className="text-xs font-semibold text-white">{el.semantic_label}</span>
                      )}
                    </div>
                    <div className="text-[11px] font-mono text-slate-400 bg-slate-900/60 px-2 py-1 rounded border border-slate-800 break-all">
                      {el.selector}
                    </div>
                  </div>

                  <div className="flex-shrink-0 text-right">
                    <span className="text-[10px] font-mono text-cyber-emerald flex items-center justify-end">
                      <CheckCircle2 className="w-3 h-3 mr-1" /> Ready
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Bottom Proceed Action */}
          {elements.length > 0 && (
            <div className="pt-3 border-t border-command-border/60 flex justify-end">
              <button
                onClick={onProceedToPlanning}
                className="px-4 py-2 rounded-xl bg-cyber-emerald hover:bg-cyber-emerald/90 text-black text-xs font-mono font-semibold tracking-wide shadow-glow-cyan transition-all flex items-center space-x-2"
              >
                <span>Proceed to AI Test Planning</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
