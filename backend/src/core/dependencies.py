from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import SessionLocal
from src.domain.use_cases import FileUseCases, AlertUseCases
from src.infrastructure.repositories import FileRepository, AlertRepository
from src.infrastructure.storage import LocalStorage
from src.infrastructure.task_scheduler.celery import CeleryTaskScheduler


async def get_session():
    async with SessionLocal() as db:
        yield db


async def get_task_scheduler():
    return CeleryTaskScheduler()


async def get_storage():
    return LocalStorage()


async def get_file_repository(session=Depends(get_session)):
    return FileRepository(session)


async def get_alert_repository(session=Depends(get_session)):
    return AlertRepository(session)


async def get_file_service(
    repo=Depends(get_file_repository),
    tasker=Depends(get_task_scheduler),
    storage=Depends(get_storage)
):
    return FileUseCases(repo=repo, tasker=tasker, storage=storage)


async def get_alert_service(
    file_repo=Depends(get_file_repository),
    alert_repo=Depends(get_alert_repository)
):
    return AlertUseCases(file_repo=file_repo, alert_repo=alert_repo)


SessionDep = Annotated[AsyncSession, Depends(get_session)]
FileRepoDep = Annotated[FileRepository, Depends(get_file_repository)]
AlertRepoDep = Annotated[AlertRepository, Depends(get_alert_repository)]
FileServiceDep = Annotated[FileUseCases, Depends(get_file_service)]
AlertServiceDep = Annotated[AlertUseCases, Depends(get_alert_service)]
TaskSchedulerDep = Annotated[CeleryTaskScheduler, Depends(get_task_scheduler)]
StorageDep = Annotated[LocalStorage, Depends(get_storage)]
