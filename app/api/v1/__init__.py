from fastapi import APIRouter
from .shortener import router as url_router

v1_router = APIRouter(prefix="/api/v1", tags=["v1"])
v1_router.include_router(url_router)