from pydantic import BaseModel, Field

from .submission import Submission


class Judge0Config(BaseModel):
    source_code: str
    language_id: int

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
    def from_submission_create(cls, submission: Submission, **overrides):
        base_data = submission.model_dump()
        base_data.update(overrides)
        return cls(**base_data)
