import pytest
from pathlib import Path
from app.main import app as light_app
from fastapi.testclient import TestClient
from beanie import init_beanie
from pymongo import AsyncMongoClient
from httpx import ASGITransport, AsyncClient
from app.core.settings import get_settings
from app.models.user import User, UserRole
from app.models.logs import InfereceLog
from app.core.auth import get_password_hash
from asgi_lifespan import LifespanManager

settings = get_settings()
image_path = Path(__file__).parent / "fixtures" / "79.png"

@pytest.fixture(scope = "module")
def client():
    with TestClient(light_app) as c:
        yield c
        
@pytest.fixture(scope = "module")
async def db_client():
    client = AsyncMongoClient(settings.mongodb_uri_test)
    await init_beanie(database = client.get_default_database(), document_models=[User, InfereceLog])
    yield client
    await User.delete_all()
    await InfereceLog.delete_all()
    await client.close()
    
@pytest.fixture(scope = "module")
async def admin_user(db_client):
    user = User(
        name = "admin_test",
        last_name = "test",
        email = "test@example.com", 
        role = UserRole.ADMIN,
        hash_password = get_password_hash("test_password")
    )
    await user.insert()
    yield user
    
@pytest.fixture(scope = "module")
async def normal_user(db_client):
    user = User(
        name = "normal_test",
        last_name = "test",
        email = "hola@gmail.com",
        role = UserRole.USER,
        hash_password = get_password_hash("test_password_xd")
    )
    await user.insert()    
    yield user

@pytest.fixture()
async def async_client(db_client):
    async with LifespanManager(light_app):
        async with AsyncClient(
            transport = ASGITransport(app = light_app),
            base_url = "http://test"
        ) as ac:
            yield ac
        
@pytest.fixture()
def valid_image_bytes():
    return image_path.read_bytes()

@pytest.fixture()
def invalid_file():
    return b"%PDF-1.4 HAHAHA I bother u babe"

@pytest.fixture()
async def authenticated_client(async_client, normal_user):
    response = await async_client.post('/api/auth/login', json = {
        "email": "hola@gmail.com",
        "plain_password": "test_password_xd"
    })
    
    assert response.status_code == 200
    yield async_client
    await async_client.post('/api/auth/logout')