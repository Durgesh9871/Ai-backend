from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, EmailStr




class UserRole(StrEnum):
    CUSTOMER = "customer"
    ORGANIZER = "organizer"
    ADMIN = "admin"


class User(BaseModel):
    id: UUID
    email: EmailStr
    hashed_password: str
    role: UserRole = UserRole.CUSTOMER
    is_active: bool = True