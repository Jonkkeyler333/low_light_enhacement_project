from app.models.logs import InfereceLog, LogStatus
from beanie import PydanticObjectId

class LogRepository:
    async def create_log(self, log: InfereceLog) -> InfereceLog:
        await log.create()
        return log
    
    async def get_log_by_id(self, id: str) -> InfereceLog | None:
        log = await InfereceLog.get(id)
        return log
    
    async def get_logs(self, skip: int, limit: int, id_user: str | None, status: str | None) -> tuple[list[InfereceLog], int]:
        query_log = {}
        if id_user:
            query_log['user_id'] = PydanticObjectId(id_user)
        if status:
            query_log['status'] = status
        total_logs = await InfereceLog.find(query_log).count()
        logs = await InfereceLog.find(query_log).skip(skip).limit(limit).sort("-created_at").to_list()
        return logs, total_logs