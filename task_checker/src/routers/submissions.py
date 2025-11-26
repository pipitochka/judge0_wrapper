from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from repositories import SubmissionRepository
from services import Judge0Service
from schemas import CreateSubmissionSchema, Judge0SubmissionResultDto

router = APIRouter(prefix="/submissions", tags=["submissions"], route_class=DishkaRoute)


@router.get("/{submission_id}")
async def get_submission(submission_id: int, repo: FromDishka[SubmissionRepository]):
    return await repo.get_submission_result(submission_id)


@router.post("/")
async def create_submission(
        submission: CreateSubmissionSchema,
        judge_service: FromDishka[Judge0Service],
        test: bool = False,
        open_tests: bool = False
):
    if test and open_tests:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Submission cannot be run wit and run on `open tests` at the same time!"}
        )

    if test:
        return await judge_service.create_test_submission(submission)
    return await judge_service.create_submission(submission, open_tests)


@router.put("/callback")
async def judge0_callback(
        submission_result: Judge0SubmissionResultDto,
        repo: FromDishka[SubmissionRepository]
):
    await repo.set_submission_result(submission_result)
    return "ok"
