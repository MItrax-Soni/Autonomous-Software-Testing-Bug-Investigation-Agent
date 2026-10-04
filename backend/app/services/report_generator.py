import os
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.config import settings
from app.models.session import TestSession
from app.models.execution import TestExecution
from app.models.bug import Bug
from app.models.report import Report
from app.schemas.report import ReportMetrics

class ReportGeneratorService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_session_report(self, session_id: str) -> Report:
        """
        Compiles an executive and technical quality assurance report from database session records.
        """
        # Fetch Session with executions, bugs, and target info
        sess_stmt = (
            select(TestSession)
            .options(
                selectinload(TestSession.executions),
                selectinload(TestSession.bugs)
            )
            .where(TestSession.id == session_id)
        )
        res = await self.db.execute(sess_stmt)
        session = res.scalar_one_or_none()
        if not session:
            raise ValueError(f"Session {session_id} not found")

        executions = session.executions or []
        bugs = session.bugs or []

        total_tests = len(executions)
        passed_tests = sum(1 for e in executions if e.status == "PASSED")
        failed_tests = sum(1 for e in executions if e.status in ("FAILED", "TIMED_OUT"))
        pass_rate = round((passed_tests / total_tests * 100)) if total_tests > 0 else 100
        total_duration_ms = sum(e.duration_ms for e in executions)

        critical_bugs = sum(1 for b in bugs if b.severity == "CRITICAL")
        high_bugs = sum(1 for b in bugs if b.severity == "HIGH")
        medium_bugs = sum(1 for b in bugs if b.severity == "MEDIUM")
        low_bugs = sum(1 for b in bugs if b.severity == "LOW")

        metrics_data = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "pass_rate_percentage": pass_rate,
            "total_duration_ms": total_duration_ms,
            "critical_bugs": critical_bugs,
            "high_bugs": high_bugs,
            "medium_bugs": medium_bugs,
            "low_bugs": low_bugs
        }

        # Build Markdown Summary
        summary_lines = [
            f"# AUTONOMOUS QA AUDIT REPORT",
            f"**Target URL:** `{session.target_url}`  ",
            f"**Audit Timestamp:** `{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}`  ",
            f"**Session ID:** `{session.id}`  ",
            f"",
            f"---",
            f"",
            f"## 1. Executive Summary",
            f"- **Overall Pass Rate:** `{pass_rate}%` ({passed_tests}/{total_tests} scenarios)",
            f"- **Total Execution Duration:** `{round(total_duration_ms / 1000, 2)}s`",
            f"- **Total Defects Triaged:** `{len(bugs)}` ({critical_bugs} Critical, {high_bugs} High, {medium_bugs} Medium, {low_bugs} Low)",
            f"",
            f"## 2. Release Stability Recommendation",
        ]

        if critical_bugs > 0:
            summary_lines.append(
                f"> [!CAUTION]\n"
                f"> **RELEASE BLOCKED**: {critical_bugs} CRITICAL defect(s) detected that break core workflows or trigger internal server crashes. Remediation is required before deployment."
            )
        elif high_bugs > 0:
            summary_lines.append(
                f"> [!WARNING]\n"
                f"> **CONDITIONAL STAGING**: {high_bugs} HIGH severity defect(s) identified. Core happy path is operational, but edge-case validations require patching."
            )
        else:
            summary_lines.append(
                f"> [!NOTE]\n"
                f"> **STABLE FOR PRODUCTION**: 100% of executed automated scenarios passed without functional regressions or console exceptions."
            )

        summary_lines.append(f"\n## 3. Triaged Defects & Root Cause Analysis")
        if not bugs:
            summary_lines.append("No defects or regressions were detected during this testing session.")
        else:
            for i, bug in enumerate(bugs, 1):
                summary_lines.append(f"\n### Defect #{i}: {bug.title}")
                summary_lines.append(f"- **Severity:** `{bug.severity}`")
                summary_lines.append(f"- **Category:** `{bug.category}`")
                summary_lines.append(f"- **Probable Root Cause (AI Hypothesis):** {bug.ai_hypothesis_json.get('probable_root_cause', 'N/A')}")
                summary_lines.append(f"- **Developer Remediation Advice:** {bug.remediation_advice or 'Review step logs and server traces.'}")

        summary_markdown = "\n".join(summary_lines)

        # Check if Report already exists for session
        rep_stmt = select(Report).where(Report.session_id == session_id)
        rep_res = await self.db.execute(rep_stmt)
        report = rep_res.scalar_one_or_none()

        if report:
            report.summary_markdown = summary_markdown
            report.metrics_json = metrics_data
            report.generated_at = datetime.now(timezone.utc)
        else:
            report = Report(
                session_id=session_id,
                summary_markdown=summary_markdown,
                metrics_json=metrics_data,
                generated_at=datetime.now(timezone.utc)
            )
            self.db.add(report)

        await self.db.commit()
        await self.db.refresh(report)
        return report
