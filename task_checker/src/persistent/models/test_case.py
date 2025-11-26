from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from persistent.base import WithId, Base
from persistent.models.task import Task


class TestCase(Base, WithId):
    __tablename__ = "test_cases"

    stdin: Mapped[str | None]
    expected: Mapped[str]

    time_limit: Mapped[float] = mapped_column(default=2)
    memory_limit: Mapped[int] = mapped_column(default=32000)

    is_hidden: Mapped[bool] = mapped_column(default=True)

    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"))
    task: Mapped[Task] = relationship(back_populates="test_cases")
