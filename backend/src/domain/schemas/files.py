from pathlib import Path
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, field_validator

from src.core.config import settings
from src.domain.schemas import FileUploadStatus
from src.domain.schemas.mixins import TimestampSchemaMixin, partial


class FileCreateRequest(BaseModel):
    title: str
    file: UploadFile

    @field_validator("file")
    @classmethod
    def validate_file(cls, v: UploadFile):
        max_size = settings.max_file_size

        if v.size == 0:
            raise ValueError("Файл пуст")

        if v.size and v.size > max_size:
            raise ValueError(f"Файл слишком большой (макс. {max_size // 1024 // 1024}МБ)")

        return v


class FileUpdateRequest(BaseModel):
    title: str


class FileResponse(TimestampSchemaMixin, BaseModel):
    id: str
    title: str
    original_name: str
    mime_type: str
    size: int
    processing_status: FileUploadStatus
    requires_attention: bool = False
    scan_status: Optional[str] = None
    scan_details: Optional[str] = None


class FileBase(TimestampSchemaMixin, BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    stored_name: Optional[str] = None
    original_name: str
    mime_type: str
    size: int
    file: UploadFile
    processing_status: FileUploadStatus = FileUploadStatus.UPLOADED
    scan_status: str | None = None
    scan_details: str | None = None
    metadata_json: dict | None = None
    requires_attention: bool = False

    @property
    def extension(self) -> str:
        return Path(self.original_name).suffix.lower()

    @property
    def absolute_path(self) -> Path:
        return settings.storage_dir / self.stored_name


class FileCreateDTO(BaseModel):
    id: str
    title: str
    original_name: str
    stored_name: str
    mime_type: str
    size: int
    processing_status: FileUploadStatus = FileUploadStatus.UPLOADED


@partial
class FileDTO(FileBase):
    pass