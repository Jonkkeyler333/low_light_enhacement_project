import cv2
from io import BytesIO
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
from app.dependencies.inference import get_engine
from app.inference.engine import SciEngine
from app.services.preprocessing import load_image_bytestring, ImageValidationError
from typing import Any, Annotated, Union
from app.core.settings import Settings, get_settings

router = APIRouter()

@router.get('/settings/')
def settings(settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    return {
        "image_size_max": settings.image_size_max,
        "allowed_extensions": settings.allowed_extensions,
        "max_content_length": settings.max_content_length
    }
    
@router.get('/check/')
def check_model(engine: SciEngine = Depends(get_engine)) -> dict[str, Any]:
    trainable = sum(
            p.numel()
            for p in engine.model.parameters() # type: ignore
            if p.requires_grad
    )
    
    return {
        "model_loaded": engine is not None,
        "trainable_parameters": trainable,
        "eval_mode": not(bool(engine.model.training)) # type: ignore
    }

@router.post('/', response_model = None, responses = {
        200: {
            "content": {"image/png": {}},
            "description": "Imagen mejorada en PNG"
        },
        400: {
            "model": dict,
            "description": "Error de validación"
        }
    })
async def enhance_image(image: Annotated[UploadFile, File(description = 'Image to upload for model enhance')]) -> Union[StreamingResponse, JSONResponse] :
    image_bytes = await image.read()
    try:
        image_array = load_image_bytestring(image_bytes)
        success, encoded_buffer = cv2.imencode('.png', image_array)
        if success:
            # 3. Convert the buffer to a standard Python bytes object
            png_bytes = encoded_buffer.tobytes()
            print(type(png_bytes))
            # 4. Create a BytesIO object from the bytes
            png_buffer = BytesIO(png_bytes)
            png_buffer.seek(0)
            return StreamingResponse(png_buffer, media_type = "image/png")
        else:
            print("Encoding failed.")
            return JSONResponse(
                        status_code = 400,
                        content = {"error": "Invalid image bytestring"}
            )
    except ImageValidationError:
        return JSONResponse(
            status_code = 400,
            content = {"error": "Invalid image bytestring"}
        )
    
    