from functools import lru_cache
from pathlib import Path

from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", ".env.dev"))

    celery_broker_url: str
    db_echo: bool = False

    postgres_scheme: str = "postgresql+asyncpg"
    postgres_user: str
    postgres_password: str
    postgres_host: str
    pgport: int
    postgres_db: str

    base_dir: Path = Path(__file__).resolve().parent.parent
    max_file_size: int = 15 * 1024 * 1024  # 15 mb

    @computed_field
    @property
    def database_url(self) -> str:
        return str(
            MultiHostUrl.build(
                scheme=self.postgres_scheme,
                username=self.postgres_user,
                password=self.postgres_password,
                host=self.postgres_host,
                port=self.pgport,
                path=self.postgres_db,
            )
        )

    @property
    def storage_dir(self) -> Path:
        return self.base_dir / "storage" / "files"


@lru_cache
def get_settings():
    return Settings()
