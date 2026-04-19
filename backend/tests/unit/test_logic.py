import pytest

from src.domain.logic import (
    get_pdf_metadata, get_text_metadata, get_base_metadata, analyze_file_security, determine_file_alert
)
from src.domain.schemas import FileProcessingStatus
from src.domain.schemas.enums import AlertLevel
from tests.factories import create_file_dto


pytestmark = pytest.mark.unit

@pytest.mark.parametrize("name, size, mime, reason_count", [
    ("1", 500, "", 1),
    ("1.txt", 500, "text/plain", 0),
    ("1.exe", 500, "application/x-msdownload", 1),
    ("1.pdf", 500, "image/png", 1),
    ("1.txt", 11 * 1024 * 1024, "text/plain", 1),
    ("1.sh", 15 * 1024 * 1024, "text/x-sh", 2),
])
def test_analyze_file_security(name, size, mime, reason_count):
    file = create_file_dto(original_name=name, size=size, mime_type=mime)

    reasons = analyze_file_security(file)

    assert len(reasons) == reason_count


@pytest.mark.parametrize("status, requires_attention, scan_details, expected_level", [
    (FileProcessingStatus.FAILED, False, "", AlertLevel.CRITICAL),
    (FileProcessingStatus.PROCESSED, True, "Virus found", AlertLevel.WARNING),
    (FileProcessingStatus.PROCESSED, False, "", AlertLevel.INFO),
])
def test_determine_file_alert(status, requires_attention, scan_details, expected_level):
    file = create_file_dto(
        processing_status=status,
        requires_attention=requires_attention,
        scan_details=scan_details
    )
    alert = determine_file_alert(file)

    assert alert.level == expected_level


@pytest.mark.parametrize("name, size, mime, ext", [
    ("1.png", 1024, "image/png", ".png"),
    ("2.json", 0, "application/json", ".json"),
    ("3.zip", 50 * 1024, "application/zip", ".zip"),
])
def test_get_base_metadata(name, size, mime, ext):
    file = create_file_dto(original_name=name, size=size, mime_type=mime)
    metadata = get_base_metadata(file)
    assert metadata == {
        "extension": ext,
        "size_bytes": size,
        "mime_type": mime,
    }


@pytest.mark.parametrize("content, expected_lines, expected_chars", [
    ("", 0, 0),
    ("hello\nworld", 2, 11),
    ("one line", 1, 8),
])
def test_get_text_metadata(content, expected_lines, expected_chars):
    metadata = get_text_metadata(content)
    assert metadata["line_count"] == expected_lines
    assert metadata["char_count"] == expected_chars


@pytest.mark.parametrize("content, expected_pages", [
    (b"no page tags", 1),
    (b"/Type /Page /Type /Page", 2),
])
def test_get_pdf_metadata(content, expected_pages):
    metadata = get_pdf_metadata(content)
    assert metadata["approx_page_count"] == expected_pages
