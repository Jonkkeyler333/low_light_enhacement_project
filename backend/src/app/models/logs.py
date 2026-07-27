from beanie import Document, PydanticObjectId
from pydantic import Field
from datetime import datetime , timezone
from enum import Enum

class LogStatus(str, Enum):
    PENDING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class InfereceLog(Document):
    user_id: PydanticObjectId
    model_name: str
    input_filename: str
    output_filename: str | None = None
    processing_time : float
    status: str = Field(default = LogStatus.COMPLETED.value)
    error_detail : str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "inference_logs"
        indexes = [
           "user_id"
        ]