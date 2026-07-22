from fastapi import Request
from app.inference.engine import SciEngine

def get_engine(request: Request) -> SciEngine:
    return request.app.state.engine