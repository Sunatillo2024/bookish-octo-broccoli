from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Presentation-Generator"
    REDIS_URL: str = "redis://localhost:6379/0"
    RESULT_BACKEND: str = "redis://localhost:6379/0"
    STORAGE_PATH: str = "./storage"
    OPENAI_API_KEY: str = ""

    SECRET_KEY: str = "your-secret-key-change-this-in-production-09876543210"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API Key sozlamalari (oddiy variant)
    API_KEYS: list = [
        "demo-api-key-12345",  # Demo key
        "client-api-key-67890"  # Client key
    ]
    class Config:
        env_file = ".env"

settings = Settings()
