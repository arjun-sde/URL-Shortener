from datetime import datetime
from typing import Optional

from pydantic import AnyUrl, BaseModel

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

    # Pydantic v2 style
    model_config = {
        "from_attributes": True
    }
