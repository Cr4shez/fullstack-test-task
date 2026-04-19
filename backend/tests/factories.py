from src.domain.schemas import FileDTO, AlertDTO, FileProcessingStatus, FileCreateDTO, AlertCreateDTO
from src.domain.schemas.enums import FileScanStatus, AlertLevel
from src.infrastructure.models import StoredFile, Alert


def create_file_dto(**kwargs) -> FileDTO:
    defaults = {
        "title": "test_name.txt",
        "stored_name": "test_name.txt",
        "original_name": "test_name.txt",
        "mime_type": "text/plain",
        "size": 500,
        "processing_status": FileProcessingStatus.PROCESSED,
        "scan_status": FileScanStatus.CLEAN,
        "scan_details": None,
        "metadata_json": None,
        "requires_attention": False,
    }
    defaults.update(kwargs)
    return FileDTO(**defaults)


def create_alert_dto(**kwargs) -> AlertDTO:
    defaults = {
        "file_id": None,
        "level": AlertLevel.WARNING,
        "message": "warning",
    }
    defaults.update(kwargs)
    return AlertDTO(**defaults)



def _create_file(**kwargs):
    file_dto = create_file_dto(**kwargs)
    create_dto = FileCreateDTO(**file_dto.model_dump(exclude={"id"}))
    file_dto.id = create_dto.id
    return file_dto, StoredFile(**create_dto.model_dump())


def _create_alert(**kwargs):
    alert_dto = create_alert_dto(**kwargs)
    create_dto = AlertCreateDTO(**alert_dto.model_dump())
    return alert_dto, Alert(**create_dto.model_dump())
