from sqlalchemy import select
from sqlalchemy.orm import selectinload

from persistent.models import Submission, SubmissionResult, SubmissionStatus, Task, TestCase
from schemas import SubmissionGeneralSchema, Judge0SubmissionResultDto, SubmissionResultDto
from schemas.submission import TestCaseResultDto
from .base import BaseRepository


class SubmissionRepository(BaseRepository):
    async def create_submission(self, user_id: str, task_id: int) -> SubmissionGeneralSchema:
        submission = Submission(
            task_id=task_id,
            user_id=user_id
        )
        self.session.add(submission)
        await self.session.commit()
        await self.session.refresh(submission)

        return SubmissionGeneralSchema.from_sqlalchemy(submission)

    async def create_empty_submission_results(
            self,
            submission_id: int,
            testcase_ids: list[int],
            judge0_submission_ids: list[str]
    ):
        for tc_id, token in zip(testcase_ids, judge0_submission_ids):
            submission = SubmissionResult(
                submission_id=submission_id,
                test_case_id=tc_id,
                judge0_submission_id=token,
                status=SubmissionStatus.Pending,
                used_time="0",
                used_memory=0,
                stderr=None,
                stdout=None,
                message=None,
                compile_output=None
            )
            self.session.add(submission)
        await self.session.commit()

    async def set_submission_result(self, submission_result: Judge0SubmissionResultDto):
        q = select(SubmissionResult).where(
            SubmissionResult.judge0_submission_id == submission_result.token
        )
        model: SubmissionResult | None = (await self.session.execute(q)).scalar_one_or_none()  # если model = None, то это гг

        model.status = SubmissionStatus.from_string(submission_result.status.description)
        model.used_time = submission_result.time
        model.used_memory = submission_result.memory
        model.stdout = submission_result.stdout
        model.stderr = submission_result.stderr
        model.compile_output = submission_result.compile_output
        model.message = submission_result.message

        self.session.add(model)
        await self.session.commit()

    async def get_submission_result(self, submission_id: int, load_hidden_test: bool = False) -> SubmissionResultDto | None:
        q = (
            select(Submission)
            .where(Submission.id == submission_id)
            .options(
                selectinload(Submission.results)
                .joinedload(SubmissionResult.test_case)
            )
        )
        result = await self.session.execute(q)
        submission: Submission | None = result.scalar_one_or_none()

        if not submission:
            return None

        status = "Passed"
        testcase_results = []

        for tcr in submission.results:
            test_case = await tcr.awaitable_attrs.test_case
            is_hidden = test_case.is_hidden if test_case else False

            if tcr.status == SubmissionStatus.Failed:
                if not is_hidden:
                    status = "Failed"
                elif status == "Passed":
                    status = "Failed on hidden testcases"

            elif tcr.status == SubmissionStatus.Pending:
                if "Failed" not in status:
                    status = "Pending"

            if is_hidden and not load_hidden_test:
                continue

            stdin = None
            expected = None
            if test_case:
                stdin = test_case.stdin
                expected = test_case.expected

            testcase_results.append(
                TestCaseResultDto.from_sqlalchemy(tcr, stdin, expected)
            )

        return SubmissionResultDto(
            id=submission_id,
            status=status,
            task_id=submission.task_id,
            testcase_results=testcase_results
        )
