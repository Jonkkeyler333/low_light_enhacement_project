from fastapi import APIRouter, Depends, HTTPException, Response, Request
from app.core.auth import InvalidTokenError, get_password_hash, validate_jwt_token, verify_password
from app.schemas.users import UserCreateRequest, UserCreateResponse, UserLoginRequest, UserLoginRequest, UserLoginResponse, UserLoginResponse
from app.services.users import UserService, CreateUserError, InvalidCredentialsError
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(tags=["auth"])
user_service = UserService()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.post('/register', response_model = UserCreateResponse, summary = "Register a new user", description = "New user registration endpoint. Returns the created user's ID and email.")
async def register_user(new_user: UserCreateRequest) -> UserCreateResponse:
    try:
        created_user = await user_service.create_user(new_user.model_dump())
    except CreateUserError:
            raise HTTPException(status_code = 400, detail = str(CreateUserError))
    return UserCreateResponse.model_validate(created_user)

@router.post('/login', response_model = UserLoginResponse, summary = "Login a user", description = "Authenticate a user and return a JWT token.")
async def login_user(login_data: UserLoginRequest, response: Response) -> UserLoginResponse:
    try:
        response_dict = await user_service.login_user(login_data.email, login_data.plain_password)
        response.set_cookie(
            key="access_token",
            value=response_dict['token'],
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=3600,  # Set the cookie to expire in 1 hou
            path="/"
        )
    except InvalidCredentialsError:
        raise HTTPException(status_code = 401, detail = "Invalid credentials")
    return UserLoginResponse(message = response_dict["message"])

@router.post('/test', summary = "probar la logica de descifrado del token", description = "probar la logica de descifrado del token.")
async def test_token(request: Request):
    try:
        token = request.cookies.get("access_token")
        print(request.cookies)
        payload = validate_jwt_token(token)
        return {"message": "Token is valid", "payload": payload}
    except InvalidTokenError as e:
        raise HTTPException(status_code = 401, detail = f"Invalid token: {str(e)}")