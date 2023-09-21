from __future__ import annotations

import datetime
from typing import AsyncIterator

from sqlalchemy import DateTime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

Base = declarative_base()


class AbstractModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)

    @classmethod
    async def _list(cls, session: AsyncSession) -> AsyncIterator[AbstractModel]:
        query = select(cls)

        stream = await session.stream_scalars(query.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def _get(cls, session: AsyncSession, id: int) -> AbstractModel | None:
        query = select(cls).where(cls.id == id)

        return await session.scalar(query.order_by(cls.id))

    @classmethod
    async def _delete(cls, session: AsyncSession, obj: AbstractModel) -> None:
        await session.delete(obj)
        await session.flush()


class TimestampedModel(AbstractModel):
    __abstract__ = True

    timestamp: Mapped[datetime.datetime] = mapped_column(
        "timestamp", DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
    )
