from app.repositories.log import LogRepository
from app.models.logs import InfereceLog, ErrorId
from app.repositories.users import UserRepository
from pydantic import ValidationError

class LogService:
    def __init__(self):
        self.log_repository = LogRepository()
        
    async def create_log(self, log_data: dict) -> InfereceLog:
        log = InfereceLog(**log_data)
        created_log = await self.log_repository.create_log(log)
        return created_log
    
    async def get_logs(self, skip: int, limit: int, id_user: str | None = None, status: str | None = None) -> tuple[list[InfereceLog], int]:
        if id_user is not None:
            user_repo = UserRepository()
            user = await user_repo.get_user_by_id(id_user)
            if user is None:
                raise ValueError(f"User with id {id_user} does not exist.")
        logs, total_user_blogs = await self.log_repository.get_logs(skip, limit, id_user, status)
        return logs, total_user_blogs
    
    async def get_log_by_id(self, log_id: str) -> InfereceLog:
        try:
            log = await self.log_repository.get_log_by_id(log_id)
            if log is None:
                raise ErrorId(log_id)
            return log
        except ValidationError:
            raise ErrorId(log_id)