from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.schemas.url_schemas import URLCreateSchema, ShortenResponseSchema, URLInfoSchema
from app.core import get_session
from app.services.impl.url_service_impl import URLServiceImpl
from app.core.config import settings

router = APIRouter()
service = URLServiceImpl()

async def resolve_domain(request: Request, domain_in: Optional[str] = None) -> str:
    if domain_in:
        return domain_in
    host = request.headers.get("x-forwarded-host") or request.headers.get("host")
    if host:
        return host.split(":")[0]
    return "default"

@router.post("/shorten", response_model=ShortenResponseSchema, status_code=status.HTTP_201_CREATED)
async def shorten_url(payload: URLCreateSchema, request: Request, session: AsyncSession = Depends(get_session)):
    domain = await resolve_domain(request, payload.domain)
    url_obj = await service.shorten(session, payload.original_url, domain)
    # choose returned domain depending on config
    if settings.ENABLE_MULTI_TENANT:
        short_url = f"{request.url.scheme}://{domain}/s/{url_obj.short_code}"
    else:
        short_url = f"{settings.BASE_URL.rstrip('/')}/s/{url_obj.short_code}"
    return ShortenResponseSchema(short_url=short_url, short_code=url_obj.short_code)

@router.get("/s/{short_code}")
async def redirect_short(short_code: str, request: Request, session: AsyncSession = Depends(get_session)):
    domain = (request.headers.get("x-forwarded-host") or request.headers.get("host") or "default").split(":")[0]
    url_obj = await service.get_and_increment(session, domain, short_code)
    if not url_obj:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url_obj.original_url)

@router.get("/stats/{short_code}", response_model=URLInfoSchema)
async def stats(short_code: str, request: Request, session: AsyncSession = Depends(get_session)):
    domain = (request.headers.get("x-forwarded-host") or request.headers.get("host") or "default").split(":")[0]
    url_obj = await service.get(session, domain, short_code)
    if not url_obj:
        raise HTTPException(status_code=404, detail="URL not found")
    return URLInfoSchema.from_orm(url_obj)
