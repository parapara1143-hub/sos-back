
from pydantic import BaseModel, Field
from typing import Optional, List

class AttachmentIn(BaseModel):
    url: str
    label: Optional[str] = None

class IncidentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    attachments: Optional[List[AttachmentIn]] = None
