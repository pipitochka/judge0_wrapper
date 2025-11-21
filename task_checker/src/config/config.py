import multiprocessing

from pydantic_settings import BaseSettings


class UvicornSettings(BaseSettings):
    host: str = "localhost"
    port: int = 8000
    workers: int = multiprocessing.cpu_count()


class AuthSettings(BaseSettings):
    jwt_secret: str = "asdf"
    jwt_algorithm: str = "HS256"


class Judge0Settings(BaseSettings):
    judge0_authn_header: str = "X-Auth-Token"
    judge0_authn_token: str = "other_mega_secret_token"
    judge0_host: str = "localhost"
    judge0_port: int = 2358


class AppSettings(BaseSettings):
    uvicorn: UvicornSettings = UvicornSettings()
    auth: AuthSettings = AuthSettings()
    judge0: Judge0Settings = Judge0Settings()


app_settings = AppSettings()
