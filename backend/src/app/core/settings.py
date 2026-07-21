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
    max_content_length: int = Field(default = 0)
    
    model_config = SettingsConfigDict(env_file = ENV_FILE, env_file_encoding = "utf-8")
    
def get_settings() -> Settings:
    return Settings()