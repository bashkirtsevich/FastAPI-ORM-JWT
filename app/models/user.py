from __future__ import annotations

import enum
from typing import AsyncIterator

from sqlalchemy import String, select, Boolean, Enum
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from .abstract import AbstractModel


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"


class User(AbstractModel):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column("email", String(), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column("password_hash", String())
    first_name: Mapped[str] = mapped_column("first_name", String(), nullable=False, index=False)
    last_name: Mapped[str] = mapped_column("last_name", String(), nullable=False, index=False)
    patronymic: Mapped[str] = mapped_column("patronymic", String(), nullable=False, index=False)
    subdivision: Mapped[str] = mapped_column("subdivision", String(), nullable=False, index=True)
    position: Mapped[str] = mapped_column("position", String(), nullable=False, index=True)
    role: Mapped[UserRole] = mapped_column("role", String(), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column("is_active", Boolean(), nullable=False, default=False)

    @classmethod
    async def read_all(cls, session: AsyncSession) -> AsyncIterator[User]:
        return cls._list(session)

    @classmethod
    async def read_by_id(cls, session: AsyncSession, user_id: int) -> User | None:
        return await cls._get(session, user_id)

    @classmethod
    async def read_by_email(cls, session: AsyncSession, email: str) -> User | None:
        query = select(cls).where(cls.email == email)

        return await session.scalar(query.order_by(cls.id))

    @classmethod
    async def create(
            cls, session: AsyncSession, email: str, password_hash: str, first_name: str, last_name: str,
            patronymic: str, subdivision: str, position: str, role: str, is_active: bool = False
    ) -> User:
        user = cls(email=email, password_hash=password_hash, first_name=first_name, last_name=last_name,
                   patronymic=patronymic, subdivision=subdivision, position=position, role=role, is_active=is_active)
        session.add(user)
        await session.flush()

        new = await cls.read_by_id(session, user.id)
        if not new:
            raise RuntimeError()

        return new

    @classmethod
    async def delete(cls, session: AsyncSession, user: User) -> None:
        return await cls._delete(session, user)
