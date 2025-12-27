from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.market_data import Stock, MarketData
from typing import List, Optional
from pydantic import BaseModel
from datetime import date

router = APIRouter()

class StockResponse(BaseModel):
    symbol: str
    name: Optional[str]
    exchange: Optional[str]

    class Config:
        from_attributes = True

class MarketDataResponse(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int

    class Config:
        from_attributes = True

@router.get("/stocks", response_model=List[StockResponse])
async def get_stocks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Stock))
    return result.scalars().all()

@router.get("/stocks/{symbol}/history", response_model=List[MarketDataResponse])
async def get_stock_history(symbol: str, db: AsyncSession = Depends(get_db)):
    # Check if stock exists
    result = await db.execute(select(Stock).where(Stock.symbol == symbol))
    stock = result.scalars().first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    # Fetch history
    # Optimally, we should add date range filters here
    result = await db.execute(select(MarketData).where(MarketData.symbol == symbol).order_by(MarketData.date.desc()))
    return result.scalars().all()

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    from app.core.config import settings
    # Mask password for security
    db_url = settings.DATABASE_URL
    safe_url = db_url.split("@")[-1] if "@" in db_url else "localhost"
    
    try:
        from sqlalchemy import text
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected", "connection_target": safe_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed. Target: {safe_url}. Error: {str(e)}")

@router.get("/debug-env")
async def debug_env():
    import os
    # Return ONLY keys for security to confirm what variables exist
    return {
        "env_keys": sorted(list(os.environ.keys())),
        "postgres_vars_present": [k for k in os.environ.keys() if "POSTGRES" in k or "DATABASE" in k]
    }
