import pytest
from app.database import init_db
from app.models.session import TestSession
from app.models.scenario import TestScenario
from app.models.execution import TestExecution, ExecutionStep
from app.models.evidence import EvidenceItem
from app.services.bug_investigator import BugInvestigationService

@pytest.mark.asyncio
async def test_bug_investigation_and_evidence_grounding(async_client):
    await init_db()

    # 1. Create Session
    sess_res = await async_client.post("/api/v1/sessions", json={
        "target_url": "http://localhost:8088",
        "max_depth": 1,
        "max_pages": 1
    })
    session_id = sess_res.json()["id"]

    # 2. Create Scenario
    gen_res = await async_client.post(f"/api/v1/sessions/{session_id}/generate-scenarios")
    scenario_id = gen_res.json()["scenarios"][0]["id"]

    # 3. Simulate a FAILED TestExecution directly in database
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        failed_exec = TestExecution(
            scenario_id=scenario_id,
            session_id=session_id,
            status="FAILED",
            duration_ms=1850,
            error_message="HTTP 500: Server returned Internal Server Error during POST /api/checkout",
            error_step_index=3
        )
        session.add(failed_exec)
        await session.flush()

        step = ExecutionStep(
            execution_id=failed_exec.id,
            step_index=3,
            action="click",
            selector="button#checkout",
            status="FAILED",
            duration_ms=1500,
            error_log="POST http://localhost:8088/api/checkout 500"
        )
        session.add(step)

        ev_net = EvidenceItem(
            execution_id=failed_exec.id,
            evidence_type="NETWORK_FAILURE",
            file_path="in-memory",
            metadata_json={"failures": [{"url": "http://localhost:8088/api/checkout", "status": 500, "status_text": "Internal Server Error"}]}
        )
        session.add(ev_net)
        await session.commit()
        execution_id = failed_exec.id

    # 4. Trigger Investigation
    inv_res = await async_client.post(f"/api/v1/executions/{execution_id}/investigate")
    assert inv_res.status_code == 200
    bug_data = inv_res.json()

    assert bug_data["severity"] == "CRITICAL"
    assert bug_data["execution_id"] == execution_id
    assert "http_errors" in bug_data["verified_evidence_json"]
    assert len(bug_data["verified_evidence_json"]["http_errors"]) == 1
    assert "probable_root_cause" in bug_data["ai_hypothesis_json"]
    assert bool(bug_data["remediation_advice"]) is True

    # 5. Retrieve via Session Bugs API
    session_bugs_res = await async_client.get(f"/api/v1/sessions/{session_id}/bugs")
    assert session_bugs_res.status_code == 200
    bugs_list = session_bugs_res.json()
    assert len(bugs_list) == 1
    assert bugs_list[0]["id"] == bug_data["id"]
