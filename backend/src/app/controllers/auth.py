from fastapi import APIRouter, Depends, HTTPException, Response, Depends, status
from app.schemas.users import UserCreateRequest, UserCreateResponse, UserLoginRequest, UserLoginResponse, UserResponse
from app.services.users import UserService, CreateUserError, InvalidCredentialsError
from fastapi.security import OAuth2PasswordBearer
from app.dependencies.user import get_current_user

router = APIRouter(tags=["auth"])
user_service = UserService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.post('/register', response_model = UserCreateResponse, summary = "Register a new user", status_code = status.HTTP_201_CREATED, description = "New user registration endpoint. Returns the created user's ID and email.")
async def register_user(new_user: UserCreateRequest) -> UserCreateResponse:
    try:
        created_user = await user_service.create_user(new_user.model_dump())
    except CreateUserError:
            raise HTTPException(status_code = 400, detail = str(CreateUserError))
    return UserCreateResponse.model_validate(created_user)

@router.post('/login', response_model = UserLoginResponse, status_code = status.HTTP_200_OK, summary = "Login a user", description = "Authenticate a user and return a JWT token.")
async def login_user(login_data: UserLoginRequest, response: Response) -> UserLoginResponse:
    try:
        response_dict = await user_service.login_user(login_data.email, login_data.plain_password)
        response.set_cookie(
            key = "access_token",
            value = response_dict['token'],
            httponly = True,
            secure = False,  # set to True in production with HTTPS
            samesite = "lax",
            max_age = 3600, 
            path = "/"
        )
    except InvalidCredentialsError:
        raise HTTPException(status_code = 401, detail = "Invalid credentials")
    return UserLoginResponse(message = response_dict["message"])

@router.post('/logout', summary = "Logout a user", status_code = status.HTTP_204_NO_CONTENT, description = "Logout the currently authenticated user by clearing the JWT token cookie.")
async def logout_user(response: Response):
    response.delete_cookie(key = "access_token", path = "/")

@router.post('/me', response_model = UserResponse, summary = "Get current user", status_code = status.HTTP_200_OK, description = "Retrieve the currently authenticated user's information.")
async def get_me(current_user = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)