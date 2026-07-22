import numpy as np 
import cv2
from datetime import datetime, timezone
from app.core.settings import Settings, get_settings
import torch

SETTINGS = get_settings()

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
    
def preprocess_image(image: np.ndarray) -> torch.Tensor:
    max_size = SETTINGS.image_size_max
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width = image_rgb.shape[:2]
    if max(height, width) > max_size:
        scaling_factor = max_size / max(height, width)
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        image = cv2.resize(image_rgb, (new_width, new_height), interpolation=cv2.INTER_AREA)
    tensor = torch.from_numpy(image).permute(2, 0, 1).float() / 255.0
    tensor_batch = tensor.unsqueeze(0)
    return tensor_batch

def posprocess_image(tensor: torch.Tensor) -> np.ndarray:
    out_array = tensor.squeeze(0).detach().cpu().clamp(0,1).permute(1, 2, 0).numpy()*255
    out_img = out_array.astype('uint8')
    return out_img