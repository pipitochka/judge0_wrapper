from typing import AsyncIterable

from dishka import Provider, Scope, provide

from config import app_settings
from persistent import Database
from repositories import TaskRepository, TestCaseRepository
from services import Judge0Service


class AppProvider(Provider):
    def __init__(self, database_url: str):
        self._db = Database(database_url)
        super().__init__()

    @provide(scope=Scope.APP)
    def provide_judge0_service(self) -> Judge0Service:
        return Judge0Service(
            f"http://{app_settings.judge0.host}:{app_settings.judge0.port}",
            header=app_settings.judge0.authn_header,
            token=app_settings.judge0.authn_token
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
