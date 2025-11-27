from pydantic import BaseModel, Field

from config import app_settings
from .submission import CreateSubmissionSchema, CreateRunTestDtoSchema
from .task import TestCaseDto


class Judge0SubmissionSchema(BaseModel):
    source_code: str
    language_id: str

    stdin: str | None = None
    expected_output: str | None = None
    compiler_options: str | None = None
    command_line_arguments: str | None = None

    cpu_time_limit: float = Field(default=2.0, ge=0.1, le=15.0)
    cpu_extra_time: float = Field(default=0.5, ge=0.0, le=5.0)
    wall_time_limit: float = Field(default=5.0, ge=1.0, le=30.0)
    memory_limit: int = Field(default=128000, ge=8000, le=512000)  # 128MB
    stack_limit: int = Field(default=64000, ge=8000, le=256000)  # 64MB
    max_processes_and_or_threads: int = Field(default=60, ge=1, le=100)
    enable_per_process_and_thread_time_limit: bool = False
    enable_per_process_and_thread_memory_limit: bool = False
    max_file_size: int = Field(default=1024, ge=0, le=8192)  # 1MB
    redirect_stderr_to_stdout: bool = False
    enable_network: bool = False  # сеть отключена
    number_of_runs: int = Field(default=1, ge=1, le=3)
    additional_files: str | None = None
    callback_url: str | None = None

    @classmethod
    def from_submission_schema(cls, submission_schema: CreateRunTestDtoSchema):
        return Judge0SubmissionSchema(
            source_code=submission_schema.answer,
            language_id=submission_schema.language_id,
            stdin=submission_schema.stdin,
            compiler_options=None,
            command_line_arguments=None,
            callback_url=app_settings.get_callback_url_for_judge0()
        )

    @classmethod
    def from_testcase(cls, tc: TestCaseDto, submission_schema: CreateSubmissionSchema) -> "Judge0SubmissionSchema":
        return Judge0SubmissionSchema(
            source_code=submission_schema.answer,
            language_id=submission_schema.language_id,
            stdin=tc.stdin,
            compiler_options=None,
            command_line_arguments=None,
            cpu_time_limit=tc.time_limit or 2,
            memory_limit=tc.memory_limit or 128000,
            expected_output=tc.expected,
            callback_url=app_settings.get_callback_url_for_judge0()
        )


class Judge0StatusDto(BaseModel):
    id: int
    description: str


class Judge0SubmissionResultDto(BaseModel):
    # представление ответа judge0
    token: str

    stdout: str | None
    stderr: str | None

    message: str | None
    compile_output: str | None

    memory: int | None
    time: str | None

    status: Judge0StatusDto
