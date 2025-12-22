from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, UniqueConstraint
from app.core.database import Base

class Stock(Base):
    __tablename__ = "stocks"

    symbol = Column(String, primary_key=True, index=True)
    name = Column(String)
    exchange = Column(String) # NSE or BSE
    sector = Column(String, nullable=True)

class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, autoincrement=True) # Optional surrogate key
    symbol = Column(String, ForeignKey("stocks.symbol"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    
    # Validation to ensure one entry per symbol per day
    __table_args__ = (
        UniqueConstraint('symbol', 'date', name='uix_symbol_date'),
    )
