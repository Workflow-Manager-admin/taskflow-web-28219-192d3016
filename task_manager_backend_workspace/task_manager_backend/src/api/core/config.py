from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Configuration for FastAPI app and DB."""

    PROJECT_NAME: str = "Task Manager API"
    DATABASE_URL: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/taskmanager",
        env="DATABASE_URL"
    )
    SECRET_KEY: str = Field(default="supersecret", env="SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
