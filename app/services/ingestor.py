import yfinance as yf
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert
from app.core.database import AsyncSessionLocal
from app.models.market_data import Stock, MarketData
from datetime import date, datetime
import pandas as pd
import logging

logger = logging.getLogger(__name__)

async def fetch_and_store_data(symbol: str):
    logger.info(f"Fetching data for {symbol}")
    # yfinance suffix check
    yf_symbol = symbol + ".NS" if not (symbol.endswith(".NS") or symbol.endswith(".BO")) else symbol
    
    try:
        ticker = yf.Ticker(yf_symbol)
        # Fetch last 2 days to ensure we get latest closed candle. 
        # For bulk history, we might want a different function or parameter.
        hist = ticker.history(period="5d") 
        
        if hist.empty:
            logger.warning(f"No data found for {symbol}")
            return

        async with AsyncSessionLocal() as session:
            # Ensure stock exists
            result = await session.execute(select(Stock).where(Stock.symbol == symbol))
            stock = result.scalars().first()
            if not stock:
                # Auto-create stock entry if missing (simplified)
                # In real app, we might want stricter control
                info = ticker.info
                new_stock = Stock(
                     symbol=symbol, 
                     name=info.get('longName', symbol), 
                     exchange="NSE" if ".NS" in yf_symbol else "BSE"
                )
                session.add(new_stock)
                await session.commit()

            for index, row in hist.iterrows():
                # index is Timestamp
                record_date = index.date()
                
                stmt = insert(MarketData).values(
                    symbol=symbol,
                    date=record_date,
                    open=row['Open'],
                    high=row['High'],
                    low=row['Low'],
                    close=row['Close'],
                    volume=int(row['Volume'])
                )
                # Upsert: do nothing on conflict (or update)
                stmt = stmt.on_conflict_do_update(
                    index_elements=['symbol', 'date'],
                    set_={
                        'open': stmt.excluded.open,
                        'high': stmt.excluded.high,
                        'low': stmt.excluded.low,
                        'close': stmt.excluded.close,
                        'volume': stmt.excluded.volume
                    }
                )
                await session.execute(stmt)
            
            await session.commit()
            logger.info(f"Successfully updated {symbol}")

    except Exception as e:
        logger.error(f"Error fetching {symbol}: {e}")

async def sync_tickers():
    # In a real app, load this list from DB or config
    # For demo, we use a static list
    tickers = ["RELIANCE", "TCS", "INFY", "HDFCBANK"]
    for ticker in tickers:
        await fetch_and_store_data(ticker)
