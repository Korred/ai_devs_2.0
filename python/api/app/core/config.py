from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pydantic import AnyHttpUrl, PostgresDsn, computed_field
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
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

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

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow", case_sensitive=True
    )


# Use a global instance of Settings that can be used by other modules
settings: Settings = Settings()
