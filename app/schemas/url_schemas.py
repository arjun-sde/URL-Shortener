from pydantic import BaseModel, AnyHttpUrl
from datetime import datetime

class URLCreate(BaseModel):
    original_url: AnyHttpUrl

class URLResponse(BaseModel):
    short_url: AnyHttpUrl
    created_at: datetime | None = None
