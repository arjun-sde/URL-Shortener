from pydantic import BaseModel, AnyUrl
from datetime import datetime
from typing import Optional

class URLCreateSchema(BaseModel):
    original_url: AnyUrl
    domain: Optional[str] = None

class ShortenResponseSchema(BaseModel):
    short_url: AnyUrl
    short_code: str

from datetime import datetime
from pydantic import BaseModel, AnyUrl

class URLInfoSchema(BaseModel):
    id: int
    domain: str
    original_url: AnyUrl
    short_code: str
    clicks: int
    created_at: datetime

    # Pydantic v2 style
    model_config = {
        "from_attributes": True  # replaces orm_mode=True
    }

