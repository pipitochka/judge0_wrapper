from sqlalchemy import select

from persistent.models import Task
from schemas.task import (
    TaskDto, CreateTaskDto, UpdateTaskDto,
)
from .base import BaseRepository


class TaskRepository(BaseRepository):
    async def create_task(self, data: CreateTaskDto) -> TaskDto:
        task = Task(
            title=data.title,
            content=data.content,
            type=data.type
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return TaskDto(
            id=task.id,
            title=task.title,
            content=task.content,
            type=task.type
        )

    async def get_task(self, task_id: int) -> TaskDto | None:
        q = select(Task).where(Task.id == task_id)
        result = await self.session.execute(q)
        task = result.scalar_one_or_none()

        if task is None:
            return None

        return TaskDto(
            id=task.id,
            title=task.title,
            content=task.content,
            type=task.type
        )

    async def update_task(self, task_id: int, data: UpdateTaskDto) -> TaskDto | None:
        q = select(Task).where(Task.id == task_id)
        result = await self.session.execute(q)
        task = result.scalar_one_or_none()
        if task is None:
            return None

        if data.title is not None:
            task.title = data.title
        if data.content is not None:
            task.content = data.content
        if data.type is not None:
            task.type = data.type

        await self.session.commit()
        await self.session.refresh(task)
        return TaskDto(
            id=task.id,
            title=task.title,
            content=task.content,
            type=task.type
        )

    async def delete_task(self, task_id: int) -> bool:
        q = select(Task).where(Task.id == task_id)
        result = await self.session.execute(q)
        task = result.scalar_one_or_none()
        if task is None:
            return False

        await self.session.delete(task)
        await self.session.commit()
        return True
