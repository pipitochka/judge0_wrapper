from fastapi import APIRouter, Request, Depends

from dishka.integrations.fastapi import DishkaRoute, FromDishka

router = APIRouter(prefix="/tasks", tags=["tasks"], route_class=DishkaRoute)


@router.get("/{task_id}/testcases/all")
async def get_task_cases(task_id: int):
    return {}  # пока что не храним сами задачи


@router.get("/{task_id}/testcases/only_visible")
async def get_task_visible_cases(task_id: int):
    return {}


@router.post("/{task_id}/testcases")
async def create_test_case(task_id: int):
    ...


@router.put("/{task_id}/testcases/{testcase_id}")
async def edit_test_case(task_id: int, testcase_id: int):
    ...


@router.get("/{task_id}/testcases/{testcase_id}")
async def get_test_case(task_id: int, testcase_id: int):
    ...


@router.delete("/{task_id}/testcases/{testcase_id}")
async def delete_test_case(task_id: int, testcase_id: int):
    ...


@router.get("/{task_id}")
async def get_task():
    ...


@router.post("/{task_id}")
async def create_task():
    ...


@router.put("/{task_id}")
async def edit_task():
    ...


@router.delete("/{task_id}")
async def delete_task():
    ...
