import logging

from pydantic import AnyUrl
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.interface.url_service_interface import URLServiceInterface
from app.dao.impl.url_dao_impl import URLDAOImpl
from app.core.models import URL
from app.utils.shortener import generate_url_id, id_to_code

logger = logging.getLogger(__name__)

class URLServiceImpl(URLServiceInterface):
    """
    Singleton service with DAO dependency (depends on URLDAOInterface impl).
    """

    _instance = None

    def __new__(cls, dao: URLDAOImpl = None, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(URLServiceImpl, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, dao: URLDAOImpl = None):
        if getattr(self, "_initialized", False):
            return
        self.dao = dao or URLDAOImpl()
        logger.info(f"Initializing URLServiceImpl singleton id={id(self)}")
        self._initialized = True

    async def shorten(self, session: AsyncSession, original_url: AnyUrl, domain: str) -> URL:
        for attempt in range(3):
            url_id = generate_url_id()
            url_obj = URL(
                id=url_id,
                domain=domain,
                original_url=str(original_url),
                short_code=id_to_code(url_id),
                clicks=0,
            )

            try:
                url_obj = await self.dao.create(session, url_obj)
                await session.commit()
                await session.refresh(url_obj)
                return url_obj
            except IntegrityError:
                await session.rollback()
                logger.warning("short code collision while creating URL", extra={"attempt": attempt + 1})

        raise RuntimeError("failed to create a unique short URL after retries")

    async def get_and_increment(self, session: AsyncSession, domain: str, short_code: str):
        url_obj = await self.dao.get_by_domain_and_code(session, domain, short_code)
        if not url_obj:
            return None
        await self.dao.increment_clicks(session, url_obj)
        await session.commit()
        await session.refresh(url_obj)
        return url_obj

    async def get(self, session: AsyncSession, domain: str, short_code: str):
        return await self.dao.get_by_domain_and_code(session, domain, short_code)
