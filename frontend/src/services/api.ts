import { Project, TestSession, DiscoveredPage, DiscoveredElement, TestScenario, TestExecution, BugFinding, TestReport } from '../types';

const API_BASE = '/api/v1';

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(errorData.detail || `Request failed with status ${res.status}`);
  }

  return res.json();
}

export const api = {
  // System Health
  getHealth: () => request<{ status: string; environment: string; gemini_configured: boolean }>('/health'),

  // Projects
  getProjects: () => request<Project[]>('/projects'),
  createProject: (data: { name: string; target_url: string; description?: string }) =>
    request<Project>('/projects', { method: 'POST', body: JSON.stringify(data) }),

  // Sessions
  getSessions: (projectId?: string) =>
    request<TestSession[]>(`/sessions${projectId ? `?project_id=${projectId}` : ''}`),
  getSession: (sessionId: string) => request<TestSession>(`/sessions/${sessionId}`),
  createSession: (data: { target_url: string; max_depth?: number; max_pages?: number }) =>
    request<TestSession>('/sessions', { method: 'POST', body: JSON.stringify(data) }),

  // Crawler & Scanner
  startScan: (sessionId: string) =>
    request<{ status: string; pages_count: number }>(`/sessions/${sessionId}/scan`, { method: 'POST' }),
  getDiscoveredPages: (sessionId: string) =>
    request<DiscoveredPage[]>(`/sessions/${sessionId}/pages`),
  getDiscoveredElements: (sessionId: string) =>
    request<DiscoveredElement[]>(`/sessions/${sessionId}/elements`),

  // AI Test Planning
  generateScenarios: (sessionId: string) =>
    request<{ count: number; scenarios: TestScenario[] }>(`/sessions/${sessionId}/generate-scenarios`, { method: 'POST' }),
  getScenarios: (sessionId: string) =>
    request<TestScenario[]>(`/sessions/${sessionId}/scenarios`),
  toggleScenarioApproval: (sessionId: string, scenarioId: string, isApproved: boolean) =>
    request<TestScenario>(`/sessions/${sessionId}/scenarios/${scenarioId}`, {
      method: 'PUT',
      body: JSON.stringify({ is_approved: isApproved }),
    }),

  // Test Execution
  executeTests: (sessionId: string) =>
    request<{ status: string; session_id: string }>(`/sessions/${sessionId}/execute`, { method: 'POST' }),
  getExecutions: (sessionId: string) =>
    request<TestExecution[]>(`/sessions/${sessionId}/executions`),

  // Bug Investigation
  getBugs: (sessionId: string) => request<BugFinding[]>(`/sessions/${sessionId}/bugs`),
  getBugDetail: (bugId: string) => request<BugFinding>(`/bugs/${bugId}`),

  // Reports
  generateReport: (sessionId: string) =>
    request<TestReport>(`/sessions/${sessionId}/report`, { method: 'POST' }),
  getReport: (sessionId: string) => request<TestReport>(`/sessions/${sessionId}/report`),
};
