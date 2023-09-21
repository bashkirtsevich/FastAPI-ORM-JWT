from __future__ import annotations

from datetime import timedelta, datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.settings import settings
from .exceptions import invalid_token_exception, invalid_representation_exception, inactive_user_exception, \
    already_exists_user_exception
from .schema import Tokens, UserLoginSchema, UserSchema, UserPubSchema, RefreshTokenSchema, UserCreateSchema
from .use_cases import GetUserByEmail, GetUserById, UserExistsByEmail, NewUser

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


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


async def get_current_user(token: str, use_case: GetUserById = Depends(GetUserById)) -> UserSchema:
    try:
        payload = decode_token(token)

        token_type: str = payload.get("token_type")
        if token_type != "access":
            raise invalid_token_exception

        user_id: int = payload.get("user_id")

        if user_id is None:
            raise invalid_token_exception

    except JWTError:
        raise invalid_token_exception

    user = await use_case.execute(user_id)
    if user is None:
        raise invalid_representation_exception

    return user


async def get_current_active_user(current_user: Annotated[UserSchema, Depends(get_current_user)]) -> UserSchema:
    if current_user.is_active:
        return current_user
    raise inactive_user_exception


@router.post("/register/", response_model=UserSchema)
async def create_user(
        user_in: UserCreateSchema,
        user_exists: Annotated[UserExistsByEmail, Depends(UserExistsByEmail)],
        new_user: Annotated[NewUser, Depends(NewUser)]
):
    if await user_exists.execute(user_in.email):
        raise already_exists_user_exception

    return await new_user.execute(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        patronymic=user_in.patronymic,
        subdivision=user_in.subdivision,
        position=user_in.subdivision,
        role=user_in.role,
        is_active=False
    )


@router.post("/login/", response_model=Tokens)
async def login(user_in: UserLoginSchema, get_user: Annotated[GetUserByEmail, Depends(GetUserByEmail)]):
    if not (user := await get_user.execute(user_in.email)):
        raise invalid_representation_exception
    if not verify_password(user_in.password, user.password_hash):
        raise invalid_representation_exception

    return create_user_auth_tokens(user.id)


@router.get("/me/", response_model=UserPubSchema)
async def read_users_me(current_user: Annotated[UserPubSchema, Depends(get_current_active_user)]):
    return current_user


@router.post('/refresh/', response_model=Tokens)
async def refresh_user_token(refresh_token: RefreshTokenSchema):
    try:
        payload = decode_token(refresh_token.refresh)
        token_type: str = payload.get("token_type")
        if token_type != "access":
            raise invalid_token_exception

        user_id: int = payload.get("user_id")

        if user_id is None:
            raise invalid_token_exception

    except JWTError:
        raise invalid_token_exception

    return create_user_auth_tokens(user_id)
