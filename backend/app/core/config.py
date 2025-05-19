from pydantic import PostgresDsn, validator
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    SQLALCHEMY_DATABASE_URL: Optional[str] = None
    ASYNC_SQLALCHEMY_DATABASE_URL: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if v:
            return v
        # Формируем строку подключения вручную
        return f"postgresql://{values['DB_USER']}:{values['DB_PASSWORD']}@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"

    @validator("ASYNC_SQLALCHEMY_DATABASE_URL", pre=True)
    def assemble_async_db_connection(cls, v: Optional[str], values: dict) -> str:
        if v:
            return v
        return f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASSWORD']}@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()