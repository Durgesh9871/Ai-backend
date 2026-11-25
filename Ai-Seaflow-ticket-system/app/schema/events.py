
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class EventCreate(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    capacity: int = Field(gt=4)
    currency: str = Field(min_length=3, max_length=3, pattern=r"^[A-Z]{3}$",)
    start_time: datetime | None


class EventResponse(BaseModel):
    id: UUID
    name: str
    capacity: int
    currency: str
    start_time: datetime
    


class EventUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=20)

    capacity: int | None = Field(default=None, gt=4)

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
        pattern=r"^[A-Z]{3}$"
    )

    start_time: datetime | None = None    