from fastapi import APIRouter, Request, Depends

from task_checker.src.auth import require_role, bearer_schema, require_login

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/{task_id}", dependencies=[Depends(bearer_schema)])
@require_login()
async def get_task_info(task_id: int, request: Request):
    user = request.state.user
    print(user)
    return "ok"
