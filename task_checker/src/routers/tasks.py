from fastapi import APIRouter, HTTPException

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from repositories import TaskRepository, TestCaseRepository
from schemas.task import (
    TaskDto, CreateTaskDto, UpdateTaskDto,
    TestCaseDto, CreateTestCaseDto, UpdateTestCaseDto
)

router = APIRouter(prefix="/tasks", tags=["tasks"], route_class=DishkaRoute)


@router.get("/{task_id}/testcases/all", response_model=list[TestCaseDto])
async def get_task_cases(
    task_id: int,
    testcase_repo: FromDishka[TestCaseRepository]
):
    return await testcase_repo.get_testcases(task_id)


@router.get("/{task_id}/testcases/only_visible", response_model=list[TestCaseDto])
async def get_task_visible_cases(
    task_id: int,
    testcase_repo: FromDishka[TestCaseRepository]
):
    return await testcase_repo.get_visible_testcases(task_id)


@router.post("/{task_id}/testcases", response_model=TestCaseDto)
async def create_test_case(
    task_id: int,
    data: CreateTestCaseDto,
    testcase_repo: FromDishka[TestCaseRepository]
):
    return await testcase_repo.create_testcase(task_id, data)


@router.put("/{task_id}/testcases/{testcase_id}", response_model=TestCaseDto)
async def edit_test_case(
    task_id: int,
    testcase_id: int,
    data: UpdateTestCaseDto,
    testcase_repo: FromDishka[TestCaseRepository]
):
    testcase = await testcase_repo.update_testcase(task_id, testcase_id, data)
    if testcase is None:
        raise HTTPException(status_code=404, detail="TestCase not found")
    return testcase


@router.get("/{task_id}/testcases/{testcase_id}", response_model=TestCaseDto)
async def get_test_case(
    task_id: int,
    testcase_id: int,
    testcase_repo: FromDishka[TestCaseRepository]
):
    testcase = await testcase_repo.get_testcase(task_id, testcase_id)
    if testcase is None:
        raise HTTPException(status_code=404, detail="TestCase not found")
    return testcase


@router.delete("/{task_id}/testcases/{testcase_id}")
async def delete_test_case(
    task_id: int,
    testcase_id: int,
    testcase_repo: FromDishka[TestCaseRepository]
):
    deleted = await testcase_repo.delete_testcase(task_id, testcase_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="TestCase not found")
    return {"detail": "TestCase deleted"}


@router.get("/{task_id}", response_model=TaskDto)
async def get_task(
    task_id: int,
    task_repo: FromDishka[TaskRepository]
):
    task = await task_repo.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=TaskDto)
async def create_task(
    data: CreateTaskDto,
    task_repo: FromDishka[TaskRepository]
):
    return await task_repo.create_task(data)


@router.put("/{task_id}", response_model=TaskDto)
async def edit_task(
    task_id: int,
    data: UpdateTaskDto,
    task_repo: FromDishka[TaskRepository]
):
    task = await task_repo.update_task(task_id, data)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    task_repo: FromDishka[TaskRepository]
):
    deleted = await task_repo.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}
