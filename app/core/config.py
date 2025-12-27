from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Share Market Data Service"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    # Vercel standard variable is POSTGRES_HOST
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    # Vercel standard variable is POSTGRES_DATABASE
    POSTGRES_DATABASE: str = "market_data"
    
    # Vercel automatically injects POSTGRES_URL or DATABASE_URL
    POSTGRES_URL: Optional[str] = None
    POSTGRES_PRISMA_URL: Optional[str] = None
    POSTGRES_URL_NON_POOLING: Optional[str] = None
    
    # Allow overriding DATABASE_URL directly
    DATABASE_URL_ENV: Optional[str] = None 
    
    @property
    def DATABASE_URL(self) -> str:
        # Prioritize Vercel/System Env Vars
        url = (
            self.DATABASE_URL_ENV or 
            self.POSTGRES_URL or 
            self.POSTGRES_PRISMA_URL or 
            self.POSTGRES_URL_NON_POOLING
        )
        
        if not url:
            # Fallback to constructing from components
            print("WARNING: No Vercel/Env DB URL found. Defaulting to constructed URL (likely localhost).")
            url = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"
        else:
             print("INFO: Found Database URL from environment variables.")
            
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
