import multiprocessing

from pydantic_settings import BaseSettings, SettingsConfigDict


class UvicornSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='UVICORN_')
    
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = multiprocessing.cpu_count()


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='AUTH_')
    
    jwt_secret: str = "change_me_in_production"
    jwt_algorithm: str = "HS256"


class Judge0Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='JUDGE0_')
    
    judge0_authn_header: str = "X-Auth-Token"
    judge0_authn_token: str = "change_me_in_production"
    judge0_host: str = "judge0-server"
    judge0_port: int = 2358


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    
    uvicorn: UvicornSettings = UvicornSettings()
    auth: AuthSettings = AuthSettings()
    judge0: Judge0Settings = Judge0Settings()


app_settings = AppSettings()
