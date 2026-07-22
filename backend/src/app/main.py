from fastapi import FastAPI, Depends
from app.core.settings import Settings, get_settings
from app.inference.engine import SciEngine
from contextlib import asynccontextmanager
from app.controllers.enhance import router as enhance_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = SciEngine()
    print('Iniciando modelo :)')
    engine.load()
    app.state.engine = engine
    yield

app = FastAPI(lifespan = lifespan)

app.include_router(enhance_router, prefix="/enhance", tags=["enhance"])

@app.get('/')
def home():
    return {"message": "hello world"}

@app.get('/check')
def check_model(engine: SciEngine = Depends(lambda: app.state.engine)):
    trainable = sum(
        p.numel()
        for p in engine.model.parameters() # type: ignore
        if p.requires_grad
    )
    return {"trainable_parameters": trainable}