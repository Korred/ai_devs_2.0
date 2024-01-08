from typing import Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pydantic import AnyHttpUrl, PostgresDsn, computed_field, validator
from functools import cached_property

# Load environment variables from .env file
load_dotenv()


# Define Settings class
class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DB_HOSTNAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    DB_NAME: str

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    ALLOWED_HOSTS: str | list[str] = ["localhost", "127.0.0.1"]

    @computed_field
    @cached_property
    def DB_URI(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.DB_USER,
                password=self.DB_PASSWORD,
                host=self.DB_HOSTNAME,
                port=self.DB_PORT,
                path=self.DB_NAME,
            )
        )

    @validator("ALLOWED_HOSTS", pre=True)
    def parse_allowed_hosts(cls, v: Union[str, list[str]]) -> list[str]:
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def parse_backend_cors_origins(cls, v: Union[str, list[str]]) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow", case_sensitive=True
    )


# Use a global instance of Settings that can be used by other modules
settings: Settings = Settings()
