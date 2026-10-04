import pytest
from httpx import AsyncClient, ASGITransport
from controlled_test_app.app import app as controlled_app
from app.database import init_db
from app.services.ssrf_validator import SSRFValidator

@pytest.fixture
def controlled_client():
    transport = ASGITransport(app=controlled_app)
    return AsyncClient(transport=transport, base_url="http://localhost:8088")

@pytest.mark.asyncio
async def test_controlled_app_all_defect_surfaces(controlled_client):
    # 1. Landing route
    r_home = await controlled_client.get("/")
    assert r_home.status_code == 200
    assert "Autonomous QA Target Sandbox" in r_home.text

    # 2. Login route (Happy Path)
    r_login = await controlled_client.get("/login")
    assert r_login.status_code == 200
    assert "btn-login" in r_login.text

    # 3. Checkout Intentional 500 Bug
    r_coupon_fail = await controlled_client.post("/api/checkout/apply-coupon", json={"coupon": ""})
    assert r_coupon_fail.status_code == 500
    assert "Internal Server Error" in r_coupon_fail.json()["detail"]

    # 4. Modal Disappearance route
    r_modal = await controlled_client.get("/modal")
    assert r_modal.status_code == 200
    assert "btn-open-modal" in r_modal.text

    # 5. Dedicated 500 endpoint
    r_buggy = await controlled_client.get("/api/buggy-data")
    assert r_buggy.status_code == 500

    # 6. JavaScript Crash trigger route
    r_crash = await controlled_client.get("/crash")
    assert r_crash.status_code == 200
    assert "btn-trigger-crash" in r_crash.text

def test_ssrf_explicit_permission_for_controlled_app():
    # Permitted controlled app
    is_valid, msg = SSRFValidator.validate_url("http://localhost:8088")
    assert is_valid is True

    # But unauthorized loopback port must be blocked
    with pytest.raises(Exception):
        SSRFValidator.validate_url("http://localhost:9099")
