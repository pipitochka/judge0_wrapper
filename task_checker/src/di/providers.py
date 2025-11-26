from typing import AsyncIterable

from dishka import Provider, Scope, provide

from config import app_settings
from persistent import Database
from repositories import TaskRepository, TestCaseRepository, SubmissionRepository
from services import Judge0Service, SubmissionService


class AppProvider(Provider):
    def __init__(self, database_url: str):
        self._db = Database(database_url)
        super().__init__()

    @provide(scope=Scope.REQUEST)
    def provide_judge0_service(self, tc_repo: TestCaseRepository, sm_repo: SubmissionRepository) -> Judge0Service:
        return Judge0Service(
            url=f"http://{app_settings.judge0.host}:{app_settings.judge0.port}",
            header=app_settings.judge0.authn_header,
            token=app_settings.judge0.authn_token,
            testcases_repo=tc_repo,
            submission_repo=sm_repo
        )

    @provide(scope=Scope.APP)
    def provide_db(self) -> Database:
        return self._db

    @provide(scope=Scope.REQUEST)
    async def provide_task_repository(self, db: Database) -> AsyncIterable[TaskRepository]:
        async with db.session() as session:
            yield TaskRepository(session)

    @provide(scope=Scope.REQUEST)
    async def provide_testcase_repository(self, db: Database) -> AsyncIterable[TestCaseRepository]:
        async with db.session() as session:
            yield TestCaseRepository(session)

    @provide(scope=Scope.REQUEST)
    async def provide_submission_repository(self, db: Database) -> AsyncIterable[SubmissionRepository]:
        async with db.session() as session:
            yield SubmissionRepository(session)

    @provide(scope=Scope.REQUEST)
    async def provide_submission_service(
            self, task_repo: TaskRepository,
            testcases_repo: TestCaseRepository,
            submission_repo: SubmissionRepository,
            judge0_service: Judge0Service
    ) -> SubmissionService:
        return SubmissionService(
            task_repo, testcases_repo, submission_repo, judge0_service
        )
