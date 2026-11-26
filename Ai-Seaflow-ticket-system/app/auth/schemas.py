



from pydantic import BaseModel, EmailStr, Field, field_validator
from app.users.models import UserRole

class RegisterRequest(BaseModel):
    email: EmailStr
    @field_validator('email', mode='before')
    @classmethod
    def validate_email(cls, value):
        value = value.strip().lower()
        return value



    password: str = Field(min_length=3, max_length=100)


   
class UserResponse(BaseModel):
    email: EmailStr
    is_active: bool
    role: UserRole


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"  