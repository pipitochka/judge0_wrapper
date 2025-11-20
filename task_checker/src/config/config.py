import multiprocessing

from pydantic_settings import BaseSettings


class UvicornSettings(BaseSettings):
    host: str = "localhost"
    port: int = 8000
    workers: int = multiprocessing.cpu_count()


class AuthSettings(BaseSettings):
    jwt_secret: str = "asdf"
    jwt_algorithm: str = "HS256"


class AppSettings(BaseSettings):
    uvicorn: UvicornSettings = UvicornSettings()
    auth: AuthSettings = AuthSettings()


app_settings = AppSettings()
