import pytest
from app.main import app as light_app
from fastapi.testclient import TestClient

@pytest.fixture(scope="module")
def client():
    with TestClient(light_app) as c:
        yield c