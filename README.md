# Share Market Data Service

A REST API service to collect, store, and serve public share market data for NSE & BSE using FastAPI, TimescaleDB, and yfinance.

## Prerequisites

- Python 3.9+
- Docker Desktop

## Setup & Run

1.  **Start Database:**
    Ensure Docker is running, then start the TimescaleDB container:
    ```bash
    docker-compose up -d
    ```

2.  **Install Application Dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Run the Application:**
    ```bash
    uvicorn app.main:app --reload
    ```

4.  **Access:**
    - API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
    - Root: [http://localhost:8000/](http://localhost:8000/)

## Project Structure

- `app/` - Application source code
    - `api/` - API endpoints
    - `core/` - Configuration & DB setup
    - `models/` - Database models
    - `services/` - Background services (Ingestion, Scheduler)
- `docker-compose.yml` - Database orchestration

## Verification
You can use `curl` or the Swagger UI to test:
```bash
curl http://localhost:8000/api/v1/stocks
```
To trigger a manual ingestion (for testing), you can run a python shell:
```python
from app.services.ingestor import fetch_and_store_data
import asyncio
asyncio.run(fetch_and_store_data("RELIANCE"))
```
