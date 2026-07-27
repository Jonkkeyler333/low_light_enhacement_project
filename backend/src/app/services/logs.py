from app.repositories.log import LogRepository
from app.models.logs import InfereceLog

class LogService:
    def __init__(self):
        self.log_repository = LogRepository()
        
    async def create_log(self, log_data: dict) -> InfereceLog:
        log = InfereceLog(**log_data)
        created_log = await self.log_repository.create_log(log)
        return created_log
    
    async def get_logs(self, skip: int, limit: int, id_user: str | None = None, status: str | None = None) -> list[InfereceLog]:
        logs = await self.log_repository.get_logs(skip, limit, id_user, status)
        return logs