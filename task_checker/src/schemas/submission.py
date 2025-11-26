from pydantic import BaseModel, Field, field_validator

from persistent.models import Submission, SubmissionResult


class CreateSubmissionSchema(BaseModel):
    task_id: int
    answer: str = Field(..., min_length=1, max_length=100000, description="Source code or answer")
    language_id: str

    stdin: str | None = Field(default=None, max_length=10000, description="stdin")
    compiler_options: str | None = Field(default=None, max_length=512, description="Compiler options")
    command_line_arguments: str | None = Field(default=None, max_length=512, description="CMD args")

    @field_validator("answer")
    def validate_source_code(cls, v):
        if len(v.strip()) == 0:
            raise ValueError("Source code cannot be empty")
        return v

    @field_validator("compiler_options")
    def validate_compiler_options(cls, v):
        if v and len(v) > 512:
            raise ValueError("Compiler options too long")
        return v

    @field_validator("command_line_arguments")
    def validate_command_line_args(cls, v):
        if v and len(v) > 512:
            raise ValueError("Command line arguments too long")
        return v


class SubmissionJudge0Schema(BaseModel):
    token: str

    stdout: str | None
    stderr: str | None

    message: str | None
    compile_output: str | None

    status: str | None
    accepted: bool

    memory_used: str
    time_used: str

    @classmethod
    def from_json(cls, data: dict) -> "SubmissionJudge0Schema":
        return cls(
            token=data["token"],
            stdout=data["stdout"],
            stderr=data["stderr"],
            message=data["message"],
            compile_output=data["compile_output"],
            status=data["status"]["description"],
            accepted=data["status"]["description"] == "Accepted",
            memory_used=data["memory"],
            time_used=data["time"]
        )


class TestCaseResultDto(BaseModel):
    stdin: str | None
    stdout: str | None
    stderr: str | None
    expected_answer: str | None

    message: str | None
    compile_output: str | None

    status: str | None

    used_memory: int
    used_time: str

    @classmethod
    def from_sqlalchemy(
            cls,
            data: SubmissionResult,
            stdin: str,
            expected_answer: str
    ) -> "TestCaseResultDto":
        return cls(
            stdin=stdin,
            stdout=data.stdout,
            stderr=data.stderr,
            expected_answer=expected_answer,
            message=data.message,
            compile_output=data.compile_output,
            status=data.status,
            used_memory=data.used_memory,
            used_time=data.used_time
        )


class SubmissionResultDto(BaseModel):
    id: int
    task_id: int
    status: str
    answer: str

    testcase_results: list[TestCaseResultDto] = []


class SubmissionGeneralSchema(BaseModel):
    id: int
    task_id: int
    answer: str

    @classmethod
    def from_sqlalchemy(cls, data: Submission) -> "SubmissionGeneralSchema":
        return cls(
            id=data.id,
            task_id=data.task_id,
            answer=data.answer
        )
