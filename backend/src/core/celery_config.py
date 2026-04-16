from celery import Celery

from pydantic_settings import BaseSettings, SettingsConfigDict


class CelerySettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", ".env.dev"))

    broker: str = "redis://backend-redis:6379/0"
    backend: str = "redis://backend-redis:6379/0"


celery_settings = CelerySettings()

celery_app = Celery(__name__, broker=celery_settings.broker, backend=celery_settings.backend)
celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)
celery_app.autodiscover_tasks(["src"])
