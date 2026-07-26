from app.repositories.users import UserRepository
from app.models.user import User, CreateUserError, InvalidCredentialsError
from pymongo.errors import DuplicateKeyError
from pydantic import ValidationError
from datetime import datetime , timezone
from app.core.auth import get_password_hash, verify_password, create_jwt_token

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        
    async def create_user(self, user_data: dict) -> User:
        try:
            plain_password = user_data.pop("plain_password")
            hashed_password = get_password_hash(plain_password)
            user_data["hash_password"] = hashed_password
            user = User(**user_data)
            print(f"Creating user: {user}")
            new_user = await self.user_repository.create_user(user)
            return new_user
        except (DuplicateKeyError, ValidationError) as e:
            raise CreateUserError(f"Error creating user: {str(e)}")
    
    async def get_all_user(self, skip: int = 0, limit: int = 100) -> list[User]:
        users = await self.user_repository.get_users(skip = skip, limit = limit)
        return users
    
    async def get_user_by_email(self, email: str) -> User | None:
        user = await self.user_repository.get_user_by_email(email)
        return user
    
    async def login_user(self, email:str, plain_password:str) -> dict:
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise InvalidCredentialsError()
        if not verify_password(plain_password, user.hash_password):
            raise InvalidCredentialsError()
        last_login = datetime.now(timezone.utc).isoformat()
        update_user = await self.user_repository.update_user(str(user.id), {"last_login": last_login})
        if not update_user:
            raise InvalidCredentialsError("Failed to update last login time.")
        payload = {"email": str(update_user.email), "id": str(update_user.id)}
        jwt_token = create_jwt_token(payload)
        return {
            "user": user,
            "message": "Login successful",
            "token": jwt_token
        }