# PROJECT PLAN: Autonomous Software Testing & Bug Investigation Agent

## 1. Executive Summary & Vision

The **Autonomous Software Testing & Bug Investigation Agent** is an enterprise-grade, AI-driven QA automation and diagnostics platform. Given any permitted target web application URL, the platform autonomously launches controlled browser instances, maps discovered interactive topologies, formulates rigorous test plans via Gemini generative intelligence, executes those plans deterministically using Playwright, detects functional regressions and UX anomalies, captures comprehensive multi-angle evidence (screenshots, network logs, DOM state, console traces), conducts deep root-cause investigations, and synthesizes executive and technical bug reports.

The user experience is engineered as a **Futuristic AI Command Center**—a high-performance, dark-themed operations dashboard with rich interactive data visualization, real-time streaming status updates, and deep inspection tools.

---

## 2. Core Objectives & Scope Boundaries

### 2.1 In Scope
- **Secure Target Onboarding**: Strict SSRF-protected URL entry and validation pipeline.
- **Autonomous Crawler & Element Discovery**: Headless Chromium scanning of links, buttons, forms, inputs, dialogues, and accessibility trees.
- **Structured AI Test Generation**: Gemini-powered test scenario generation validated against strict Pydantic schemas.
- **Deterministic Playwright Execution**: Schema-driven test runner that strictly isolates AI suggestions from browser execution code.
- **Multi-Angle Evidence Capture**: Step-by-step and failure screenshots, full console logs, HTTP request/response failures, and DOM snapshots.
- **Evidence-Based Bug Investigation**: Gemini-powered triage that categorizes severity, identifies root-cause hypotheses, and strictly demarcates *verified evidence* from *AI hypotheses*.
- **Executive & Developer Reports**: Structured markdown, JSON, and visual reports with export capabilities.
- **Historical Session Analytics**: Persistent test session records with search, filter, and trend analysis.
- **Controlled Test Website**: Local intentionally flawed web application to verify the end-to-end loop without external network dependencies.

### 2.2 Out of Scope
- Destructive testing against production external applications (e.g., automated account deletion, mass purchasing).
- Bypassing CAPTCHAs, Cloudflare turnstiles, multi-factor authentication, or paywalls.
- Dynamic execution of arbitrary AI-generated Python or JavaScript code (all execution is governed by a deterministic DSL).
- Distributed multi-node test grid execution (initial design runs locally with async concurrency, architected for future Celery/Redis scaling).

---

## 3. Technology Stack & Rationale

| Layer | Selected Technology | Version | Rationale & Capabilities |
| :--- | :--- | :--- | :--- |
| **Frontend Framework** | React + Vite + TypeScript | React 19, Vite 6, TS 5 | Blazing fast HMR, strict type safety, modular component structure |
| **Styling & Theme** | Tailwind CSS + Custom CSS Variables | Tailwind v3.4+ | Deep dark-mode command center design, glassmorphism tokens, electric blue/cyan accents |
| **Icons & Visuals** | Lucide React | Latest | Clean, consistent, zero-emoji UI icons |
| **Data Visualization** | Recharts | Latest | High-fidelity interactive charts for pass rates, duration trends, and severity breakdowns |
| **Backend API** | FastAPI + Pydantic v2 | Python 3.12 - 3.14 | High-performance asynchronous API, auto-generated OpenAPI documentation, strict request/response validation |
| **Database & ORM** | SQLAlchemy 2.0 + SQLite (WAL mode) | SQLite 3 (PostgreSQL-ready) | Zero-setup local persistence with strict relational integrity and clean migration path to PostgreSQL |
| **Browser Automation** | Playwright for Python | Latest | Chromium browser engine, network interception, screenshot capture, DOM and accessibility tree inspection |
| **AI Intelligence** | Google Gemini API (gemini-2.5-flash / gemini-1.5-pro) | Google GenAI SDK | High-speed structured JSON output for test planning, root cause hypothesis generation, and report synthesis |
| **Testing Framework** | Pytest + Playwright Pytest + Vitest | Latest | Automated unit, API, and end-to-end testing |

---

## 4. Architectural Separation & Deterministic Boundaries

To guarantee safety, reliability, and security, the system enforces a strict boundary between AI generative capabilities and deterministic software execution:

```
+-----------------------------------------------------------------------------------+
|                            GENERATIVE AI BOUNDARY (Gemini)                         |
|  - Test Scenario Formulation (JSON schema only)                                    |
|  - Failure Root-Cause Hypothesis Generation                                       |
|  - Executive Bug Report Summarization & Remediation Advice                         |
+------------------------------------------+----------------------------------------+
                                           | Structured JSON (Pydantic Validated)
                                           v
+-----------------------------------------------------------------------------------+
|                        DETERMINISTIC SOFTWARE ENGINE (Python/Playwright)           |
|  - SSRF Verification & IP Deny-listing (Pre-flight DNS + redirect checks)         |
|  - Browser Launch & Headless Context Management                                   |
|  - Action Interpreter (Click, Fill, Navigate, Expect)                             |
|  - Pass/Fail Evaluation via Exact Assertions & HTTP Status Checks                  |
|  - Evidence Capture (Screenshots, console listeners, network failure interceptor)  |
|  - Database Transactions & Relational Persistence                                 |
+-----------------------------------------------------------------------------------+
```

---

## 5. Implementation Roadmap (Phases 0 - 11)

Following the Workspace Rules, the implementation is decomposed into sequential, verifiable phases:

| Phase | Title | Primary Deliverables | Target Verification |
| :--- | :--- | :--- | :--- |
| **Phase 0** | **Project Planning Only** | Complete planning documents (`PROJECT_PLAN.md`, `ARCHITECTURE.md`, `REQUIREMENTS.md`, etc.), environment audit. | Plan review and explicit user sign-off. |
| **Phase 1** | **Project Setup & Scaffolding** | Workspace structure, backend virtualenv, FastAPI app with health checks, Vite React TS frontend scaffolding, Tailwind CSS setup. | Health check endpoint returns 200 OK; frontend dev server runs clean. |
| **Phase 2** | **UI Foundation & Command Center** | Global design tokens, layout shell (Sidebar, Topbar, Status Bar), dashboard metrics screen, reusable UI components (Cards, Badges, Tables, Modals, Empty/Loading states). | Responsive dark-mode command center renders properly with mock/initial state. |
| **Phase 3** | **Backend & Database Architecture** | SQLAlchemy models, database initialization, repository layer, CRUD API endpoints for projects, sessions, test cases, and runs. | Pytest suite passes for database models and REST API endpoints. |
| **Phase 4** | **Browser Automation & Scanner** | Playwright crawler service, SSRF protection module, DOM element extraction (forms, buttons, links, inputs), journey graph builder. | Unit tests verify SSRF blocking; crawler successfully explores a local target page. |
| **Phase 5** | **AI Test Planning Engine** | Gemini API integration client, structured prompt templates, Pydantic scenario schemas, test case deduplication and validation. | Generator yields valid, schema-compliant test scenarios from element trees. |
| **Phase 6** | **Deterministic Test Execution** | Playwright action runner (click, fill, verify), timeout guards, evidence collectors (screenshots, network failures, console errors). | Runner executes scenarios against a web target and records step logs and artifacts. |
| **Phase 7** | **Bug Investigation & Root Cause** | Diagnostic analyzer, Gemini failure investigator, verified evidence vs hypothesis classifier, severity scorer. | Failed executions trigger investigation producing grounded root-cause reports. |
| **Phase 8** | **Reports & Historical Analytics** | Report generation service (HTML, Markdown, JSON), session history views, Recharts analytical widgets for pass/fail metrics. | Users can view, filter, and export comprehensive reports from the UI. |
| **Phase 9** | **Full System Integration** | Complete pipeline connection: Scanner -> Planner -> Executor -> Investigator -> Reporter in automated flow. | End-to-end autonomous run triggers from UI and executes all phases without manual intervention. |
| **Phase 10** | **QA, Security & Refinement** | Controlled defective website suite (intentional bugs), SSRF penetration testing, UI responsiveness audit, error boundary hardening. | All intentional defects detected, investigated, and verified in automated tests. |
| **Phase 11** | **Final Delivery & Documentation** | Final technical docs, setup guide, demo video/screenshots, clean `.env.example`, delivery checklist sign-off. | Complete acceptance criteria met; reproducible setup verified. |

---

## 6. Risk Management & Technical Contingencies

| Identified Risk | Impact | Likelihood | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **SSRF / Malicious URL Target** | Critical | High | Multi-stage IP resolution checks blocking 127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.169.254, and IPv6 loopbacks/private ranges before browser launch, with redirect monitoring. Controlled local test app runs on a specifically whitelisted port with explicit override token. |
| **Gemini Structured Output Drift / Rate Limits** | High | Medium | Enforce `response_mime_type="application/json"` with strict Pydantic parsing. Implement automatic retry with exponential backoff and fallback schema repair. |
| **Dynamic Single Page Applications (SPAs) Crawler Lag** | Medium | High | Use Playwright's `wait_for_load_state("networkidle")` combined with MutationObserver snapshots and explicit action timeouts. |
| **Browser Hanging / Zombie Chromium Processes** | High | Low | Playwright context manager with strict per-action and per-session timeout wrappers (`asyncio.wait_for`); automatic context cleanup in `finally` blocks. |
| **Node / Windows PowerShell Execution Restrictions** | Low | High | Use `npm.cmd` explicitly for package execution in Windows PowerShell environments. |

---

## 7. Approval Gates

Execution of Phase 1 will commence only upon user review and approval of the Phase 0 deliverables.
