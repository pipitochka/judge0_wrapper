from sqlalchemy import select

from persistent.models import Task, TestCase
from .base import BaseRepository


class TaskRepository(BaseRepository):
    async def create_task(self):
        ...

    async def get_testcases(self, task_id: int) -> list:
        q = select(TestCase).where(TestCase.task_id == task_id)
