import logging
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.interface.url_service_interface import URLServiceInterface
from app.dao.impl.url_dao_impl import URLDAOImpl
from app.core.models import URL
from app.utils.shortener import id_to_code, random_code

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

    async def shorten(self, session: AsyncSession, original_url: str, domain: str) -> URL:
        # Create new URL row and flush to get id
        url_obj = URL(domain=domain, original_url=original_url, short_code="")
        url_obj = await self.dao.create(session, url_obj)

        # Generate deterministic code from the ID
        code = id_to_code(url_obj.id)
        if not code:
            code = random_code(6)
        url_obj.short_code = code

        try:
            # commit the new row with short_code
            await session.commit()
        except IntegrityError:
            # collision within domain - fallback to random and retry commit
            await session.rollback()
            url_obj.short_code = random_code(6)
            session.add(url_obj)
            await session.commit()

        await session.refresh(url_obj)
        return url_obj

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
