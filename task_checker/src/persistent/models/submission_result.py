import enum

from sqlalchemy import BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from persistent.base import WithTimestamp, WithId, Base
from .submission import Submission
from .test_case import TestCase


class SubmissionStatus(enum.StrEnum):
    Pending = "pending"
    Failed = "failed"
    Passed = "passed"


class SubmissionResult(Base, WithId, WithTimestamp):
    __tablename__ = "submission_results"

    submission_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("submissions.id"))
    test_case_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("test_cases.id"))
    stdout: Mapped[str]
    status: Mapped[SubmissionStatus] = mapped_column(default=SubmissionStatus.Passed)

    submission: Mapped[Submission] = relationship(back_populates="results")
    test_case: Mapped[TestCase] = relationship()
