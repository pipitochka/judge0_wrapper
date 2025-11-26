from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from persistent.models import TaskType
from repositories import SubmissionRepository, TestCaseRepository, TaskRepository
from services import Judge0Service
from schemas import CreateSubmissionSchema, Judge0SubmissionResultDto
from services.submission import SubmissionService

router = APIRouter(prefix="/submissions", tags=["submissions"], route_class=DishkaRoute)


@router.get("/{submission_id}")
async def get_submission(submission_id: int, repo: FromDishka[SubmissionRepository]):
    return await repo.get_submission_result(submission_id)


@router.post("/")
async def create_submission(
        submission: CreateSubmissionSchema,
        submission_service: FromDishka[SubmissionService],
        test: bool = False,
        open_tests: bool = False
):
    if test and open_tests:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Submission cannot be run wit and run on `open tests` at the same time!"}
        )
    return await submission_service.submit_solution(submission, test, open_tests)


@router.put("/callback")
async def judge0_callback(
        submission_result: Judge0SubmissionResultDto,
        repo: FromDishka[SubmissionRepository]
):
    await repo.set_submission_result(submission_result)
    return "ok"
