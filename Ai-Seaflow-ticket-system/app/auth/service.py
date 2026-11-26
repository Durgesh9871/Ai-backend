from app.users.repository import get_user_by_email, save_user
from app.users.models import User
from app.core.security import hash_password
from app.auth.schemas import RegisterRequest
from uuid import uuid4
from app.core.security import verify_password



from fastapi import HTTPException, status


def register_user(payload: RegisterRequest) -> User:
    user = get_user_by_email(payload.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    hashed_password = hash_password(payload.password)
    user = User(
        id=uuid4(),
        email=payload.email,
        hashed_password=hashed_password
    )
    return save_user(user)



def authenticate_user(email: str, password: str) -> User | None:
    user = get_user_by_email(email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    if not user.is_active:
        return None

    return user