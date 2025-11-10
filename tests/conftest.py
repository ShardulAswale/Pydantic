import pytest
from fastapi.testclient import TestClient
from car_api.main import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture()
def auth_header():
    # Basic auth header for admin:changeme
    import base64
    token = base64.b64encode(b"admin:changeme").decode()
    return {"Authorization": f"Basic {token}"}
