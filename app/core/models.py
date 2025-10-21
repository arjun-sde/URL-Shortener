from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.db import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String(6), unique=True, index=True, nullable=False)
    domain = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
