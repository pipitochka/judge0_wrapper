from typing import TYPE_CHECKING

from sqlalchemy import BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from persistent.base import WithId, WithTimestamp, Base
from .task import Task
if TYPE_CHECKING:
    from .submission_result import SubmissionResult


class Submission(Base, WithId, WithTimestamp):
    __tablename__ = "submissions"

    task_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("tasks.id"))
    user_id: Mapped[str]
    answer: Mapped[str]

    task: Mapped[Task] = relationship()
    results: Mapped[list["SubmissionResult"]] = relationship()
