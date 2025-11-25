import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from auth import add_jwt_auth_middleware
from di import setup_di
from persistent import Database
from routers import add_routers
from exceptions import init_exception_handlers
from config import app_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = app.state.dishka_container
    db: Database = await container.get(Database)
    await db.check_and_create_tables()
    yield
    await app.state.dishka_container.close()


async def create_app():
    app = FastAPI(title="Task Checker", root_path="/api", lifespan=lifespan)

    setup_di(app)
    add_jwt_auth_middleware(app)
    init_exception_handlers(app)
    add_routers(app)

    @app.get("/health")
    async def check_server_health() -> bool:
        return True


    return app


async def main():
    app = await create_app()

    server = uvicorn.Server(
        uvicorn.Config(
            app,
            host=app_settings.uvicorn.host,
            port=app_settings.uvicorn.port,
            workers=app_settings.uvicorn.workers
        )
    )
    await server.serve()


asyncio.run(main())
