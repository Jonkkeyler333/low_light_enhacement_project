from fastapi import FastAPI, Depends
from app.core.settings import Settings, get_settings
from app.inference.engine import SciEngine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = SciEngine()
    print('Iniciando modelo :)')
    engine.load()
    app.state.engine = engine
    yield

app = FastAPI(lifespan = lifespan)

@app.get('/')
def home():
    return {"message": "hello world"}

@app.get('/check')
def check_model(engine: SciEngine = Depends(lambda: app.state.engine)):
    trainable = sum(
        p.numel()
        for p in engine.model.parameters()
        if p.requires_grad
    )
    return {"trainable_parameters": trainable}

@app.get('/settings')
def settings(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "image_size_max": settings.image_size_max
    }