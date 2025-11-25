from sqlalchemy import select

from persistent.models import Task, TestCase
from schemas.task import (
    TaskDto, CreateTaskDto, UpdateTaskDto,
    TestCaseDto, CreateTestCaseDto, UpdateTestCaseDto
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


class TestCaseRepository(BaseRepository):
    async def create_testcase(self, task_id: int, data: CreateTestCaseDto) -> TestCaseDto:
        testcase = TestCase(
            stdin=data.stdin,
            expected=data.expected,
            time_limit=data.time_limit,
            memory_limit=data.memory_limit,
            is_hidden=data.is_hidden,
            task_id=task_id
        )
        self.session.add(testcase)
        await self.session.commit()
        await self.session.refresh(testcase)
        return TestCaseDto(
            id=testcase.id,
            stdin=testcase.stdin,
            expected=testcase.expected,
            time_limit=testcase.time_limit,
            memory_limit=testcase.memory_limit,
            is_hidden=testcase.is_hidden,
            task_id=testcase.task_id
        )

    async def get_testcase(self, task_id: int, testcase_id: int) -> TestCaseDto | None:
        q = select(TestCase).where(
            TestCase.id == testcase_id,
            TestCase.task_id == task_id
        )
        result = await self.session.execute(q)
        testcase = result.scalar_one_or_none()
        if testcase is None:
            return None
        return TestCaseDto(
            id=testcase.id,
            stdin=testcase.stdin,
            expected=testcase.expected,
            time_limit=testcase.time_limit,
            memory_limit=testcase.memory_limit,
            is_hidden=testcase.is_hidden,
            task_id=testcase.task_id
        )

    async def get_testcases(self, task_id: int) -> list[TestCaseDto]:
        q = select(TestCase).where(TestCase.task_id == task_id)
        result = await self.session.execute(q)
        testcases = result.scalars().all()
        return [
            TestCaseDto(
                id=tc.id,
                stdin=tc.stdin,
                expected=tc.expected,
                time_limit=tc.time_limit,
                memory_limit=tc.memory_limit,
                is_hidden=tc.is_hidden,
                task_id=tc.task_id
            )
            for tc in testcases
        ]

    async def get_visible_testcases(self, task_id: int) -> list[TestCaseDto]:
        q = select(TestCase).where(
            TestCase.task_id == task_id,
            TestCase.is_hidden == False
        )
        result = await self.session.execute(q)
        testcases = result.scalars().all()
        return [
            TestCaseDto(
                id=tc.id,
                stdin=tc.stdin,
                expected=tc.expected,
                time_limit=tc.time_limit,
                memory_limit=tc.memory_limit,
                is_hidden=tc.is_hidden,
                task_id=tc.task_id
            )
            for tc in testcases
        ]

    async def update_testcase(
        self, task_id: int, testcase_id: int, data: UpdateTestCaseDto
    ) -> TestCaseDto | None:
        q = select(TestCase).where(
            TestCase.id == testcase_id,
            TestCase.task_id == task_id
        )
        result = await self.session.execute(q)
        testcase = result.scalar_one_or_none()
        if testcase is None:
            return None

        if data.stdin is not None:
            testcase.stdin = data.stdin
        if data.expected is not None:
            testcase.expected = data.expected
        if data.time_limit is not None:
            testcase.time_limit = data.time_limit
        if data.memory_limit is not None:
            testcase.memory_limit = data.memory_limit
        if data.is_hidden is not None:
            testcase.is_hidden = data.is_hidden

        await self.session.commit()
        await self.session.refresh(testcase)
        return TestCaseDto(
            id=testcase.id,
            stdin=testcase.stdin,
            expected=testcase.expected,
            time_limit=testcase.time_limit,
            memory_limit=testcase.memory_limit,
            is_hidden=testcase.is_hidden,
            task_id=testcase.task_id
        )

    async def delete_testcase(self, task_id: int, testcase_id: int) -> bool:
        q = select(TestCase).where(
            TestCase.id == testcase_id,
            TestCase.task_id == task_id
        )
        result = await self.session.execute(q)
        testcase = result.scalar_one_or_none()
        if testcase is None:
            return False

        await self.session.delete(testcase)
        await self.session.commit()
        return True
