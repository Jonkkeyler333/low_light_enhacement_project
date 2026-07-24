from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import datetime , timezone

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(Document):
    name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: Indexed(EmailStr, unique=True) # type: ignore
    hash_password: str
    is_active: bool = True
    role: UserRole = Field(default=UserRole.USER)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_login: str | None = None

    class Settings:
        name = "users"
        
class CreateUserError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f"CreateUserError: {self.message}"
    
class InvalidCredentialsError(Exception):
    def __init__(self, message: str = "Invalid credentials"):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return self.message
    