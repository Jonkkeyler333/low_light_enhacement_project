import cv2
from io import BytesIO
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.dependencies.inference import get_engine
from app.inference.engine import SciEngine
from app.services.preprocessing import load_image_bytestring, ImageValidationError, preprocess_image, posprocess_image
from typing import Any, Annotated, Union
from app.core.settings import Settings, get_settings

router = APIRouter()

@router.get('/settings/')
def info_settings(settings: Settings = Depends(get_settings)) -> dict[str, Any]:
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
            "description": "Image Enhancement in PNG type"
        },
        400: {
            "model": dict,
            "description": "Validation Error"
        }
    })

async def enhance_image(
        image: Annotated[UploadFile, File(description = 'Image to upload for model enhance')],
        engine: SciEngine = Depends(get_engine),
        settings: Settings = Depends(get_settings)
    )   -> Union[StreamingResponse, HTTPException] :
    print(image.content_type)
    print(image.filename)
    print(settings.allowed_extensions)
    if not (image.content_type in settings.allowed_extensions):
        raise HTTPException(status_code = 400, detail = 'File type do not support')
    image_bytes = await image.read()
    if len(image_bytes) > settings.max_content_length:
        raise HTTPException(status_code = 400, detail = 'File size exceeds the maximum limit')
    try:
        image_array = load_image_bytestring(image_bytes)
        img_input = preprocess_image(image_array)
        output = engine.predict(img_input)
        if output is None:
            return HTTPException(status_code = 500, detail = "Model not loaded" )
        image_array = posprocess_image(output)
        success, encoded_buffer = cv2.imencode('.png', image_array)
        if success:
            # convert the buffer to a standard python bytes object
            png_bytes = encoded_buffer.tobytes()
            print(type(png_bytes))
            # create a BytesIO object from the bytes
            png_buffer = BytesIO(png_bytes)
            png_buffer.seek(0)
            return StreamingResponse(png_buffer, media_type = "image/png")
        else:
            print("Encoding failed.")
            raise HTTPException(status_code = 400, detail = "Invalid image bytestring")
    except ImageValidationError:
        raise   HTTPException(status_code = 400, detail = "Invalid image bytestring" )