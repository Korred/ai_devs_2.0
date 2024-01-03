from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Define Settings class
class Settings(BaseSettings):
    openai_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )


# Use a global instance of Settings that can be used by other modules
settings = Settings()
