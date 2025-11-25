import enum

from sqlalchemy import BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from persistent.base import WithId, Base
from persistent.models.task import Task


class TestCaseType(enum.StrEnum):
    Algorithm = "algorithm"
    Math = "math"


class TestCase(Base, WithId):
    __tablename__ = "test_cases"

    stdin: Mapped[str] = mapped_column(default=None, nullable=True)
    expected: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[TestCaseType]

    task_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("tasks.id", ondelete="CASCADE"))
    task: Mapped[Task] = relationship(back_populates="test_cases")
