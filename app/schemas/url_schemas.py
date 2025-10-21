from pydantic import BaseModel, AnyUrl
from datetime import datetime
from typing import Optional

class URLCreateSchema(BaseModel):
    original_url: AnyUrl
    domain: Optional[str] = None

class ShortenResponseSchema(BaseModel):
    short_url: AnyUrl
    short_code: str

class URLInfoSchema(BaseModel):
    id: int
    domain: str
    original_url: AnyUrl
    short_code: str
    clicks: int
    created_at: datetime

    class Config:
        orm_mode = True
