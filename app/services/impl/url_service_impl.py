from app.dao import URLDAO
from app.core.config import settings

class URLService:
    def __init__(self, session):
        self.dao = URLDAO(session)

    async def shorten_url(self, original_url: str):
        domain = original_url.split("/")[2]
        url = await self.dao.create_url(original_url, domain)
        return f"{settings.BASE_URL}/{url.short_code}"

    async def resolve_url(self, code: str):
        return await self.dao.get_by_code(code)
