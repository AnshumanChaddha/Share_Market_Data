from fastapi import APIRouter, Header, HTTPException
from app.services.ingestor import sync_tickers
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/sync")
async def trigger_sync(authorization: str = Header(None)):
    # Vercel Cron jobs are authorized via a secret header or we can just keep it open for hobby
    # Ideally verify: Authorization: Bearer <CRON_SECRET>
    # For now, we'll double check env var match if set
    
    cron_secret = os.getenv("CRON_SECRET")
    if cron_secret and authorization != f"Bearer {cron_secret}":
         logger.warning("Unauthorized cron attempt")
         raise HTTPException(status_code=401, detail="Unauthorized")
    
    logger.info("Cron: Triggering sync_tickers")
    await sync_tickers()
    return {"status": "Sync initiated"}
