from functools import wraps
from typing import Callable, Any, Awaitable

from fastapi import Request, HTTPException, status

from schemas import UserSchema


def _extract_request_from_args(*args, **kwargs) -> Request:
    for arg in args:
        if isinstance(arg, Request):
            return arg
    for arg in kwargs.values():
        if isinstance(arg, Request):
            return arg
    raise RuntimeError(
        "Request not found in handler arguments. "
        "Add `request: Request` parameter to your route handler."
    )


def require_functions_factory(
    validator: Callable[[UserSchema | None, dict[str, Any]], Awaitable[None]] | Callable[[UserSchema | None, dict[str, Any]], None],
):
    def decorator_factory(**decorator_params: Any):
        def decorator(func: Callable[..., Awaitable[Any]]):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                request = _extract_request_from_args(*args, **kwargs)
                user: UserSchema | None = getattr(request.state, "user", None)

                result = validator(user, decorator_params)
                if callable(getattr(result, "__await__", None)):
                    await result

                return await func(*args, **kwargs)

            return wrapper

        return decorator

    return decorator_factory


def _login_validator(user: UserSchema | None, params: dict[str, Any]) -> None:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )


def _role_validator(user: UserSchema | None, params: dict[str, Any]) -> None:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    required_role: str = params["role"]
    if user.role != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )


def _permissions_validator(user: UserSchema | None, params: dict[str, Any]) -> None:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    required_permissions = params["permissions"]
    if set(required_permissions) != set(user.permissions):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )


_require_login_base = require_functions_factory(_login_validator)
_require_role_base = require_functions_factory(_role_validator)
_require_permission_base = require_functions_factory(_permissions_validator)


def require_login():
    return _require_login_base()


def require_role(role: str):
    return _require_role_base(role=role)


def require_permissions(permissions: list[str]):
    return _require_permission_base(permissions=permissions)
