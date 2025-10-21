import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

logger = logging.getLogger(__name__)

# Async engine (connection pool is managed internally by SQLAlchemy)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Set True for debugging queries
    future=True,
)

# Session factory for dependency injection
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_session() -> AsyncSession:
    """
    Dependency for FastAPI endpoints.
    Provides an AsyncSession per request.
    """
    async with async_session() as session:
        yield session
