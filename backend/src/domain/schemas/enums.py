import enum


class FileProcessingStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"

class AlertLevel(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class FileScanStatus(str, enum.Enum):
    PENDING = "pending"
    CLEAN = "clean"
    SUSPICIOUS = "suspicious"
