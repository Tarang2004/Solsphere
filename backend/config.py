import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./solsphere.db"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # API
    api_prefix: str = "/api"
    
    # System checks
    check_interval_minutes: int = 30
    max_check_history: int = 100
    
    class Config:
        env_file = ".env"

settings = Settings()
