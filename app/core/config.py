from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Share Market Data Service"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "market_data"
    
    # Vercel automatically injects POSTGRES_URL or DATABASE_URL
    POSTGRES_URL: Optional[str] = None
    # Allow overriding DATABASE_URL directly
    DATABASE_URL_ENV: Optional[str] = None 
    
    @property
    def DATABASE_URL(self) -> str:
        # Check for direct URL (Vercel or manual)
        url = self.DATABASE_URL_ENV or self.POSTGRES_URL
        
        if not url:
            # Fallback to constructing from components
            url = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            
        # Ensure asyncpg driver is used
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://") and "asyncpg" not in url:
             url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
             
        return url

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
