from pwdlib import PasswordHash
from app.core.settings import get_settings
from datetime import datetime, timedelta, timezone
import jwt

settings = get_settings()
secret_key = settings.secret_key
algorithm = settings.algorithm
password_context = PasswordHash.recommended()

class InvalidTokenError(Exception):
    def __init__(self, message: str = "Invalid token"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"{self.message}"

def get_password_hash(password):
    return password_context.hash(password)

def verify_password(password_input, hashed_password):
    return password_context.verify(password_input, hashed_password)

def create_jwt_token(payload: dict) -> str:
    to_encode = payload.copy()
    expires_time = settings.access_token_expire_minutes
    if expires_time > 0:
        expire = datetime.now(timezone.utc) + timedelta(minutes = expires_time)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = 15)
    to_encode.update({"exp": expire})
    print(f"Creating JWT token with payload: {to_encode}")
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm = algorithm)
    return encoded_jwt

def validate_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, secret_key, algorithms = [algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise InvalidTokenError("Token has expired")
    except jwt.InvalidTokenError:
        raise InvalidTokenError("Invalid token")