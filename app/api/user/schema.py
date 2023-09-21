from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"


class AbstractUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    first_name: str
    last_name: str
    patronymic: str
    subdivision: str
    position: str
    role: RoleEnum = RoleEnum.user
    is_active: Optional[bool] = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserCreateSchema(AbstractUser):
    password: str


class UserPubSchema(AbstractUser):
    id: int


class UserSchema(UserPubSchema):
    password_hash: str


class AccessToken(BaseModel):
    access: str


class RefreshTokenSchema(BaseModel):
    refresh: str


class Tokens(AccessToken, RefreshTokenSchema):
    pass
