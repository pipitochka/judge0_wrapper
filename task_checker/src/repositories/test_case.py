from sqlalchemy import select

from persistent.models import TestCase
from schemas.task import (
    TestCaseDto, CreateTestCaseDto, UpdateTestCaseDto
)
from .base import BaseRepository


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

        return TestCaseDto.from_sqlalchemy(testcase)

    async def create_testcases(self, task_id: int, data: list[CreateTestCaseDto]) -> list[TestCaseDto]:
        result = []
        for tc in data:
            testcase = TestCase(
                stdin=tc.stdin,
                expected=tc.expected,
                time_limit=tc.time_limit,
                memory_limit=tc.memory_limit,
                is_hidden=tc.is_hidden,
                task_id=task_id
            )
            result.append(testcase)
            self.session.add(testcase)

        await self.session.commit()
        for tc in result:
            await self.session.refresh(tc)

        return [
            TestCaseDto.from_sqlalchemy(tc)
            for tc in result
        ]

    async def get_testcase(self, task_id: int, testcase_id: int) -> TestCaseDto | None:
        q = select(TestCase).where(
            TestCase.id == testcase_id,
            TestCase.task_id == task_id
        )
        result = await self.session.execute(q)
        testcase = result.scalar_one_or_none()
        if testcase is None:
            return None

        return TestCaseDto.from_sqlalchemy(testcase)

    async def get_testcases(self, task_id: int, only_open: bool = False) -> list[TestCaseDto]:
        q = select(TestCase).where(TestCase.task_id == task_id)
        if only_open:
            q = q.where(
                TestCase.is_hidden == False
            )

        result = await self.session.execute(q)
        testcases = result.scalars().all()
        return [
            TestCaseDto.from_sqlalchemy(tc)
            for tc in testcases
        ]

    async def get_visible_testcases(self, task_id: int) -> list[TestCaseDto]:
        q = select(TestCase).where(
            TestCase.task_id == task_id,
            TestCase.is_hidden.is_(False)
        )
        result = await self.session.execute(q)
        testcases = result.scalars().all()
        return [
            TestCaseDto.from_sqlalchemy(tc)
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

        return TestCaseDto.from_sqlalchemy(testcase)

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
