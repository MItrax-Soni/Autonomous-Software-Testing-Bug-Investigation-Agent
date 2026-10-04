# Autonomous Software Testing & Bug Investigation Agent

An enterprise-grade, autonomous software testing and defect diagnosis platform. The agent accepts any permitted website URL, explores its interactive surfaces using Playwright browser automation, maps DOM elements and user flows, formulates structured test scenarios using Google Gemini generative AI, executes those tests deterministically, captures multimodal diagnostic evidence upon failure (screenshots, network failures, console logs, DOM state), and conducts deep root-cause investigations.

The user interface is engineered as a **Futuristic AI Command Center**—a dark-themed, data-rich operations dashboard providing real-time telemetry, interactive topologies, and deep-dive diagnostic inspection.

---

## Key Capabilities

- **Autonomous Web Crawler**: Headless Chromium scanning of links, buttons, inputs, dropdowns, forms, and accessibility trees.
- **AI Test Scenario Formulation**: Gemini-powered test generation covering happy paths, negative validation, and edge-case user journeys.
- **Deterministic Test Runner**: Strict separation between AI suggestions and Playwright execution code—zero arbitrary script evaluation (`eval`).
- **Multimodal Evidence Vault**: Automatic capture of full-page screenshots, failing element snapshots, browser console traces, and failed HTTP requests.
- **Evidence-Based Bug Investigation**: Gemini-powered failure diagnosis that categorizes severity and clearly separates **Verified Evidence** from **AI Hypotheses**.
- **Futuristic AI Command Center**: Dark slate UI with electric blue and violet accents, interactive Recharts telemetry, and live execution streams (zero emojis).
- **Controlled Defective Test App**: Embedded local testing sandbox with intentional defects (auth, checkout validation, modal disappearance, 500 API error, JS crash) for rigorous end-to-end verification.
- **Robust Security**: Multi-stage SSRF protection pipeline blocking private networks, cloud metadata endpoints, and unauthorized internal destinations.

---

## Architecture Overview

```
[ Frontend: Futuristic AI Command Center ] (React + Vite + TypeScript + Tailwind)
                     |
                     | REST API & SSE Events
                     v
[ Backend API & Workflow Orchestrator ] (FastAPI + Pydantic v2)
         |                           |
         | (SSRF Guard & DB)         | (Structured Prompts / JSON)
         v                           v
[ SQLite / SQLAlchemy ORM ]     [ Google Gemini Generative AI ]
         |                           | (Test Plans & Root Causes)
         +-------------+-------------+
                       |
                       v
         [ Playwright Automation Engine ]
                       |
            +----------+----------+
            |                     |
            v                     v
[ Controlled Test App ]   [ Permitted Web Targets ]
```

---

## Technology Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Frontend** | React 19, Vite, TypeScript | Fast HMR, strict type safety, modular architecture |
| **Styling** | Tailwind CSS v3.4+ | Deep dark-mode command center design, glassmorphism tokens |
| **Icons & Visuals** | Lucide React | Clean, modern, zero-emoji UI icons |
| **Charts** | Recharts | Interactive SVG metrics and trend charts |
| **Backend** | Python 3.12 - 3.14, FastAPI | Asynchronous ASGI API, auto OpenAPI documentation |
| **Validation** | Pydantic v2 | Strict schema validation for requests, DB models, and AI outputs |
| **Database** | SQLAlchemy 2.0, SQLite (WAL) | Zero-setup local persistence, PostgreSQL-ready |
| **Browser Automation**| Playwright for Python | Headless Chromium automation, network/console listeners |
| **AI Reasoning** | Google Gemini API (gemini-2.5-flash) | Fast, structured JSON generation and failure diagnosis |
| **Testing** | Pytest, Vitest | Comprehensive unit, integration, and E2E testing |

---

## Implementation Roadmap

- [x] **Phase 0: Project Planning Only** (Master docs, architecture, schema, API spec, security)
- [x] **Phase 1: Project Setup & Scaffolding** (FastAPI backend, Vite frontend, Playwright Chromium installed)
- [x] **Phase 2: UI Foundation & Command Center** (Futuristic layout shell, design tokens, 6 views, Recharts)
- [x] **Phase 3: Backend & Database Architecture** (SQLAlchemy 2.0 async engine, 10 models, CRUD endpoints)
- [x] **Phase 4: Browser Automation & Scanner** (SSRF protection guard, Playwright crawler, DOM element extraction)
- [x] **Phase 5: AI Test Planning Engine** (Gemini client, scenario generator, deterministic DSL schemas)
- [x] **Phase 6: Deterministic Test Execution** (Playwright action runner, multimodal evidence vault)
- [x] **Phase 7: Bug Investigation & Root Cause** (Gemini diagnostic triage, verified evidence vs hypothesis split)
- [x] **Phase 8: Reports & Historical Analytics** (Report generator service, metrics aggregation, Markdown export)
- [x] **Phase 9: Full System Integration** (Autonomous end-to-end pipeline orchestrator & SSE streaming)
- [x] **Phase 10: Controlled Test Application & QA** (Local defective app with 5 bugs, SSRF penetration tests)
- [x] **Phase 11: Final Delivery & Documentation** (16/16 automated tests passed, complete documentation)

---

## Project Structure

```
.
├── .agents/                    # Workspace rules and instructions
├── .env.example                # Template environment variables
├── README.md                   # This documentation
├── PROJECT_PLAN.md             # Detailed roadmap and risk management
├── REQUIREMENTS.md             # Functional & non-functional requirements
├── ARCHITECTURE.md             # System architecture and data flows
├── TASK_TRACKER.md             # Phase-by-phase implementation tracker
├── TECHNICAL_DOCUMENTATION.md  # Database schema, API spec, and Playwright DSL
├── TESTING_REPORT.md           # Environment audit and testing strategy
├── CHANGELOG.md                # Version history
├── backend/                    # FastAPI application & Pytest suite
├── frontend/                   # React + Vite Command Center
├── controlled_test_app/        # Local intentionally defective app (port 8088)
└── artifacts/                  # Diagnostic screenshots, logs, and reports
```

---

## Developer Quickstart

### 1. Controlled Test Target Application
```bash
# In terminal 1: Start the local benchmark application (port 8088)
cd "d:\Projects\Autonomous Software Testing & Bug Investigation Agent"
.\backend\.venv\Scripts\python.exe controlled_test_app/app.py
```

### 2. Backend API Service
```bash
# In terminal 2: Start FastAPI service (port 8000)
cd "d:\Projects\Autonomous Software Testing & Bug Investigation Agent\backend"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Futuristic Command Center
```bash
# In terminal 3: Start Vite development server (port 5173)
cd "d:\Projects\Autonomous Software Testing & Bug Investigation Agent\frontend"
npm.cmd run dev
```

### 4. Running the Test Suite
```bash
cd "d:\Projects\Autonomous Software Testing & Bug Investigation Agent\backend"
.\.venv\Scripts\python.exe -m pytest tests -v
```

---

## Security Guidelines

- **SSRF Protection**: All URLs submitted for scanning undergo pre-flight DNS resolution and IP address filtering against private and internal subnets.
- **Execution Sandboxing**: All test steps are strictly interpreted by a deterministic action handler. Arbitrary code execution or `eval()` is strictly prohibited.
- **Credential Safety**: The `GEMINI_API_KEY` is loaded exclusively on the backend server and never exposed to the frontend.
