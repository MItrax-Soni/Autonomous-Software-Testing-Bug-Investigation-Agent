import pytest
from app.database import init_db
from app.models.scenario import TestScenario

@pytest.mark.asyncio
async def test_execution_empty_and_retrieval(async_client):
    await init_db()

    # 1. Create a session
    sess_res = await async_client.post("/api/v1/sessions", json={
        "target_url": "http://localhost:8088",
        "max_depth": 1,
        "max_pages": 1
    })
    session_id = sess_res.json()["id"]

    # 2. Execution with no approved scenarios
    exec_res = await async_client.post(f"/api/v1/sessions/{session_id}/execute")
    assert exec_res.status_code == 200
    assert exec_res.json()["status"] == "NO_SCENARIOS"

    # 3. Retrieve executions list
    list_res = await async_client.get(f"/api/v1/sessions/{session_id}/executions")
    assert list_res.status_code == 200
    assert isinstance(list_res.json(), list)
