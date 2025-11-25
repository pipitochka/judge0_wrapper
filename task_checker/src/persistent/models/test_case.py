import enum

from sqlalchemy import BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from persistent.base import WithId, Base
from persistent.models.task import Task


class TestCaseType(enum.StrEnum):
    Algorithm = "algorithm"
    Math = "math"
    AI_validated = "ai"


class TestCase(Base, WithId):
    __tablename__ = "test_cases"

    stdin: Mapped[str | None]
    expected: Mapped[str]

    type: Mapped[TestCaseType]

    time_limit: Mapped[float | None]
    memory_limit: Mapped[int | None]

    is_hidden: Mapped[bool] = mapped_column(default=True)

    task_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("tasks.id", ondelete="CASCADE"))
    task: Mapped[Task] = relationship(back_populates="test_cases")
