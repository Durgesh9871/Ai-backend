
from uuid import UUID
from datetime import datetime,timezone
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import Self


class EventCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=3, max_length=20)
    capacity: int = Field(gt=0, lt=10000)
    currency: str = Field(min_length=3, max_length=3, pattern=r"^[A-Z]{3}$",)
    start_time: datetime
    @field_validator('currency', mode='before')
    @classmethod
    def normalize_currency(cls, value:str)->str:
        value = value.strip().upper()
        if value not in ['USD', 'EUR', 'GBP', 'INR']:
            raise ValueError('Currency must be one of USD, EUR, GBP, INR')
        return value

    @field_validator('start_time')
    @classmethod
    def validate_start_time(cls, v):
        if v.tzinfo is None or v.utcoffset() is None:
            raise ValueError('Start time must not have timezone info')
        if v <= datetime.now(timezone.utc):
            raise ValueError('Start time must be in the future')
        return v


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

    @field_validator('start_time')
    @classmethod
    def validate_start_time(cls, v):
        if v is None:
            return v
        if v.tzinfo is None or v.utcoffset() is None:
            raise ValueError('Start time must not have timezone info')
        if v <= datetime.now(timezone.utc):
            raise ValueError('Start time must be in the future')
        return v


    @field_validator('currency')
    @classmethod
    def validate_currency(cls, v):
        if v is None:
            return v
        v = v.strip().upper()
        if v not in ['USD', 'EUR', 'GBP', 'INR']:
            raise ValueError('Currency must be one of USD, EUR, GBP, INR')
        return v

    @model_validator(mode='after')
    def validate_update_fields(self) -> Self:
        
        for value in (self.name, self.capacity, self.currency, self.start_time):
            if value is not None:
                break
        else:
            raise ValueError('At least one field must be provided for update')
        return self