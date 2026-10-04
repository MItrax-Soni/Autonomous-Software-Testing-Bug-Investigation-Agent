import pytest
from app.services.ssrf_validator import SSRFValidator, SSRFSecurityError
from app.database import init_db

def test_ssrf_prohibited_ips():
    # Loopback
    with pytest.raises(SSRFSecurityError):
        SSRFValidator.validate_url("http://127.0.0.1:9090")

    # Private 10.x
    with pytest.raises(SSRFSecurityError):
        SSRFValidator.validate_url("http://10.10.10.10")

    # Private 192.168.x
    with pytest.raises(SSRFSecurityError):
        SSRFValidator.validate_url("http://192.168.1.100")

    # AWS / Cloud Metadata IP
    with pytest.raises(SSRFSecurityError):
        SSRFValidator.validate_url("http://169.254.169.254/latest/meta-data")

def test_ssrf_prohibited_schemes():
    with pytest.raises(SSRFSecurityError):
        SSRFValidator.validate_url("file:///etc/passwd")

    with pytest.raises(SSRFSecurityError):
        SSRFValidator.validate_url("ftp://example.com")

def test_ssrf_controlled_app_exemption():
    # Permitted controlled local app on port 8088
    is_valid, msg = SSRFValidator.validate_url("http://localhost:8088")
    assert is_valid is True
    assert "controlled" in msg.lower()

    is_valid_ip, msg_ip = SSRFValidator.validate_url("http://127.0.0.1:8088")
    assert is_valid_ip is True

@pytest.mark.asyncio
async def test_scan_api_rejects_ssrf(async_client):
    await init_db()

    # 1. Create a session with a malicious private IP target
    sess_res = await async_client.post("/api/v1/sessions", json={
        "target_url": "http://192.168.1.1",
        "max_depth": 1,
        "max_pages": 1
    })
    assert sess_res.status_code == 201
    session_id = sess_res.json()["id"]

    # 2. Trigger scan
    scan_res = await async_client.post(f"/api/v1/sessions/{session_id}/scan")
    assert scan_res.status_code == 400
    assert "SSRF Protection" in scan_res.json()["detail"]
