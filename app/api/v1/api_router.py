from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import async_session
from app.schemas import URLCreate, URLResponse
from app.services import URLService

router = APIRouter()

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@router.post("/shorten", response_model=URLResponse)
async def shorten_url(data: URLCreate, session: AsyncSession = Depends(get_session)):
    service = URLService(session)
    short_url = await service.shorten_url(data.original_url)
    return URLResponse(short_url=short_url, created_at=None)

@router.get("/{code}")
async def redirect_url(code: str, session: AsyncSession = Depends(get_session)):
    service = URLService(session)
    url_entry = await service.resolve_url(code)
    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url_entry.original_url)
