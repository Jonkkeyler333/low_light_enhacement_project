import pytest
from app.main import app as light_app
from fastapi.testclient import TestClient
from beanie import init_beanie
from pymongo import AsyncMongoClient
from httpx import ASGITransport, AsyncClient
from app.core.settings import get_settings
from app.models.user import User, UserRole
from app.models.logs import InfereceLog
from app.core.auth import get_password_hash

settings = get_settings()

@pytest.fixture(scope = "module")
def client():
    with TestClient(light_app) as c:
        yield c
        
@pytest.fixture(scope = "module")
async def db_client():
    print(settings.mongodb_uri_test)
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
    
@pytest.fixture()
async def async_client(db_client):
    async with AsyncClient(
        transport = ASGITransport(app = light_app),
        base_url = "http://test"
    ) as ac:
        yield ac