from fastapi import HTTPException

from .schema import UserSchema
from ...db import AsyncSession
from ...models.user import User


class GetUserByEmail:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, email: str) -> UserSchema:
        async with self.async_session() as session:
            if not (user := await User.read_by_email(session, email)):
                raise HTTPException(status_code=404)

            return UserSchema.model_validate(user)


class GetUserById:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, user_id: int) -> UserSchema:
        async with self.async_session() as session:
            if not (user := await User.read_by_id(session, user_id)):
                raise HTTPException(status_code=404)

        return UserSchema.model_validate(user)


class UserExistsByEmail:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, email: str) -> bool:
        async with self.async_session() as session:
            user = await User.read_by_email(session, email)
        return user is not None


class NewUser:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, email, password_hash, first_name, last_name, patronymic, subdivision, position, role,
                      is_active) -> UserSchema:
        async with self.async_session() as session:
            user = await User.create(
                session, email, password_hash, first_name, last_name, patronymic, subdivision, position, role, is_active
            )
        return UserSchema.model_validate(user)
