from app.main import app as light_app
from fastapi.testclient import TestClient

client = TestClient(light_app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello world"}
