import numpy as np 
import cv2
from datetime import datetime, timezone

class ImageValidationError(Exception):
    def __init__(self, message: str):
        self.message = message
        self.timestamp = datetime.now(timezone.utc)
        super().__init__(self.message)

def load_image_bytestring(image_bytes: bytes) -> np.ndarray:
    try:
        img_np_flat = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(img_np_flat, cv2.IMREAD_COLOR)
        if img is None:
            raise ImageValidationError("Invalid image bytestring")
        return img
    except (ValueError, AttributeError):
        raise ImageValidationError("Invalid image bytestring")
    
    
#     from io import BytesIO
# from fastapi import APIRouter, Depends, UploadFile, File
# from fastapi.responses import StreamingResponse

# router = APIRouter()

# # Inyección de dependencia para obtener el engine cargado en app.state
# def get_engine(request: Request) -> SciEngine:
#     return request.app.state.engine

# @router.post("/process-image")
# async def process_image_endpoint(
#     file: UploadFile = File(...),
#     engine: SciEngine = Depends(get_engine)
# ):
#     # 1. Leer los bytes entrantes de la petición
#     image_bytes = await file.read()
    
#     # 2. Cargar y validar la imagen con tu función
#     # (Si los bytes son inválidos, se dispara tu excepción personalizada)
#     img_np = load_image_bytestring(image_bytes)
    
#     # 3. Aplicar preprocesamiento en el engine y obtener bytes resultantes
#     processed_bytes = engine.process_image(img_np)
    
#     # 4. Envolver en BytesIO para transmitir la respuesta en streaming
#     return StreamingResponse(
#         BytesIO(processed_bytes), 
#         media_type="image/jpeg"
    # )