from beanie import init_beanie
from pymongo import AsyncMongoClient
from app.core.settings import get_settings
from app.models.user import User
from app.models.logs import InfereceLog

settings = get_settings()

async def init_db() -> AsyncMongoClient:
    client = AsyncMongoClient(settings.mongodb_uri)
    await init_beanie(database = client.get_default_database(), document_models=[User, InfereceLog])
    return client