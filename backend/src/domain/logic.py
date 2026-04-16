from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.schemas import FileDTO


class AlertInfo(NamedTuple):
    level: str
    message: str


def determine_file_alert(file: FileDTO) -> AlertInfo:
    if file.processing_status == "failed":
        return AlertInfo(level="critical", message="File processing failed")

    if file.requires_attention:
        return AlertInfo(
            level="warning",
            message=f"File requires attention: {file.scan_details}"
        )

    return AlertInfo(level="info", message="File processed successfully")


def analyze_file_security(file: FileDTO) -> list[str]:
    reasons = []
    if file.extension in {".exe", ".bat", ".cmd", ".sh", ".js"}:
        reasons.append(f"suspicious extension {file.extension}")
    if file.size > 10 * 1024 * 1024:
        reasons.append("file is larger than 10 MB")
    if file.extension == ".pdf" and file.mime_type not in {"application/pdf", "application/octet-stream"}:
        reasons.append("pdf extension does not match mime type")
    return reasons


def get_base_metadata(file: FileDTO) -> dict:
    return {
        "extension": file.extension,
        "size_bytes": file.size,
        "mime_type": file.mime_type,
    }


def get_text_metadata(content: str) -> dict:
    return {
        "line_count": len(content.splitlines()),
        "char_count": len(content)
    }


def get_pdf_metadata(content: bytes) -> dict:
    return {
        "approx_page_count": max(content.count(b"/Type /Page"), 1),
    }
