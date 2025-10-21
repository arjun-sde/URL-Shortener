from fastapi import FastAPI
from app.api import v1_router
from app.core.db import init_db

app = FastAPI(title="Fast URL Shortener")

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to Fast URL Shortener API"}
