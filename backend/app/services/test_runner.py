import asyncio
import os
import time
import uuid
from typing import List, Dict, Any, Optional
from playwright.async_api import async_playwright, expect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.models.session import TestSession
from app.models.scenario import TestScenario
from app.models.execution import TestExecution, ExecutionStep
from app.models.evidence import EvidenceItem
from app.services.ssrf_validator import SSRFValidator

class DeterministicTestRunner:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute_approved_scenarios(self, session_id: str) -> Dict[str, Any]:
        """
        Executes all approved scenarios for a session sequentially in isolated Playwright browser contexts.
        Captures step results, console logs, network errors, and failure artifacts.
        """
        # 1. Fetch Session and Scenarios
        sess_stmt = select(TestSession).where(TestSession.id == session_id)
        sess_res = await self.db.execute(sess_stmt)
        session = sess_res.scalar_one_or_none()
        if not session:
            raise ValueError(f"Session {session_id} not found")

        scen_stmt = (
            select(TestScenario)
            .where(TestScenario.session_id == session_id, TestScenario.is_approved == True)
            .order_by(TestScenario.order_index.asc())
        )
        scen_res = await self.db.execute(scen_stmt)
        scenarios = scen_res.scalars().all()

        if not scenarios:
            return {"status": "NO_SCENARIOS", "executed": 0, "passed": 0, "failed": 0}

        session.status = "EXECUTING"
        await self.db.commit()

        session_artifacts_dir = os.path.join(settings.ARTIFACTS_DIR, session_id)
        os.makedirs(session_artifacts_dir, exist_ok=True)

        passed_count = 0
        failed_count = 0

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=settings.PLAYWRIGHT_HEADLESS,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
            )

            for scenario in scenarios:
                context = await browser.new_context(
                    viewport={"width": settings.BROWSER_VIEWPORT_WIDTH, "height": settings.BROWSER_VIEWPORT_HEIGHT}
                )
                page = await context.new_page()

                console_logs: List[Dict[str, Any]] = []
                network_failures: List[Dict[str, Any]] = []

                # Attach Telemetry Listeners
                page.on("console", lambda msg: console_logs.append({
                    "type": msg.type,
                    "text": msg.text,
                    "location": msg.location
                }))

                page.on("response", lambda resp: network_failures.append({
                    "url": resp.url,
                    "status": resp.status,
                    "status_text": resp.status_text
                }) if resp.status >= 400 else None)

                # Initialize Execution Record
                execution = TestExecution(
                    scenario_id=scenario.id,
                    session_id=session.id,
                    status="PASSED",
                    duration_ms=0
                )
                self.db.add(execution)
                await self.db.flush()

                scenario_start_time = time.time()
                scenario_failed = False
                error_summary = None
                failing_step_index = None

                steps = scenario.steps_json or []
                for step_data in steps:
                    step_index = step_data.get("step_index", 1)
                    action = step_data.get("action")
                    selector = step_data.get("selector")
                    value = step_data.get("value")
                    expected_target = step_data.get("expected")
                    timeout = step_data.get("timeout_ms", settings.PLAYWRIGHT_ACTION_TIMEOUT_MS)

                    step_start_time = time.time()
                    step_status = "PASSED"
                    step_error = None
                    step_screenshot_rel = None

                    try:
                        # Deterministic Action Dispatcher
                        if action == "navigate":
                            nav_url = selector or scenario.target_page_url
                            SSRFValidator.validate_url(nav_url)
                            await page.goto(nav_url, wait_until="domcontentloaded", timeout=timeout)
                        elif action == "click":
                            await page.locator(selector).click(timeout=timeout)
                        elif action == "fill":
                            await page.locator(selector).fill(str(value or ""), timeout=timeout)
                        elif action == "select":
                            await page.locator(selector).select_option(str(value or ""), timeout=timeout)
                        elif action == "check":
                            await page.locator(selector).check(timeout=timeout)
                        elif action == "press":
                            await page.locator(selector).press(str(value or "Enter"), timeout=timeout)
                        elif action == "assert_visible":
                            await expect(page.locator(selector)).to_be_visible(timeout=timeout)
                        elif action == "assert_hidden":
                            await expect(page.locator(selector)).to_be_hidden(timeout=timeout)
                        elif action == "assert_text":
                            await expect(page.locator(selector)).to_contain_text(str(expected_target or value or ""), timeout=timeout)
                        elif action == "assert_url":
                            await expect(page).to_have_url(str(expected_target or value or ""), timeout=timeout)
                        else:
                            raise ValueError(f"Unknown DSL action: '{action}'")

                    except Exception as step_exc:
                        step_status = "FAILED"
                        step_error = str(step_exc)
                        scenario_failed = True
                        error_summary = step_error
                        failing_step_index = step_index

                        # Capture Failure Viewport Screenshot
                        failure_img_name = f"failure_exec_{execution.id[:8]}_step_{step_index}.png"
                        failure_img_path = os.path.join(session_artifacts_dir, failure_img_name)
                        try:
                            await page.screenshot(path=failure_img_path, full_page=False)
                            step_screenshot_rel = f"/artifacts/{session_id}/{failure_img_name}"

                            # Persist Evidence Item
                            ev_screenshot = EvidenceItem(
                                execution_id=execution.id,
                                evidence_type="SCREENSHOT",
                                file_path=step_screenshot_rel,
                                metadata_json={"step_index": step_index, "action": action, "selector": selector}
                            )
                            self.db.add(ev_screenshot)
                        except Exception as shot_err:
                            print(f"Screenshot capture warning: {shot_err}")

                        # Capture DOM Snapshot
                        dom_filename = f"dom_exec_{execution.id[:8]}.html"
                        dom_path = os.path.join(session_artifacts_dir, dom_filename)
                        try:
                            content = await page.content()
                            with open(dom_path, "w", encoding="utf-8") as f:
                                f.write(content)
                            ev_dom = EvidenceItem(
                                execution_id=execution.id,
                                evidence_type="DOM_SNAPSHOT",
                                file_path=f"/artifacts/{session_id}/{dom_filename}",
                                metadata_json={"step_index": step_index}
                            )
                            self.db.add(ev_dom)
                        except Exception as dom_err:
                            print(f"DOM capture warning: {dom_err}")

                    step_duration_ms = int((time.time() - step_start_time) * 1000)

                    # Persist Step Result
                    db_step = ExecutionStep(
                        execution_id=execution.id,
                        step_index=step_index,
                        action=action,
                        selector=selector,
                        value=str(value) if value is not None else None,
                        status=step_status,
                        duration_ms=step_duration_ms,
                        error_log=step_error,
                        screenshot_path=step_screenshot_rel
                    )
                    self.db.add(db_step)

                    # Abort scenario sequence on first failure
                    if scenario_failed:
                        break

                total_duration_ms = int((time.time() - scenario_start_time) * 1000)
                execution.duration_ms = total_duration_ms

                # Record console errors and network errors as Evidence Items
                if console_logs:
                    error_logs = [log for log in console_logs if log["type"] in ("error", "warning")]
                    if error_logs:
                        self.db.add(EvidenceItem(
                            execution_id=execution.id,
                            evidence_type="CONSOLE_LOG",
                            file_path="in-memory",
                            metadata_json={"logs": error_logs}
                        ))

                if network_failures:
                    self.db.add(EvidenceItem(
                        execution_id=execution.id,
                        evidence_type="NETWORK_FAILURE",
                        file_path="in-memory",
                        metadata_json={"failures": network_failures}
                    ))

                if scenario_failed:
                    execution.status = "FAILED"
                    execution.error_message = error_summary
                    execution.error_step_index = failing_step_index
                    failed_count += 1
                else:
                    execution.status = "PASSED"
                    passed_count += 1

                await context.close()

            await browser.close()

        # Update Session Summary Metrics
        session.passed_tests = passed_count
        session.failed_tests = failed_count
        session.status = "COMPLETED"
        await self.db.commit()

        return {
            "session_id": session_id,
            "status": "COMPLETED",
            "total_executed": len(scenarios),
            "passed": passed_count,
            "failed": failed_count
        }
