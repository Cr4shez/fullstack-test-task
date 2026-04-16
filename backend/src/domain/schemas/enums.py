import enum


class FileUploadStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    FAILED = "failed"
    PROCESSING = "processing"
    PROCESSED = "processed"
