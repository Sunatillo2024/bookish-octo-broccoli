from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Presentation-Generator"
    REDIS_URL: str = "redis://localhost:6379/0"
    RESULT_BACKEND: str = "redis://localhost:6379/0"
    STORAGE_PATH: str = "./storage"
    OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
