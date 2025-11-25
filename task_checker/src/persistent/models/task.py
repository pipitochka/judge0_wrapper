from typing import TYPE_CHECKING
import enum

from sqlalchemy.orm import Mapped, relationship

from persistent.base import WithId, Base
if TYPE_CHECKING:
    from .test_case import TestCase


class TestCaseType(enum.StrEnum):
    Algorithm = "algorithm"
    Math = "math"
    AI_validated = "ai"


class Task(Base, WithId):
    __tablename__ = "tasks"

    title: Mapped[str]
    content: Mapped[str | None]
    type: Mapped[TestCaseType]

    test_cases: Mapped[list["TestCase"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
