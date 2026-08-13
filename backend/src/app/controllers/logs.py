from asyncio import log

from fastapi import APIRouter, HTTPException, Query, status, Path, Depends
from app.schemas.logs import LogCreateRequest, LogResponse, LogResponseWithCount
from app.services.logs import LogService
from typing import Annotated
from app.dependencies.user import get_current_user, valid_admin

router = APIRouter()
log_service = LogService()

@router.get('/', response_model = list[LogResponse], status_code = status.HTTP_200_OK)
async def get_logs(skip: Annotated[int, Query(ge = 0)] = 0,
                   limit: Annotated[int, Query(ge = 1)] = 10,
                   user_id: Annotated[str | None, Query()] = None,
                   status: Annotated[str | None, Query()] = None, 
                   admin : Annotated[None, Depends(valid_admin)] = None):
    logs = await log_service.get_logs(
        skip = skip,
        limit = limit,
        id_user = user_id,
        status = status
    )
    return logs

@router.get('/me', response_model = LogResponseWithCount, status_code = status.HTTP_200_OK)
async def get_me_logs(skip: Annotated[int, Query(ge = 0)] = 0,
                   limit: Annotated[int, Query(ge = 1)] = 10,
                   user = Depends(get_current_user)):
    try:
        logs, total_user_logs = await log_service.get_logs(
            skip = skip,
            limit = limit,
            id_user = str(user.id),
        )
        logs_response = [LogResponse.model_validate(log) for log in logs]
        return LogResponseWithCount(logs = logs_response, count = total_user_logs)
    except ValueError:
        raise HTTPException(status_code = 404, detail = "Bad User Id")

@router.get('/{log_id}', response_model = LogResponse , status_code = status.HTTP_200_OK)
async def get_log_by_id(log_id : Annotated[str, Path()],
                        admin : Annotated[None, Depends(valid_admin)] = None):
    try:
        log = await log_service.get_log_by_id(log_id)
        return log
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))