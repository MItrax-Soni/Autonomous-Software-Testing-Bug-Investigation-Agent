import asyncio
import traceback
from typing import Dict, Any, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.session import TestSession
from app.models.execution import TestExecution
from app.services.crawler import WebCrawlerService
from app.services.gemini_client import gemini_service
from app.services.test_runner import DeterministicTestRunner
from app.services.bug_investigator import BugInvestigationService
from app.services.report_generator import ReportGeneratorService
from app.models.scenario import TestScenario
from app.models.page import DiscoveredPage
from app.models.element import DiscoveredElement

class AutonomousPipelineOrchestrator:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def run_full_pipeline(self, session_id: str) -> Dict[str, Any]:
        """
        Executes the entire autonomous lifecycle sequentially:
        1. Scan & Crawl Topology
        2. Formulate Test Scenarios
        3. Deterministic Playwright Execution
        4. Multimodal Bug Investigation on Failures
        5. Executive QA Report Generation
        """
        res = await self.db.execute(select(TestSession).where(TestSession.id == session_id))
        session = res.scalar_one_or_none()
        if not session:
            raise ValueError(f"Session {session_id} not found")

        try:
            # Step 1: Scan & Crawl
            crawler = WebCrawlerService(db=self.db)
            crawl_res = await crawler.crawl_target(session_id=session_id)

            # Step 2: Formulate Scenarios
            pages_res = await self.db.execute(select(DiscoveredPage).where(DiscoveredPage.session_id == session_id))
            pages = pages_res.scalars().all()
            elements_res = await self.db.execute(
                select(DiscoveredElement)
                .join(DiscoveredPage, DiscoveredElement.page_id == DiscoveredPage.id)
                .where(DiscoveredPage.session_id == session_id)
            )
            elements = elements_res.scalars().all()

            pages_dict = [{"url": p.url, "title": p.title} for p in pages]
            elements_dict = [
                {"tag_name": e.tag_name, "element_type": e.element_type, "selector": e.selector, "semantic_label": e.semantic_label}
                for e in elements
            ]

            scenarios_raw = await gemini_service.generate_test_scenarios(
                target_url=session.target_url,
                pages=pages_dict,
                elements=elements_dict
            )

            for idx, sc in enumerate(scenarios_raw):
                db_scenario = TestScenario(
                    session_id=session.id,
                    title=sc.get("title", f"Scenario #{idx + 1}"),
                    description=sc.get("description", "Autonomous journey"),
                    category=sc.get("category", "POSITIVE"),
                    target_page_url=sc.get("target_page_url", session.target_url),
                    steps_json=sc.get("steps_json", []),
                    expected_result=sc.get("expected_result", "Successful state"),
                    is_approved=True,
                    order_index=idx + 1
                )
                self.db.add(db_scenario)

            session.status = "PLANNED"
            await self.db.commit()

            # Step 3: Execute Scenarios
            runner = DeterministicTestRunner(db=self.db)
            exec_res = await runner.execute_approved_scenarios(session_id=session_id)

            # Step 4: Investigate Any Failures
            failed_execs_res = await self.db.execute(
                select(TestExecution).where(
                    TestExecution.session_id == session_id,
                    TestExecution.status == "FAILED"
                )
            )
            failed_executions = failed_execs_res.scalars().all()

            if failed_executions:
                session.status = "INVESTIGATING"
                await self.db.commit()
                investigator = BugInvestigationService(db=self.db)
                for f_exec in failed_executions:
                    await investigator.investigate_failed_execution(execution_id=f_exec.id)

            # Step 5: Synthesize Executive Report
            report_service = ReportGeneratorService(db=self.db)
            report = await report_service.generate_session_report(session_id=session_id)

            session.status = "COMPLETED"
            await self.db.commit()

            return {
                "session_id": session_id,
                "status": "COMPLETED",
                "pages_crawled": crawl_res.get("pages_discovered", 0),
                "scenarios_generated": len(scenarios_raw),
                "tests_passed": exec_res.get("passed", 0),
                "tests_failed": exec_res.get("failed", 0),
                "report_id": report.id
            }

        except Exception as e:
            session.status = "FAILED"
            session.error_summary = f"{str(e)}\n{traceback.format_exc()}"
            await self.db.commit()
            raise e
