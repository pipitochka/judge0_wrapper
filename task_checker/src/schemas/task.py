from pydantic import BaseModel

from persistent.models import TestCaseType


class TaskDto(BaseModel):
    id: int
    title: str
    content: str | None


class TestCaseDto(BaseModel):
    stdin: str | None = None
    expected: str

    type: TestCaseType

    time_limit: float | None = None
    memory_limit: int | None = None

    is_hidden: bool = True
