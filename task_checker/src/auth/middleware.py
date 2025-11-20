from logging import getLogger

from fastapi import Request, Response, status, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from .providers import UserProvider

logger = getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            user_provider: UserProvider,
    ):
        super().__init__(app)
        self.user_provider = user_provider

    async def dispatch(
            self,
            request: Request,
            call_next: RequestResponseEndpoint,
    ) -> Response:
        try:
            user = await self.user_provider.get_user(request)
        except HTTPException as exc:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": exc.detail},
            )

        request.state.user = user
        return await call_next(request)
