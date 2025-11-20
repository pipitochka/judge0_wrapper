from abc import ABC, abstractmethod
from logging import getLogger

from fastapi import Request, status
from fastapi.exceptions import HTTPException
import jwt

from schemas import UserSchema

logger = getLogger(__name__)


class UserProvider(ABC):
    @abstractmethod
    async def get_user(self, request: Request) -> UserSchema | None:
        pass


class JWTUserProvider(UserProvider):
    def __init__(self, secret: str = None, algorithm: str = "HS256"):
        self._secret = secret
        self._algorithm = algorithm
        # по-хорошему надо использовать асимметричный алгоритм шифрования,
        # чтоб каждый микросервис мог проверить подлинность токена, не владея секретом

    async def get_user(self, request: Request) -> UserSchema | None:
        auth = request.headers.get("Authorization")
        if not auth:
            return

        if not auth.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing bearer token",
            )

        token = auth.removeprefix("Bearer ").strip()

        try:
            payload = jwt.decode(
                jwt=token,
                key=self._secret,
                algorithms=[self._algorithm],
            )
            user_id = payload["sub"]  # если поле sub не строка, то будет странная ошибка на этапе декода
            role = payload.get("role", "default")
            perms = payload.get("permissions", [])
            return UserSchema(id=user_id, role=role, permissions=perms)

        except jwt.PyJWTError as exc:
            logger.exception(exc)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        except Exception as exc:
            logger.exception(exc)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )


class ExternalServiceUserProvider(UserProvider):
    async def get_user(self, request: Request) -> UserSchema | None:
        raise NotImplementedError()  # если вдруг будет микросервис авторизации
