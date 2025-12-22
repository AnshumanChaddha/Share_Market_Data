from fastapi import FastAPI
from app.api import endpoints, cron
from app.core.database import engine, Base
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Share Market Data Service")

# Include Routers
app.include_router(endpoints.router, prefix="/api/v1")
app.include_router(cron.router, prefix="/api/v1/cron")

@app.on_event("startup")
async def startup_event():

    logger.info("Starting up...")
    # Create tables (In production, use Alembic migrations)
    # Note: For Vercel, we might need to run migration manually or check on startup
    # Since Vercel is serverless, running create_all on every hot cold start is okay for small scale
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
def read_root():
    return {"message": "Share Market Data Service is running"}
