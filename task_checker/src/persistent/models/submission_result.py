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

    @classmethod
    def from_string(cls, val: str):
        match val:
            case "Accepted":
                return SubmissionStatus.Passed
            case "Pending":
                return SubmissionStatus.Pending
            case _:
                return SubmissionStatus.Failed


class SubmissionResult(Base, WithId, WithTimestamp):
    __tablename__ = "submission_results"

    submission_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("submissions.id"))
    test_case_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("test_cases.id"))
    judge0_submission_id: Mapped[str]

    used_time: Mapped[str] = mapped_column(default=0)
    used_memory: Mapped[int] = mapped_column(default=0)

    stdout: Mapped[str | None]
    stderr: Mapped[str | None]
    compile_output: Mapped[str | None]
    message: Mapped[str | None]

    status: Mapped[SubmissionStatus] = mapped_column(default=SubmissionStatus.Pending)

    submission: Mapped[Submission] = relationship(back_populates="results")
    test_case: Mapped[TestCase] = relationship()
