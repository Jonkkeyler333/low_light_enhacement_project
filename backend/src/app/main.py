from fastapi import FastAPI, status
from app.inference.engine import SciEngine
from contextlib import asynccontextmanager
from app.controllers.enhance import router as enhance_router
from app.controllers.users import router as users_router
from app.controllers.auth import router as auth_router
from app.controllers.logs import router as logs_router
from app.dependencies.database import init_db
from app.core.settings import get_settings
from fastapi.middleware.cors import CORSMiddleware

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.environment == "development":
        engine = SciEngine()    
        print('model is uploading...')
        engine.load()
        app.state.engine = engine
        print('model uploaded successfully')
        client_mongo = await init_db()
        yield
        await client_mongo.close()
    elif settings.environment == "test":
        print('test environment detected')
        engine = SciEngine()    
        print('model is uploading...')
        engine.load()
        app.state.engine = engine
        yield

app = FastAPI(lifespan = lifespan, title = "Low Light Enhancement API", description = "API for low light enhancement using deep learning models", version = "0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
app.include_router(enhance_router, prefix="/api/enhance", tags=["enhance"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(logs_router, prefix="/api/logs", tags=["logs"])

@app.get('/health', status_code = status.HTTP_200_OK)
def home():
    return {"status": "ok", "message": "API is running successfully"}