import pytest
from app.database import init_db
from app.models.page import DiscoveredPage
from app.models.element import DiscoveredElement
from app.models.session import TestSession
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

@pytest.mark.asyncio
async def test_scenario_generation_and_approval_flow(async_client):
    await init_db()

    # 1. Create a session
    sess_res = await async_client.post("/api/v1/sessions", json={
        "target_url": "http://localhost:8088",
        "max_depth": 2,
        "max_pages": 5
    })
    assert sess_res.status_code == 201
    session_id = sess_res.json()["id"]

    # 2. Trigger scenario generation
    gen_res = await async_client.post(f"/api/v1/sessions/{session_id}/generate-scenarios")
    assert gen_res.status_code == 200
    gen_data = gen_res.json()
    assert gen_data["status"] == "PLANNED"
    assert gen_data["count"] > 0
    assert len(gen_data["scenarios"]) > 0

    first_scenario_id = gen_data["scenarios"][0]["id"]

    # 3. Fetch Scenarios via GET
    get_scenarios_res = await async_client.get(f"/api/v1/sessions/{session_id}/scenarios")
    assert get_scenarios_res.status_code == 200
    scenarios = get_scenarios_res.json()
    assert len(scenarios) == gen_data["count"]

    # 4. Toggle scenario approval via PUT
    update_res = await async_client.put(
        f"/api/v1/sessions/{session_id}/scenarios/{first_scenario_id}",
        json={"is_approved": False}
    )
    assert update_res.status_code == 200
    assert update_res.json()["is_approved"] is False

    # Toggle back to True
    update_res_2 = await async_client.put(
        f"/api/v1/sessions/{session_id}/scenarios/{first_scenario_id}",
        json={"is_approved": True}
    )
    assert update_res_2.status_code == 200
    assert update_res_2.json()["is_approved"] is True
