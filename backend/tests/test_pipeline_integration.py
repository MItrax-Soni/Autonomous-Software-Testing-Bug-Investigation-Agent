import pytest
from app.database import init_db
from app.database import AsyncSessionLocal
from app.models.session import TestSession
from sqlalchemy import select

@pytest.mark.asyncio
async def test_session_stream_endpoint(async_client):
    await init_db()

    # 1. Create a session marked COMPLETED so stream terminates immediately
    async with AsyncSessionLocal() as db:
        session = TestSession(
            target_url="http://localhost:8088",
            max_depth=1,
            max_pages=1,
            status="COMPLETED"
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
        session_id = session.id

    # 2. Query SSE stream endpoint
    stream_res = await async_client.get(f"/api/v1/sessions/{session_id}/stream")
    assert stream_res.status_code == 200
    assert "text/event-stream" in stream_res.headers["content-type"]
    assert "COMPLETED" in stream_res.text

@pytest.mark.asyncio
async def test_orchestrate_rejects_ssrf_and_handles_failure(async_client):
    await init_db()

    # 1. Create session with private IP
    sess_res = await async_client.post("/api/v1/sessions", json={
        "target_url": "http://10.254.1.1",
        "max_depth": 1,
        "max_pages": 1
    })
    session_id = sess_res.json()["id"]

    # 2. Trigger pipeline -> must fail gracefully with HTTP 500 containing SSRF error message
    orch_res = await async_client.post(f"/api/v1/sessions/{session_id}/orchestrate")
    assert orch_res.status_code == 500
    assert "SSRF" in orch_res.json()["detail"]

    # 3. Verify session status in DB is marked FAILED
    get_res = await async_client.get(f"/api/v1/sessions/{session_id}")
    assert get_res.json()["status"] == "FAILED"
    assert "SSRF" in get_res.json()["error_summary"]
