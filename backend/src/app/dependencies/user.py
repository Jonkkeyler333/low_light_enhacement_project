from fastapi import Request, HTTPException
from app.core.auth import validate_jwt_token, InvalidTokenError
from app.services.users import UserService
from app.models.user import InvalidCredentialsError

def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token not found in cookies")
    return token

async def get_current_user(request: Request):
    token = get_token(request)
    try:
        payload = validate_jwt_token(token)
        user_service = UserService()
        user = await user_service.get_user_by_email(payload["email"])
        if not user:
            raise InvalidCredentialsError()
        return user
    except InvalidTokenError as e:
        raise HTTPException(status_code = 401, detail = f"Invalid token: {str(e)}")