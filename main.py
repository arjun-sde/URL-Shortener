import logging
from fastapi import FastAPI
from app.api.v1 import v1_router
from app.core.db import init_db
from app.core.config import settings

logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s - %(message)s")

app = FastAPI(title="Fast URL Shortener", version="1.0.0")
app.include_router(v1_router)  # prefix defined in v1/__init__.py

@app.on_event("startup")
async def startup():
    # create tables in dev/test (no-op if already created)
    await init_db()

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
