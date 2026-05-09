from pydantic import AnyUrl, TypeAdapter

from app.services.impl.url_service_impl import URLServiceImpl


class FakeDAO:
    def __init__(self):
        self.urls = {}

    async def create(self, session, url_obj):
        self.urls[(url_obj.domain, url_obj.short_code)] = url_obj
        return url_obj

    async def get_by_domain_and_code(self, session, domain, short_code):
        return self.urls.get((domain, short_code))

    async def increment_clicks(self, session, url_obj):
        url_obj.clicks += 1


class FakeSession:
    def __init__(self):
        self.commits = 0

    async def commit(self):
        self.commits += 1

    async def rollback(self):
        pass

    async def refresh(self, url_obj):
        pass


def build_service(fake_dao):
    service = object.__new__(URLServiceImpl)
    service.dao = fake_dao
    service._initialized = True
    return service


async def test_shorten_creates_code_and_stats_lookup():
    fake_dao = FakeDAO()
    service = build_service(fake_dao)
    session = FakeSession()
    original_url = TypeAdapter(AnyUrl).validate_python("https://example.com/articles/1")

    url_obj = await service.shorten(session, original_url, "default")
    found = await service.get(session, "default", url_obj.short_code)

    assert found is not None
    assert found.id == url_obj.id
    assert found.original_url == "https://example.com/articles/1"
    assert len(found.short_code) >= 7
    assert session.commits == 1


async def test_get_and_increment_updates_click_count():
    fake_dao = FakeDAO()
    service = build_service(fake_dao)
    session = FakeSession()
    original_url = TypeAdapter(AnyUrl).validate_python("https://example.com")
    url_obj = await service.shorten(session, original_url, "default")

    clicked = await service.get_and_increment(session, "default", url_obj.short_code)

    assert clicked is not None
    assert clicked.clicks == 1
    assert session.commits == 2
