from datetime import timedelta, datetime

from jose import jwt

from app.settings import settings


def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        key=settings.AUTH_JWT_SECRET_KEY,
        algorithm=settings.AUTH_JWT_TOKEN_ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        key=settings.AUTH_JWT_SECRET_KEY,
        algorithms=[settings.AUTH_JWT_TOKEN_ALGORITHM]
    )


def create_user_auth_tokens(user_id: int) -> dict:
    payload = {"user_id": user_id}

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_TIME)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_TIME)

    access_token = create_token({**payload, "token_type": "access"}, access_token_expires)
    refresh_token = create_token({**payload, "token_type": "refresh"}, refresh_token_expires)

    return {"access": access_token, "refresh": refresh_token}