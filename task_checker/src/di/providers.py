from dishka import Provider, Scope, provide

from config import app_settings
from services import Judge0Service


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_judge0_service(self) -> Judge0Service:
        return Judge0Service(
            f"http://{app_settings.judge0.host}:{app_settings.judge0.port}",
            header=app_settings.judge0.authn_header,
            token=app_settings.judge0.authn_token
        )
