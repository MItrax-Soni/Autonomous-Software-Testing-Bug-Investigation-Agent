import pytest
from app.database import init_db

@pytest.mark.asyncio
async def test_database_initialization():
    # Verify init_db runs and creates all tables without error
    await init_db()

@pytest.mark.asyncio
async def test_project_and_session_lifecycle(async_client):
    await init_db()

    # 1. Create Project
    project_payload = {
        "name": "E-Commerce Target App",
        "target_url": "http://localhost:8088",
        "description": "Integration test project"
    }
    create_proj_res = await async_client.post("/api/v1/projects", json=project_payload)
    assert create_proj_res.status_code == 201
    project_data = create_proj_res.json()
    project_id = project_data["id"]
    assert project_data["name"] == project_payload["name"]
    assert project_data["target_url"] == project_payload["target_url"]

    # 2. Get Project
    get_proj_res = await async_client.get(f"/api/v1/projects/{project_id}")
    assert get_proj_res.status_code == 200
    assert get_proj_res.json()["id"] == project_id

    # 3. Create Session under Project
    session_payload = {
        "project_id": project_id,
        "target_url": "http://localhost:8088",
        "max_depth": 2,
        "max_pages": 10
    }
    create_sess_res = await async_client.post("/api/v1/sessions", json=session_payload)
    assert create_sess_res.status_code == 201
    session_data = create_sess_res.json()
    session_id = session_data["id"]
    assert session_data["project_id"] == project_id
    assert session_data["status"] == "DRAFT"

    # 4. List Sessions
    list_sess_res = await async_client.get(f"/api/v1/sessions?project_id={project_id}")
    assert list_sess_res.status_code == 200
    sessions_list = list_sess_res.json()
    assert len(sessions_list) >= 1
    assert any(s["id"] == session_id for s in sessions_list)

    # 5. Delete Project (Cascades to Session)
    del_proj_res = await async_client.delete(f"/api/v1/projects/{project_id}")
    assert del_proj_res.status_code == 204

    # 6. Verify Session was cascade-deleted
    get_sess_deleted = await async_client.get(f"/api/v1/sessions/{session_id}")
    assert get_sess_deleted.status_code == 404
