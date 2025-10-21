from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import URL

class URLServiceInterface:
    async def shorten(self, session: AsyncSession, original_url: str, domain: str) -> URL:
        raise NotImplementedError

    async def get_and_increment(self, session: AsyncSession, domain: str, short_code: str) -> Optional[URL]:
        raise NotImplementedError

    async def get(self, session: AsyncSession, domain: str, short_code: str) -> Optional[URL]:
        raise NotImplementedError
