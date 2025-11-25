from typing import Annotated
from datetime import datetime

from sqlalchemy import func, inspect, Integer
from sqlalchemy.orm import Mapped, sessionmaker, DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs, create_async_engine

created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[
    datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)
]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id!r})'


class WithId:
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class WithTimestamp:
    __abstract__ = True

    created_at: created_at
    updated_at: updated_at
