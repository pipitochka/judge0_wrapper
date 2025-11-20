from fastapi import FastAPI

from task_checker.src.config import app_settings

from .bearer_schema import bearer_schema
from .permissions import require_role, require_login, require_permissions
from .middleware import AuthMiddleware
from .providers import JWTUserProvider, ExternalServiceUserProvider


def add_jwt_auth_middleware(app: FastAPI):
    provider = JWTUserProvider(
        app_settings.auth.jwt_secret,
        app_settings.auth.jwt_algorithm
    )
    app.add_middleware(AuthMiddleware, user_provider=provider)
