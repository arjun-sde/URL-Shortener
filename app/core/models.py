from sqlalchemy import Column, Integer, String, Text, DateTime, func, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), nullable=False, index=True)
    original_url = Column(Text, nullable=False)
    short_code = Column(String(64), nullable=False, index=True)
    clicks = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("domain", "short_code", name="uq_domain_short_code"),
    )
