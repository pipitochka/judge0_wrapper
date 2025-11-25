from pydantic import BaseModel

from persistent.models import TestCaseType


class TaskDto(BaseModel):
    id: int
    title: str
    content: str | None
    type: TestCaseType


class CreateTaskDto(BaseModel):
    title: str
    content: str | None = None
    type: TestCaseType


class UpdateTaskDto(BaseModel):
    title: str | None = None
    content: str | None = None
    type: TestCaseType | None = None


class TestCaseDto(BaseModel):
    id: int
    stdin: str | None = None
    expected: str

    time_limit: float | None = None
    memory_limit: int | None = None

    is_hidden: bool = True
    task_id: int


class CreateTestCaseDto(BaseModel):
    stdin: str | None = None
    expected: str

    time_limit: float | None = None
    memory_limit: int | None = None

    is_hidden: bool = True


class UpdateTestCaseDto(BaseModel):
    stdin: str | None = None
    expected: str | None = None

    time_limit: float | None = None
    memory_limit: int | None = None

    is_hidden: bool | None = None
