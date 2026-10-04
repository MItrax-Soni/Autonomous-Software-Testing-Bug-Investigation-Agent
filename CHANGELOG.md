# CHANGELOG: Autonomous Software Testing & Bug Investigation Agent

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-10-03

### Added
- **Phase 0: Planning & Architectural Foundations**:
  - Comprehensive planning specifications (`PROJECT_PLAN.md`, `REQUIREMENTS.md`, `ARCHITECTURE.md`, `TECHNICAL_DOCUMENTATION.md`, `TASK_TRACKER.md`, `TESTING_REPORT.md`, `CHANGELOG.md`, `README.md`, `.env.example`).
- **Phase 1: Project Setup & Scaffolding**:
  - FastAPI backend configured with CORS, async lifecycle, health check endpoint (`/api/v1/health`), and `/artifacts` static mount.
  - React 18 + Vite 6 + TypeScript + Tailwind CSS 3.4 frontend setup.
  - Playwright Chromium headless engine installed.
- **Phase 2: UI Foundation & Command Center**:
  - Futuristic AI Command Center layout shell (`Sidebar`, `Topbar`, `StatusBar`).
  - 6 interactive views: `DashboardView`, `ScannerView`, `PlanningView`, `ExecutionView`, `InvestigationView`, `ReportsView`.
  - Dark slate theme with cyan/violet glows, Recharts SVG data visualizations, and zero interface emojis.
- **Phase 3: Backend & Database Architecture**:
  - SQLAlchemy 2.0 async engine with SQLite WAL mode and foreign key constraints.
  - 10 Relational entities: `Project`, `TestSession`, `DiscoveredPage`, `DiscoveredElement`, `TestScenario`, `TestExecution`, `ExecutionStep`, `Bug`, `EvidenceItem`, `Report`.
  - Pydantic v2 schemas using `ConfigDict(from_attributes=True)`.
  - REST endpoints for Projects and Sessions.
- **Phase 4: Browser Automation & Website Scanner**:
  - Pre-flight SSRF protection service (`SSRFValidator`) with DNS resolution and CIDR network deny-listing.
  - Autonomous Playwright crawler (`WebCrawlerService`) extracting routes, DOM nodes, ARIA roles, and interactive buttons/forms.
  - Scanner API endpoints (`POST /api/v1/sessions/{id}/scan`, `/pages`, `/elements`).
- **Phase 5: AI Test Planning Engine**:
  - Google Gemini integration client (`GeminiAIService`) with structured JSON scenario generation and heuristic fallback.
  - Deterministic action DSL schemas (`navigate`, `click`, `fill`, `select`, `check`, `press`, `assert_visible`, `assert_text`).
  - Scenario management endpoints (generation, update, approval toggling).
- **Phase 6: Deterministic Test Execution Engine**:
  - Playwright action runner (`DeterministicTestRunner`) executing scenarios in isolated browser contexts.
  - Multimodal evidence collector capturing full-page screenshots, console errors, and HTTP network failures.
  - Execution endpoints (`POST /api/v1/sessions/{id}/execute`, `GET /executions`).
- **Phase 7: Bug Investigation & Root Cause Analysis**:
  - Gemini bug diagnostic engine (`BugInvestigationService`) classifying defect severity (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`).
  - Mandatory strict separation between **Verified Evidence** (facts) and **AI Hypotheses** (inferred causes).
  - Bug retrieval endpoints (`GET /api/v1/sessions/{id}/bugs`, `GET /api/v1/bugs/{id}`).
- **Phase 8: Reports & Historical Analytics**:
  - Report synthesis service (`ReportGeneratorService`) compiling executive Markdown, metrics, and download endpoints (`/report/download`).
- **Phase 9: Full System Integration**:
  - End-to-end pipeline orchestrator (`AutonomousPipelineOrchestrator`) executing Crawl -> Plan -> Run -> Investigate -> Report in automated sequence.
  - Server-Sent Events (SSE) live progress stream (`GET /sessions/{id}/stream`).
- **Phase 10: Controlled Test Application & QA Hardening**:
  - Embedded local defective web app (`/controlled_test_app`, port 8088) with 5 intentional defects (auth, checkout 500 bug, modal glitch, dedicated 500 endpoint, JS uncaught exception).
- **Phase 11: Final Delivery & Documentation**:
  - 100% test coverage across 16 automated tests verified.
  - Final developer setup and user guides verified in `README.md`.

### Fixed
- **TypeScript Build Configuration & IDE Problem Decorations**:
  - Removed stale `tsconfig.tsbuildinfo` that produced casing mismatch warnings against `Sidebar.tsx` and `Topbar.tsx` on Windows.
  - Updated `package.json` build script to invoke `tsc --noEmit` rather than `tsc -b` for a non-composite single-project configuration.
  - Modernized `Sidebar.tsx` and `Topbar.tsx` to standard React 18 functional component patterns, eliminating redundant `React` default imports.
  - Strictly typed navigation tab identifiers with union type `NavTab` across `SidebarProps` and `navItems` in `Sidebar.tsx`.

