"""Application settings."""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    # Database
    postgres_user: str = "user"
    postgres_password: str = "password"
    postgres_db: str = "db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # Application
    app_name: str = "Usuarios API"
    app_version: str = "1.0.0"
    debug: bool = True

    @property
    def database_url(self) -> str:
        """Get database connection URL."""
        return (
            f"postgresql+psycopg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
