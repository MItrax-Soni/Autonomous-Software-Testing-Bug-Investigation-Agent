---
trigger: always_on
---

# AUTONOMOUS SOFTWARE TESTING & BUG INVESTIGATION AGENT — WORKSPACE RULES

## 1. ROLE AND OBJECTIVE

Act as a senior software architect, full-stack developer, AI engineer, QA automation engineer, UI/UX designer, and technical project manager.

Build a real AI-powered software testing platform that accepts a website URL, scans its pages and interactions, generates test scenarios, executes them, identifies failures, investigates possible causes, and generates evidence-based reports.

Prioritize functionality, security, maintainability, usability, and premium UI/UX.

## 2. CORE DEVELOPMENT RULES

- Inspect the existing workspace before making changes.
- Follow the approved implementation phases sequentially.
- Plan architecture before coding.
- Never overwrite important files without inspection.
- Build modular, reusable, maintainable components.
- Prioritize functional implementations over mock features.
- Test every major module before integration.
- Never claim functionality works without verification.
- Resolve errors before proceeding.
- Preserve existing working code.
- Explain significant technical decisions and trade-offs.
- Obtain approval of the implementation plan before coding.

## 3. TECHNOLOGY STACK

Use the following stack unless workspace inspection identifies a strong reason to change it. Explain proposed changes before implementation.

- **Frontend:** React, Vite, TypeScript, Tailwind CSS, Lucide React, Recharts.
- **Backend:** Python, FastAPI, Pydantic, SQLAlchemy.
- **Automation:** Playwright with Chromium.
- **AI:** Gemini API.
- **Database:** SQLite initially, designed for PostgreSQL compatibility.
- **Testing:** Pytest.

Maintain clear separation between frontend, backend, automation, AI services, and database layers. All frontend-backend communication must use documented APIs.

## 4. CORE SYSTEM MODULES

Implement independent, modular components for:

- Dashboard and frontend.
- Backend APIs and orchestration.
- Website scanning and DOM inspection.
- Playwright browser automation.
- AI-based test planning.
- Test execution and result collection.
- Bug investigation and classification.
- Evidence and report generation.
- Database and session management.

## 5. CORE FUNCTIONAL REQUIREMENTS

### A. Website Scanning
- Accept and validate website URLs.
- Launch controlled browser sessions.
- Discover pages, links, buttons, forms, and interactive elements.
- Identify potential user journeys.
- Display scanning progress and discovered elements.

### B. AI Test Planning
- Generate structured test scenarios using discovered elements and workflows.
- Include test name, objective, steps, expected result, and associated page.
- Validate AI responses against predefined schemas.
- Prevent duplicate or meaningless scenarios.

### C. Automated Test Execution
- Execute approved test scenarios using Playwright.
- Capture execution status, duration, steps, and errors.
- Collect screenshots, console errors, and relevant network failures.
- Persist results for future review.

### D. Bug Investigation
- Investigate failed tests using collected evidence.
- Categorize issues by type and severity.
- Identify potential root causes.
- Clearly distinguish verified evidence from AI-generated hypotheses.
- Never present an unverified cause as confirmed.

### E. Reports and History
- Generate structured reports containing summaries, failures, severity, and evidence.
- Store testing sessions and execution history.
- Allow users to review previous results.
- Generate visualizations using actual database records.

## 6. AI ENGINEERING RULES

Use Gemini for:
- Test scenario generation.
- Failure investigation.
- Bug explanations.
- Report generation.

Use deterministic code for:
- Browser execution.
- Pass/fail evaluation.
- Database operations.
- Input validation.
- Security checks.
- Application orchestration.

Never execute arbitrary AI-generated code. Validate all structured outputs and handle API failures, invalid responses, timeouts, and rate limits.

Store API keys securely in environment variables. Never expose credentials in frontend code or logs.

## 7. SECURITY REQUIREMENTS

Treat all URLs and external website content as untrusted.

- Implement SSRF protection.
- Block localhost, private IP ranges, internal services, and cloud metadata endpoints.
- Validate URLs and resolved IP addresses before browser access.
- Prevent unsafe redirects and restricted destinations.
- Never bypass CAPTCHA, authentication, or access controls.
- Avoid destructive actions on external websites.
- Use controlled local websites for intentional failure testing.
- Never store credentials in plaintext.
- Apply secure logging, validation, and error handling.
- Obtain approval before deployment, destructive operations, or credential access.

## 8. UI/UX — FUTURISTIC AI COMMAND CENTER

UI/UX is a core development requirement, not a final-stage enhancement.

Create a premium, futuristic AI-powered software testing command center. Avoid generic dashboards, static layouts, and basic forms.

### Visual Design
- Dark theme with deep navy/charcoal backgrounds.
- Electric blue, cyan, and violet accent colors.
- Subtle gradients, ambient lighting, soft shadows, and selective glassmorphism.
- Consistent typography, spacing, borders, and reusable design tokens.
- Clean, professional, visually balanced layouts.
- Avoid excessive glow, clutter, and unnecessary decoration.

### Dashboard and Screens
Build dedicated screens for:
- Dashboard and key metrics.
- Website scanning.
- Test planning.
- Test execution.
- Bug investigation.
- Reports and history.

Include:
- Modern sidebar navigation.
- Prominent website testing action.
- Interactive charts using actual data.
- Recent testing sessions.
- Progress indicators and execution timelines.
- Test statuses and severity indicators.
- Screenshots, logs, and evidence viewers.
- Clear distinction between verified findings and AI hypotheses.

### Dynamic Interactions
- Smooth transitions and purposeful animations.
- Interactive hover states and responsive controls.
- Animated progress based on actual application state.
- Skeleton loaders and meaningful loading states.
- Polished empty, success, and error states.
- Responsive desktop, tablet, and mobile layouts.

### Implementation Standards
- Use reusable React components, Tailwind CSS, and Lucide icons.
- Never use emojis as interface icons.
- Ensure accessibility, readable contrast, keyboard navigation, and visible focus states.
- Every button, menu, filter, chart, and form must function.
- Connect all screens to real backend data.
- Never use fake metrics or decorative non-functional controls.
- Inspect and test each major screen before proceeding.

Never sacrifice functionality or usability for visual effects.

## 9. DATABASE AND API ARCHITECTURE

Create database entities for:

- Websites/projects.
- Testing sessions.
- Discovered pages and elements.
- Test cases.
- Test executions.
- Bugs and findings.
- Evidence.
- Reports.

Implement appropriate relationships, constraints, timestamps, indexes, and migrations.

Document API endpoints, request/response schemas, validation, and error handling. Keep frontend and backend contracts consistent.

## 10. TESTING AND QUALITY ASSURANCE

Implement and verify:

- Unit tests for critical services.
- API validation and persistence tests.
- Browser automation tests.
- Successful and failed execution paths.
- AI output validation and error handling.
- Frontend interactions and API integration.
- URL restrictions and SSRF protection.
- End-to-end workflows.

Never fabricate test results, screenshots, reports, or performance metrics.

## 11. CONTROLLED TEST WEBSITE

Create or use a local test website containing interactive elements and intentional defects.

Use it to verify the complete workflow:

Website scanning → Element discovery → Test generation → Execution → Failure detection → Evidence capture → Bug investigation → Reporting.

Do not perform destructive or uncontrolled testing on external websites.

## 12. PROJECT DOCUMENTATION

Maintain the following files:

- `PROJECT_PLAN.md` — scope and roadmap.
- `REQUIREMENTS.md` — functional and non-functional requirements.
- `ARCHITECTURE.md` — system architecture.
- `TASK_TRACKER.md` — implementation progress.
- `TECHNICAL_DOCUMENTATION.md` — APIs and implementation.
- `TESTING_REPORT.md` — actual test results.
- `CHANGELOG.md` — project modifications.
- `README.md` — setup and usage.
- `.env.example` — required environment variables without secrets.

Update documentation whenever architecture, setup, APIs, or functionality changes.

## 13. PHASE-WISE IMPLEMENTATION

Work incrementally. Do not implement the entire application in one unverified step.

**Phase 0 — Planning**
- Inspect workspace.
- Finalize requirements, architecture, technology stack, database, APIs, security, UI/UX design system, folder structure, risks, and roadmap.
- Create planning documentation only.
- Do not implement features.

**Phase 1 — Project Setup**
- Create approved folder structure.
- Initialize frontend and backend.
- Configure dependencies and environment.
- Verify application health checks.

**Phase 2 — UI Foundation**
- Build design system, navigation, responsive layouts, dashboard, and reusable components.

**Phase 3 — Backend and Database**
- Implement models, migrations, APIs, validation, and persistence.

**Phase 4 — Browser Automation**
- Integrate Playwright for secure website scanning, element discovery, and evidence capture.

**Phase 5 — AI Test Planning**
- Integrate Gemini.
- Generate and validate structured test scenarios.

**Phase 6 — Test Execution**
- Execute approved scenarios.
- Collect and persist results.

**Phase 7 — Bug Investigation**
- Analyze failures.
- Classify findings.
- Connect evidence and possible root causes.

**Phase 8 — Reports and History**
- Implement reports, session history, and data visualizations.

**Phase 9 — Integration**
- Connect all modules.
- Verify complete end-to-end workflows.

**Phase 10 — QA and Refinement**
- Test functionality, fix errors, inspect UI, improve responsiveness, and verify security.

**Phase 11 — Final Delivery**
- Complete documentation, setup instructions, known limitations, and delivery checklist.

Do not skip phases. Obtain approval of the detailed plan before starting implementation.

## 14. PHASE COMPLETION PROTOCOL

After each phase, report:

1. Work completed.
2. Files created or modified.
3. Tests performed and actual results.
4. Remaining errors or limitations.
5. Documentation updated.
6. Acceptance criteria met or unmet.
7. Recommended next phase.

Do not proceed while critical unresolved issues remain. Never claim success without evidence.

## 15. FINAL ACCEPTANCE CRITERIA

The completed platform must allow users to:

- Submit a permitted website URL.
- Scan and discover website elements.
- Generate structured test scenarios.
- Execute tests through Playwright.
- Detect and classify failures.
- Capture screenshots and supporting evidence.
- Investigate potential root causes.
- Generate and access saved reports.
- Review historical testing sessions.

The final product must include a polished futuristic interface, reliable backend integration, persistent database, secure URL handling, meaningful error states, responsive layouts, and complete setup documentation.

**FINAL PRINCIPLE: Build a secure, functional, intelligent, and visually polished software product. Work incrementally, preserve existing work, verify every major feature, and prioritize engineering quality over rapid code generation.**