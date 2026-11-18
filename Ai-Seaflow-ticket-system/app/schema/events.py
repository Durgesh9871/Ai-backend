
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class EventCreate(BaseModel):
    name: str = field(min_length=3, max_length=20)
    capacity: int = field(gt=4)
    currency: str =field(min_length=3, max_length=3)
    start_time: datetime


class EventResponse(BaseModel):
    id: UUID
    