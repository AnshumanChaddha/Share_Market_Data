import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Share Market Data Service"
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    # Vercel standard variable is POSTGRES_HOST
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    # Vercel standard variable is POSTGRES_DATABASE
    POSTGRES_DATABASE: str = os.getenv("POSTGRES_DATABASE", "market_data")
    
    # Vercel automatically injects POSTGRES_URL or DATABASE_URL
    POSTGRES_URL: Optional[str] = os.getenv("POSTGRES_URL")
    POSTGRES_PRISMA_URL: Optional[str] = os.getenv("POSTGRES_PRISMA_URL")
    POSTGRES_URL_NON_POOLING: Optional[str] = os.getenv("POSTGRES_URL_NON_POOLING")
    
    # Allow overriding DATABASE_URL directly
    DATABASE_URL_ENV: Optional[str] = os.getenv("DATABASE_URL")
    
    @property
    def DATABASE_URL(self) -> str:
        # Direct fetch to bypass any Pydantic shadowing/default issues
        url = (
            os.environ.get("DATABASE_URL") or 
            os.environ.get("POSTGRES_URL") or 
            os.environ.get("POSTGRES_PRISMA_URL") or 
            os.environ.get("POSTGRES_URL_NON_POOLING")
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
             
        # asyncpg does not support 'sslmode' in query params, it handles SSL natively
        # Neon/Vercel URLs often include ?sslmode=require which breaks asyncpg
        if "sslmode=" in url:
            # Simple string replacement for the most common case
            url = url.replace("?sslmode=require", "").replace("&sslmode=require", "")
             
        return url

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
