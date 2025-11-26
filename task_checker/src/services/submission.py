from fastapi import HTTPException

from persistent.models import TaskType
from repositories import TaskRepository, TestCaseRepository, SubmissionRepository
from schemas import CreateSubmissionSchema, SubmissionGeneralSchema
from services import Judge0Service


class SubmissionService:
    def __init__(
            self,
            task_repo: TaskRepository,
            testcases_repo: TestCaseRepository,
            submission_repo: SubmissionRepository,
            judge0_service: Judge0Service
    ):
        self.task_repo = task_repo
        self.tc_repo = testcases_repo
        self.submission_repo = submission_repo
        self.judge_service = judge0_service

    async def submit_solution(self, submission: CreateSubmissionSchema, test: bool, open_tests: bool) -> SubmissionGeneralSchema:
        task = await self.task_repo.get_task(submission.task_id)
        if test and (not task or task.type == TaskType.Algorithm):  # тестовый прогон доступен только для алгозадач
            return await self.judge_service.create_test_submission(submission)

        elif not task:
            raise HTTPException(status_code=404, detail="Task with such id not found")

        elif task.type == TaskType.Algorithm:
            return await self.judge_service.create_submission(submission, open_tests)
        elif task.type == TaskType.Math:
            testcases = await self.tc_repo.get_testcases(task.id, False)
            submission_model = await self.submission_repo.create_submission("0", task.id, submission.answer)

            if len(testcases) != 1:
                print("wtf")
            testcase = testcases[0]

            await self.submission_repo.create_non_algorithmic_submission(
                submission_model.id,
                testcase.id,
                submission.answer == testcase.expected  # TODO: возможно нужно какое-то более сложное сравнение
            )
            return submission_model

        elif task.type == TaskType.AI_validated:
            raise HTTPException(status_code=418, detail="Sorry, we have not implemented this type of tasks yet")
        else:
            raise HTTPException(status_code=403, detail="Incorrect task type")
