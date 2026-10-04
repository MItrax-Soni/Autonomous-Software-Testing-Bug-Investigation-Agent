import json
import asyncio
from typing import Dict, Any, List, Optional
from google import genai
from google.genai import types
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.config import settings
from app.models.execution import TestExecution
from app.models.evidence import EvidenceItem
from app.models.bug import Bug

class BugInvestigationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL
        self._client = None
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            self._client = genai.Client(api_key=self.api_key)

    @property
    def is_configured(self) -> bool:
        return self._client is not None

    async def investigate_failed_execution(self, execution_id: str) -> Optional[Bug]:
        """
        Assembles diagnostic evidence for a failed execution and uses Gemini (or heuristic fallback)
        to categorize severity, extract verified evidence, and generate probabilistic root-cause hypotheses.
        """
        # Fetch execution with steps, scenario, and evidence items
        stmt = (
            select(TestExecution)
            .options(
                selectinload(TestExecution.steps),
                selectinload(TestExecution.scenario),
                selectinload(TestExecution.evidence_items)
            )
            .where(TestExecution.id == execution_id)
        )
        res = await self.db.execute(stmt)
        execution = res.scalar_one_or_none()
        if not execution or execution.status != "FAILED":
            return None

        # Assemble verified facts
        failing_step = next((s for s in execution.steps if s.status == "FAILED"), None)
        screenshot_evidence = next((e for e in execution.evidence_items if e.evidence_type == "SCREENSHOT"), None)
        console_evidence = next((e for e in execution.evidence_items if e.evidence_type == "CONSOLE_LOG"), None)
        network_evidence = next((e for e in execution.evidence_items if e.evidence_type == "NETWORK_FAILURE"), None)
        dom_evidence = next((e for e in execution.evidence_items if e.evidence_type == "DOM_SNAPSHOT"), None)

        http_errors = network_evidence.metadata_json.get("failures", []) if network_evidence else []
        console_errors = console_evidence.metadata_json.get("logs", []) if console_evidence else []

        verified_evidence = {
            "http_errors": http_errors,
            "console_errors": console_errors,
            "failing_selector": failing_step.selector if failing_step else None,
            "exception_trace": execution.error_message,
            "failing_action": failing_step.action if failing_step else None,
            "step_index": execution.error_step_index
        }

        # Prompt Gemini if configured
        diagnosis = None
        if self.is_configured:
            diagnosis = await self._gemini_diagnose(execution, verified_evidence)

        if not diagnosis:
            diagnosis = self._heuristic_diagnose(execution, verified_evidence)

        # Persist Bug record
        bug = Bug(
            execution_id=execution.id,
            session_id=execution.session_id,
            title=diagnosis["title"],
            category=diagnosis["category"],
            severity=diagnosis["severity"],
            verified_evidence_json=verified_evidence,
            ai_hypothesis_json=diagnosis["ai_hypotheses"],
            remediation_advice=diagnosis["remediation_advice"]
        )
        self.db.add(bug)
        await self.db.commit()
        await self.db.refresh(bug)

        # Associate screenshot evidence with bug
        if screenshot_evidence:
            screenshot_evidence.bug_id = bug.id
            await self.db.commit()

        return bug

    async def _gemini_diagnose(self, execution: TestExecution, verified_evidence: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        system_instruction = (
            "You are a Principal Software Debugging & Quality Engineer. Given verified diagnostic facts from a failed "
            "browser test execution, analyze the root cause and provide structured remediation advice. "
            "CRITICAL RULE: Maintain a strict separation between verified deterministic evidence (observed HTTP codes, error messages) "
            "and AI hypotheses (inferred underlying cause). Never state an unverified inference as a proven fact. "
            "Respond ONLY with valid JSON."
        )

        prompt = f"""
Failed Test Scenario: {execution.scenario.title if execution.scenario else 'Unknown Scenario'}
Error Message: {execution.error_message}
Verified Diagnostic Evidence:
{json.dumps(verified_evidence, indent=2)}

Format response as JSON:
{{
  "title": "Clear concise summary of the defect",
  "category": "FUNCTIONAL_DEFECT" | "VALIDATION_ERROR" | "NETWORK_FAILURE" | "UI_MISSING" | "CRASH",
  "severity": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW",
  "ai_hypotheses": {{
    "summary": "High level diagnosis explanation",
    "probable_root_cause": "Detailed technical root cause explanation",
    "impact_analysis": "Business and user impact assessment",
    "confidence_score": 0.95
  }},
  "remediation_advice": "Actionable developer instructions to fix this bug"
}}
"""
        for attempt in range(2):
            try:
                response = self._client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        response_mime_type="application/json",
                        temperature=0.1
                    )
                )
                return json.loads(response.text)
            except Exception as e:
                print(f"Gemini diagnostic attempt {attempt + 1} warning: {e}")
                await asyncio.sleep(1)

        return None

    def _heuristic_diagnose(self, execution: TestExecution, verified_evidence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deterministic rule-based diagnosis when Gemini API is unavailable.
        """
        error_msg = (execution.error_message or "").lower()
        http_errors = verified_evidence.get("http_errors", [])
        has_500 = any(e.get("status") == 500 for e in http_errors) or "500" in error_msg

        if has_500:
            return {
                "title": "Uncaught Server Exception (HTTP 500)",
                "category": "CRASH",
                "severity": "CRITICAL",
                "ai_hypotheses": {
                    "summary": "Server-side exception triggered during interactive request.",
                    "probable_root_cause": "The backend endpoint failed with an internal 500 error, likely due to unhandled null values or database exception.",
                    "impact_analysis": "Blocks user transactions and may result in corrupted session state.",
                    "confidence_score": 0.95
                },
                "remediation_advice": "Inspect backend server error logs for stack traces. Implement request input validation to return HTTP 400 Bad Request instead of uncaught 500."
            }
        elif "timeout" in error_msg:
            return {
                "title": "Element Locator Timeout / Unresponsive DOM Node",
                "category": "UI_MISSING",
                "severity": "HIGH",
                "ai_hypotheses": {
                    "summary": "Target DOM element was not rendered or visible within timeout threshold.",
                    "probable_root_cause": "The component selector failed to resolve, possibly due to delayed asynchronous API response or dynamic class name mutation.",
                    "impact_analysis": "Prevents automated progression and indicates slow page hydration or missing UI component.",
                    "confidence_score": 0.88
                },
                "remediation_advice": "Verify that the target locator selector matches the current DOM markup and that dynamic client-side state correctly sets component visibility."
            }
        else:
            return {
                "title": "Assertion Failure During Test Execution",
                "category": "FUNCTIONAL_DEFECT",
                "severity": "MEDIUM",
                "ai_hypotheses": {
                    "summary": "Observed application state did not match expected scenario outcome.",
                    "probable_root_cause": "The UI content or navigation state differed from the expected business assertion.",
                    "impact_analysis": "Causes test failure and represents potential regression or out-of-date acceptance criteria.",
                    "confidence_score": 0.85
                },
                "remediation_advice": "Check whether the application behavior or design specification has updated, or fix regression in the view component."
            }
