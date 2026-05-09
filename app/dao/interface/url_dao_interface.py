from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import URL

class URLDAOInterface:
    async def create(self, session: AsyncSession, url_obj: URL) -> URL:
        raise NotImplementedError

    async def get_by_domain_and_code(self, session: AsyncSession, domain: str, short_code: str) -> Optional[URL]:
        raise NotImplementedError

    async def increment_clicks(self, session: AsyncSession, url_obj: URL) -> None:
        raise NotImplementedError

    async def get_by_id(self, session: AsyncSession, id_: int) -> Optional[URL]:
        raise NotImplementedError
