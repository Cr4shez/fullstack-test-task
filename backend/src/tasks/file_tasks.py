
from src.core.celery_config import celery_app
from src.core.database import  CelerySessionLocal
from src.domain.use_cases import FileUseCases, AlertUseCases
from src.infrastructure.repositories import FileRepository, AlertRepository
from src.infrastructure.storage import LocalStorage
from src.infrastructure.task_scheduler.celery import CeleryTaskScheduler
from src.tasks.base import run_async


"""celery does not work with fastapi DI and I hate to break the whole system here. should use taskiq."""
@celery_app.task
def scan_file_for_threats(file_id: str) -> str:
    async def run() -> str:
        async with CelerySessionLocal() as session:
            service = FileUseCases(FileRepository(session), CeleryTaskScheduler(), LocalStorage())
            await service.scan_for_threats(file_id)
        return file_id
    return run_async(run())


@celery_app.task
def extract_file_metadata(file_id: str) -> str:
    async def run() -> str:
        async with CelerySessionLocal() as session:
            service = FileUseCases(FileRepository(session), CeleryTaskScheduler(), LocalStorage())
            await service.extract_metadata(file_id)
        return file_id
    return run_async(run())


@celery_app.task
def send_file_alert(file_id: str) -> str:
    async def run() -> str:
        async with CelerySessionLocal() as session:
            service = AlertUseCases(file_repo=FileRepository(session), alert_repo=AlertRepository(session))
            await service.create_file_alert(file_id)
        return file_id
    return run_async(run())
