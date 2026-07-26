from fastapi import Request, HTTPException, Depends
from app.core.auth import validate_jwt_token, InvalidTokenError
from app.services.users import UserService
from app.models.user import InvalidCredentialsError, User

def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException( status_code = 401, detail=  "Unauthorized")
    return token

async def get_current_user(request: Request) -> User:
    token = get_token(request)
    try:
        payload = validate_jwt_token(token)
        user_service = UserService()
        user = await user_service.get_user_by_email(payload["email"])
        if not user:
            raise InvalidCredentialsError( message = "Invalid credentials")
        return user
    except InvalidTokenError as e:
        raise HTTPException(status_code = 401, detail = f"Unauthorized")
    
async def valid_admin(user : User | None = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code = 401, detail = "Unauthorized")
    if not user.role == "admin":
        raise HTTPException(status_code = 403, detail = "Forbidden: Admin access required")