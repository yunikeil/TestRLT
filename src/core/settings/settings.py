import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


current_file_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
env_path = os.path.join(root_path, ".env")

load_dotenv(dotenv_path=env_path, override=True)


class Settings(BaseSettings):
    """Класс с настройками .env файла
    """
    DEBUG: bool
    BETTER_FORMAT: bool
    RELOAD: bool
    TG_TOKEN: str
    TG_LOG_TOKEN: str
    TG_LOG_CHANNEL: int
    MONGO_URL: str
    MONGODB_DATABASE: str
    MONGODB_COLLECTION: str
    
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding='utf-8')


settings = Settings()
