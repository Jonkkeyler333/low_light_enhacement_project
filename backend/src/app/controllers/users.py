from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.services.users import UserService
from app.models.user import CreateUserError
from typing import Annotated
from app.schemas.users import UserResponse, UserCreateRequest

router = APIRouter(tags=["users"])
user_service = UserService()

@router.get('/', response_model = list[UserResponse], summary = "Get all users", description = "Retrieve a list of all users with optional pagination")
async def get_users(skip: Annotated[int, Query(ge = 0)] = 0,
                    limit: Annotated[int, Query(gt = 0)] = 100) -> list[UserResponse]:
    users = await user_service.get_all_user(skip=skip, limit=limit)
    return [UserResponse.model_validate(user) for user in users]

@router.post('/', response_model = UserResponse, status_code = status.HTTP_201_CREATED, summary = "Create a new user", description = "Create a new user with the provided details")
async def create_user(new_user: UserCreateRequest) -> UserResponse:
    try:
        created_user = await user_service.create_user(new_user.model_dump())
    except CreateUserError:
        raise HTTPException(status_code = 400, detail = str(CreateUserError))
    return UserResponse.model_validate(created_user)