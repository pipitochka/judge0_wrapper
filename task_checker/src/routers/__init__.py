from fastapi import FastAPI

from .information import router as info_router
from .submissions import router as submissions_router
from .tasks import router as tasks_router

routers = [
    info_router,
    submissions_router,
    tasks_router
]


def add_routers(app: FastAPI):
    for r in routers:
        app.include_router(r)
