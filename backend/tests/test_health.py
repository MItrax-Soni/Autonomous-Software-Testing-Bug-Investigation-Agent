import pytest

@pytest.mark.asyncio
async def test_root_endpoint(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Autonomous Software Testing & Bug Investigation Agent"
    assert data["status"] == "online"

@pytest.mark.asyncio
async def test_health_check_endpoint(async_client):
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["database_configured"] is True
    assert data["ssrf_protection"] is True
