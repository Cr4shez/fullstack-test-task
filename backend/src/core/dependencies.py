from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import get_settings
from src.core.database import SessionLocal
from src.domain.use_cases import FileUseCases, AlertUseCases
from src.infrastructure.repositories import FileRepository, AlertRepository
from src.infrastructure.storage import LocalStorage
from src.infrastructure.task_scheduler.celery import CeleryTaskScheduler


async def get_session():
    async with SessionLocal() as db:
        yield db


def get_task_scheduler():
    return CeleryTaskScheduler()


def get_storage(settings=Depends(get_settings)):
    return LocalStorage(settings)


def get_file_repository(session=Depends(get_session)):
    return FileRepository(session)


def get_alert_repository(session=Depends(get_session)):
    return AlertRepository(session)


def get_file_service(
    session=Depends(get_session),
    repo=Depends(get_file_repository),
    tasker=Depends(get_task_scheduler),
    storage=Depends(get_storage)
):
    return FileUseCases(session=session, repo=repo, tasker=tasker, storage=storage)


def get_alert_service(
    session=Depends(get_session),
    file_repo=Depends(get_file_repository),
    alert_repo=Depends(get_alert_repository)
):
    return AlertUseCases(session=session, file_repo=file_repo, alert_repo=alert_repo)


SessionDep = Annotated[AsyncSession, Depends(get_session)]
FileRepoDep = Annotated[FileRepository, Depends(get_file_repository)]
AlertRepoDep = Annotated[AlertRepository, Depends(get_alert_repository)]
FileServiceDep = Annotated[FileUseCases, Depends(get_file_service)]
AlertServiceDep = Annotated[AlertUseCases, Depends(get_alert_service)]
TaskSchedulerDep = Annotated[CeleryTaskScheduler, Depends(get_task_scheduler)]
StorageDep = Annotated[LocalStorage, Depends(get_storage)]
