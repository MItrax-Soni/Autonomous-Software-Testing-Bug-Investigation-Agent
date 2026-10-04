export type SessionStatus =
  | 'DRAFT'
  | 'SCANNING'
  | 'SCANNED'
  | 'PLANNING'
  | 'PLANNED'
  | 'EXECUTING'
  | 'INVESTIGATING'
  | 'COMPLETED'
  | 'FAILED';

export type BugSeverity = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';

export type ExecutionStatus = 'PASSED' | 'FAILED' | 'TIMED_OUT' | 'SKIPPED';

export interface Project {
  id: string;
  name: string;
  target_url: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface TestSession {
  id: string;
  project_id: string;
  target_url: string;
  status: SessionStatus;
  max_depth: number;
  max_pages: number;
  total_tests: number;
  passed_tests: number;
  failed_tests: number;
  error_summary?: string;
  started_at: string;
  completed_at?: string;
}

export interface DiscoveredPage {
  id: string;
  session_id: string;
  url: string;
  title?: string;
  http_status: number;
  depth: number;
  screenshot_path?: string;
  discovered_at: string;
}

export interface DiscoveredElement {
  id: string;
  page_id: string;
  tag_name: string;
  element_type: string;
  selector: string;
  semantic_label?: string;
  attributes: Record<string, string>;
  is_interactive: boolean;
  parent_form_id?: string;
}

export interface TestStep {
  step_index: number;
  action: 'navigate' | 'click' | 'fill' | 'select' | 'check' | 'press' | 'assert_visible' | 'assert_text';
  selector?: string;
  value?: string;
  expected?: string;
  timeout_ms?: number;
}

export interface TestScenario {
  id: string;
  session_id: string;
  title: string;
  description: string;
  category: 'POSITIVE' | 'NEGATIVE' | 'BOUNDARY' | 'RESPONSIVENESS';
  target_page_url: string;
  steps: TestStep[];
  expected_result: string;
  is_approved: boolean;
  order_index: number;
}

export interface ExecutionStepResult {
  id: string;
  step_index: number;
  action: string;
  selector?: string;
  value?: string;
  status: 'PASSED' | 'FAILED';
  duration_ms: number;
  error_log?: string;
  screenshot_path?: string;
}

export interface TestExecution {
  id: string;
  scenario_id: string;
  session_id: string;
  scenario_title: string;
  status: ExecutionStatus;
  duration_ms: number;
  error_message?: string;
  error_step_index?: number;
  executed_at: string;
  steps: ExecutionStepResult[];
}

export interface BugFinding {
  id: string;
  execution_id: string;
  session_id: string;
  title: string;
  category: string;
  severity: BugSeverity;
  verified_evidence: {
    http_errors: Array<{ url: string; status: number; text: string }>;
    console_errors: Array<{ type: string; text: string }>;
    failing_selector?: string;
    exception_trace?: string;
    dom_snippet?: string;
  };
  ai_hypotheses: {
    summary: string;
    probable_root_cause: string;
    impact_analysis: string;
    confidence_score: number;
  };
  remediation_advice: string;
  screenshot_url?: string;
  created_at: string;
}

export interface ReportMetrics {
  total_tests: number;
  passed_tests: number;
  failed_tests: number;
  pass_rate_percentage: number;
  total_duration_ms: number;
  critical_bugs: number;
  high_bugs: number;
  medium_bugs: number;
  low_bugs: number;
}

export interface TestReport {
  id: string;
  session_id: string;
  summary_markdown: string;
  metrics: ReportMetrics;
  generated_at: string;
}
