from fastapi import APIRouter, HTTPException, Query, status, Path, Depends
from fastapi.responses import JSONResponse
from app.services.users import UserService
from app.models.user import CreateUserError
from typing import Annotated
from app.schemas.users import UserResponse, UserCreateRequest
from app.dependencies.user import valid_admin

router = APIRouter(tags=["users"])
user_service = UserService()

@router.get('/', response_model = list[UserResponse], summary = "Get all users", description = "Retrieve a list of all users with optional pagination")
async def get_users(skip: Annotated[int, Query(ge = 0)] = 0,
                    limit: Annotated[int, Query(gt = 0)] = 100,
                    is_admin = Depends(valid_admin)) -> list[UserResponse]:
    users = await user_service.get_all_user(skip=skip, limit=limit)
    return [UserResponse.model_validate(user) for user in users]

@router.post('/', response_model = UserResponse, status_code = status.HTTP_201_CREATED, summary = "Create a new user", description = "Create a new user with the provided details")
async def create_user(new_user: UserCreateRequest, is_admin = Depends(valid_admin)) -> UserResponse:
    try:
        created_user = await user_service.create_user(new_user.model_dump())
    except CreateUserError:
        raise HTTPException(status_code = 400, detail = str(CreateUserError))
    return UserResponse.model_validate(created_user)

@router.get('/{user_id}', response_model = UserResponse, status_code = status.HTTP_200_OK, summary = "Get user by ID", description = "Retrieve a user by their unique ID")
async def get_user_by_id(user_id : Annotated[str, Path()], is_admin = Depends(valid_admin)) -> UserResponse:
    user = user_service.get_user_id(str(user_id))
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    return UserResponse.model_validate(user)

@router.delete('/{user_id}', status_code = status.HTTP_200_OK, summary = "Delete user by ID", description = "Delete a user by their unique ID")
async def delete_user_by_id(user_id : Annotated[str, Path()], is_admin = Depends(valid_admin)) -> JSONResponse:
    user = await user_service.get_user_id(str(user_id))
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    deleted_user = await user_service.user_repository.delete_user(str(user_id))
    if not deleted_user:
        raise HTTPException(status_code = 500, detail = "Failed to delete user")
    return JSONResponse(status_code = status.HTTP_200_OK, content = {"message": "User deleted successfully"})