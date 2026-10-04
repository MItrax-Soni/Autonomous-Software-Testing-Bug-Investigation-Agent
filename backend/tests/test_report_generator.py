import pytest
from app.database import init_db

@pytest.mark.asyncio
async def test_report_generation_and_metrics_aggregation(async_client):
    await init_db()

    # 1. Create a session
    sess_res = await async_client.post("/api/v1/sessions", json={
        "target_url": "http://localhost:8088",
        "max_depth": 1,
        "max_pages": 1
    })
    session_id = sess_res.json()["id"]

    # 2. Generate Report via API
    rep_res = await async_client.post(f"/api/v1/sessions/{session_id}/report")
    assert rep_res.status_code == 200
    report_data = rep_res.json()

    assert report_data["session_id"] == session_id
    assert "metrics_json" in report_data
    assert "summary_markdown" in report_data
    assert "# AUTONOMOUS QA AUDIT REPORT" in report_data["summary_markdown"]

    # 3. Retrieve via GET
    get_rep_res = await async_client.get(f"/api/v1/sessions/{session_id}/report")
    assert get_rep_res.status_code == 200

    # 4. Test download endpoint
    dl_res = await async_client.get(f"/api/v1/sessions/{session_id}/report/download")
    assert dl_res.status_code == 200
    assert "text/markdown" in dl_res.headers["content-type"]
    assert "# AUTONOMOUS QA AUDIT REPORT" in dl_res.text
