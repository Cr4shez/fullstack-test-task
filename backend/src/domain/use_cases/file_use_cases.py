import asyncio
import mimetypes
from pathlib import Path
from typing import Optional, TYPE_CHECKING
from uuid import uuid4

from src.domain import get_base_metadata, get_text_metadata, get_pdf_metadata, analyze_file_security
from src.domain.schemas import FileUploadStatus
from src.domain.schemas import FileDTO, FileCreateDTO
from src.domain.exceptions import FileMissingError

if TYPE_CHECKING:
    from src.infrastructure.repositories.file_repository import FileRepository
    from src.infrastructure.storage import LocalStorage
    from src.infrastructure.task_scheduler.celery import CeleryTaskScheduler


class FileUseCases:
    SCAN_STATUS_BAD = "suspicious"
    SCAN_STATUS_OK = "clean"
    SCAN_DETAILS_EMPTY = "no threats found"
    DEFAULT_CONTENT_TYPE = "application/octet-stream"

    def __init__(
        self,
        repo: FileRepository,
        tasker: CeleryTaskScheduler,
        storage: LocalStorage
    ):
        self.repo = repo
        self.task_scheduler = tasker
        self.storage = storage

    async def scan_for_threats(self, file_id: str) -> Optional[FileDTO]:
        """Сценарий проверки безопасности файла."""
        file_dto = await self.repo.find_by_id(file_id)
        if not file_dto:
            raise FileMissingError(file_id)

        await self.repo.update(file_id, FileDTO(processing_status=FileUploadStatus.PROCESSING))

        reasons = analyze_file_security(file_dto)

        return await self.repo.update(file_id, FileDTO(
            scan_status=self.SCAN_STATUS_BAD if reasons else self.SCAN_STATUS_OK,
            scan_details=", ".join(reasons) if reasons else self.SCAN_DETAILS_EMPTY,
            requires_attention=bool(reasons),
            processing_status=FileUploadStatus.PROCESSED
        ))

    async def extract_metadata(self, file_id: str) -> Optional[FileDTO]:
        """Сценарий извлечения метаданных из содержимого файла."""
        file_dto = await self.repo.find_by_id(file_id)
        if not file_dto:
            raise FileMissingError(file_id)

        path = file_dto.absolute_path
        metadata = get_base_metadata(file_dto)

        if file_dto.mime_type.startswith("text/"):
            content = await asyncio.to_thread(path.read_text, "utf-8", "ignore")
            metadata.update(get_text_metadata(content))

        elif file_dto.mime_type == "application/pdf":
            content = await asyncio.to_thread(path.read_bytes)
            metadata.update(get_pdf_metadata(content))

        return await self.repo.update(file_id, FileDTO(metadata_json=metadata))

    async def process_file(self, file_id: str) -> None:
        file_dto = await self.repo.find_by_id(file_id)
        if not file_dto:
            raise FileMissingError(file_id)
        self.task_scheduler.schedule_file_analysis(file_id)

    async def create_file_and_schedule_scan(self, file_dto: FileDTO) -> FileDTO:
        _file = file_dto.file
        title = file_dto.title

        file_id = str(uuid4())
        suffix = Path(_file.filename or "").suffix
        file_name = f"{file_id}{suffix}"
        content = await file_dto.file.read()
        saved_file = await self.storage.write_file(file_name, content)

        created_file = await self.repo.create(FileCreateDTO(
            id=file_id,
            original_name=_file.filename or file_name,
            title=title,
            stored_name=file_name,
            mime_type=_file.content_type or mimetypes.guess_type(file_name)[0] or self.DEFAULT_CONTENT_TYPE,
            size=saved_file.size,
            processing_status=FileUploadStatus.UPLOADED
        ))
        self.task_scheduler.schedule_file_analysis(file_id)
        return created_file

    async def update_file(self, file_id: str, dto: FileDTO) -> FileDTO:
        return await self.repo.update(id=file_id, schema=dto)

    async def get_file(self, file_id: str) -> Optional[FileDTO]:
        return await self.repo.find_by_id(file_id)

    async def delete_file(self, file_id: str) -> bool:
        return await self.repo.delete(file_id)
