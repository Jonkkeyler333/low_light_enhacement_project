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
        
class ErrorId(Exception):
    def __init__(self, log_id: str):
        self.log_id = log_id
        super().__init__(f"Log with ID {log_id} not found.")
    def __str__(self):
        return f"Log with ID {self.log_id} not found."