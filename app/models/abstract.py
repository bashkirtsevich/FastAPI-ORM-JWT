import datetime

from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

Base = declarative_base()


class AbstractModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)


class TimestampedModel(AbstractModel):
    __abstract__ = True

    timestamp: Mapped[datetime.datetime] = mapped_column(
        "timestamp", DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
    )
