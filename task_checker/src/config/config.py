import multiprocessing

from pydantic_settings import BaseSettings, SettingsConfigDict


class UvicornSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="UVICORN_")
    
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = multiprocessing.cpu_count()


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AUTH_")
    
    jwt_secret: str = "change_me_in_production"
    jwt_algorithm: str = "HS256"


class Judge0Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="JUDGE0_")
    
    authn_header: str = "X-Auth-Token"
    authn_token: str = "change_me_in_production"
    host: str = "localhost"
    port: int = 2358


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")

    host: str = "db_host"
    port: int = 5432
    name: str = "db"
    user: str = "username"
    password: str = "pwd"

    def get_database_url(self, debug: bool) -> str:
        if debug:
            return f"sqlite+aiosqlite:///./{self.name}.db"
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    debug: bool = True

    uvicorn: UvicornSettings = UvicornSettings()
    auth: AuthSettings = AuthSettings()
    judge0: Judge0Settings = Judge0Settings()
    database: DatabaseSettings = DatabaseSettings()

    def get_database_url(self) -> str:
        return self.database.get_database_url(self.debug)


app_settings = AppSettings()
