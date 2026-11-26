from app.users.models import User
from uuid import UUID



_user_store: dict[str, User] = {}


def get_user_by_email(email: str) -> User | None:
    return _user_store.get(email.lower())


def save_user(user: User) -> User:
    _user_store[user.email.lower()] = user
    return user


def get_user_by_id(user_id: UUID) -> User | None:
    
    return next(
        (user for user in _user_store.values() if user.id == user_id),
        None,
    )