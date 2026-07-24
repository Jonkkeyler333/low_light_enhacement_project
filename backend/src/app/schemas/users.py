from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId

class UserResponse(BaseModel):
    id: PydanticObjectId = Field(alias = "_id")
    name: str
    last_name: str
    email: EmailStr
    is_active: bool
    role: str
    last_login: str | None = None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
    
class UserCreateRequest(BaseModel):
    name: str = Field(min_length = 1, max_length = 50)
    last_name: str = Field(min_length = 1, max_length = 50)
    email: EmailStr
    plain_password: str = Field(min_length = 1)

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }

class UserCreateResponse(BaseModel):
    id: PydanticObjectId = Field(alias = "_id")
    email: EmailStr

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
    
class UserLoginRequest(BaseModel):
    email: EmailStr
    plain_password: str = Field(min_length = 1)
    
class UserLoginResponse(BaseModel):
    message: str

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }