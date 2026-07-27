from fastapi import APIRouter
from app.schemas.logs import LogCreateRequest, LogGetRequest
from app.services.logs import LogService

router = APIRouter()
log_service = LogService()

@router.get('/logs/', response_model = list[LogCreateRequest])
async def get_logs(log_get_request: LogGetRequest):
    logs = await log_service.get_logs(
        skip = log_get_request.skip,
        limit = log_get_request.limit,
        id_user = str(log_get_request.user_id) if log_get_request.user_id else None,
        status = log_get_request.status
    )
    return logs