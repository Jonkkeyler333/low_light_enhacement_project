from datetime import datetime
from app.models.logs import LogStatus
from beanie import PydanticObjectId
from pydantic import BaseModel, Field, ConfigDict

class LogCreateRequest(BaseModel):
    user_id: PydanticObjectId
    model_name: str
    input_filename: str
    output_filename: str | None = None
    processing_time : float
    status: str = Field(default = LogStatus.COMPLETED.value)
    error_detail : str | None = None
    
class LogResponse(LogCreateRequest):
    id: PydanticObjectId
    created_at: datetime
    model_config = ConfigDict(from_attributes = True)
    
class LogResponseWithCount(BaseModel):
    logs: list[LogResponse]
    count: int
    
class LogGetRequest(BaseModel):
    skip: int = Field(default = 0, ge = 0)
    limit: int = Field(default = 10, ge = 1)
    user_id: PydanticObjectId | None = None
    status: str | None = None