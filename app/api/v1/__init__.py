from app.api.v1.api_router import router
from fastapi import APIRouter

v1_router = APIRouter()
v1_router.include(router)