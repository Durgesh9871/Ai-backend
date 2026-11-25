from pwdlib import PasswordHash



hasher = PasswordHash.recommended()


def password_hash(password: str) -> str:
    return hasher.hash(password)


def password_verify(password: str, hashed_password: str) -> bool:
    return hasher.verify(password, hashed_password)


hashed = password_hash("secret123")

assert hashed != "secret123"
assert password_verify("secret123", hashed)
assert not password_verify("wrong-password", hashed)