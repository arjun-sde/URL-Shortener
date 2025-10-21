import logging
from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.interface.url_dao_interface import URLDAOInterface
from app.core.models import URL

logger = logging.getLogger(__name__)

class URLDAOImpl(URLDAOInterface):
    """
    Singleton DAO implementation for URL operations (async).
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(URLDAOImpl, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        logger.info(f"Initializing URLDAOImpl singleton id={id(self)}")
        self._initialized = True

    async def create(self, session: AsyncSession, url_obj: URL) -> URL:
        session.add(url_obj)
        # flush to assign PK without commit
        await session.flush()
        return url_obj

    async def get_by_domain_and_code(self, session: AsyncSession, domain: str, short_code: str) -> Optional[URL]:
        stmt = select(URL).where(URL.domain == domain, URL.short_code == short_code)
        res = await session.execute(stmt)
        return res.scalars().first()

    async def increment_clicks(self, session: AsyncSession, url_obj: URL) -> None:
        # atomic increment for concurrency safety
        await session.execute(
            update(URL)
            .where(URL.id == url_obj.id)
            .values(clicks=URL.clicks + 1)
        )
        # no commit here; caller controls commit

    async def get_by_id(self, session: AsyncSession, id_: int) -> Optional[URL]:
        stmt = select(URL).where(URL.id == id_)
        res = await session.execute(stmt)
        return res.scalars().first()
