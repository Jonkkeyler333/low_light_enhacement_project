from fastapi import FastAPI
from app.inference.engine import SciEngine
from contextlib import asynccontextmanager
from app.controllers.enhance import router as enhance_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = SciEngine()
    print('model is uploading...')
    engine.load()
    app.state.engine = engine
    print('model uploaded successfully')
    yield

app = FastAPI(lifespan = lifespan)

app.include_router(enhance_router, prefix="/enhance", tags=["enhance"])

@app.get('/')
def home():
    return {"message": "hello world"}