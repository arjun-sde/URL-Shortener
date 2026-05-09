from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.core.config import settings
from app.schemas.url_schemas import URLCreateSchema, ShortenResponseSchema, URLInfoSchema
from app.services.impl.url_service_impl import URLServiceImpl

router = APIRouter()
redirect_router = APIRouter()
service = URLServiceImpl()


def resolve_domain(request: Request, domain_in: Optional[str] = None) -> str:
    if not settings.ENABLE_MULTI_TENANT:
        return settings.DEFAULT_DOMAIN
    if domain_in:
        return domain_in.lower()
    host = request.headers.get("x-forwarded-host") or request.headers.get("host")
    if host:
        return host.split(":")[0].lower()
    return settings.DEFAULT_DOMAIN


def build_short_url(request: Request, domain: str, short_code: str) -> str:
    if settings.ENABLE_MULTI_TENANT:
        return f"{request.url.scheme}://{domain}/s/{short_code}"
    return f"{settings.BASE_URL.rstrip('/')}/s/{short_code}"


@router.post("/shorten", response_model=ShortenResponseSchema, status_code=status.HTTP_201_CREATED)
async def shorten_url(payload: URLCreateSchema, request: Request, session: AsyncSession = Depends(get_session)):
    domain = resolve_domain(request, payload.domain)
    url_obj = await service.shorten(session, payload.original_url, domain)
    return ShortenResponseSchema(
        short_url=build_short_url(request, domain, url_obj.short_code),
        short_code=url_obj.short_code,
    )


@redirect_router.get("/s/{short_code}", include_in_schema=False)
async def redirect_short(short_code: str, request: Request, session: AsyncSession = Depends(get_session)):
    domain = resolve_domain(request)
    url_obj = await service.get_and_increment(session, domain, short_code)
    if not url_obj:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url_obj.original_url)


@router.get("/stats/{short_code}", response_model=URLInfoSchema)
async def stats(short_code: str, request: Request, session: AsyncSession = Depends(get_session)):
    domain = resolve_domain(request)
    url_obj = await service.get(session, domain, short_code)
    if not url_obj:
        raise HTTPException(status_code=404, detail="URL not found")
    return URLInfoSchema.model_validate(url_obj)
