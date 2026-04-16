from pathlib import Path

from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", ".env.dev"))

    celery_broker_url: str
    db_echo: bool = False

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    base_dir: Path = Path(__file__).resolve().parent.parent
    max_file_size: int = 15 * 1024 * 1024  # 15 mb

    @computed_field
    @property
    def database_url(self) -> str:
        return str(
            MultiHostUrl.build(
                scheme="postgresql+asyncpg",
                username=self.postgres_user,
                password=self.postgres_password,
                host=self.postgres_host,
                port=self.postgres_port,
                path=self.postgres_db,
            )
        )

    @property
    def storage_dir(self) -> Path:
        return self.base_dir / "storage" / "files"


settings = Settings()
