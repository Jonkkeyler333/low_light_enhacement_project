from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = APP_DIR / ".env"

class Settings(BaseSettings):
    app_name: str = Field(default = "")
    image_size_max: int = Field(default = 0)
    model_path: str = Field(default = "")
    allowed_extensions: list[str] = Field(default_factory = list)
    max_content_length: int = Field(default = 10 * 1024 * 1024)  # 10 MB
    mongodb_uri: str = Field(default = "")
    model_config = SettingsConfigDict(env_file = ENV_FILE, env_file_encoding = "utf-8")
    algorithm: str = Field(default = "")
    access_token_expire_minutes: int = Field(default = 0)
    secret_key: str = Field(default = "")
    
def get_settings() -> Settings:
    return Settings()