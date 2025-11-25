from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from persistent.base import WithId, Base
if TYPE_CHECKING:
    from .test_case import TestCase


class Task(Base, WithId):
    __tablename__ = "tasks"

    test_cases: Mapped[list["TestCase"]] = relationship()
