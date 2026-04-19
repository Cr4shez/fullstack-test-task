import uuid

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.domain.schemas import FileCreateDTO, AlertCreateDTO
from src.infrastructure.models import StoredFile, Alert
from src.infrastructure.repositories import FileRepository, AlertRepository
from tests.factories import create_file_dto, create_alert_dto


@pytest.mark.asyncio
async def test_file_mapping_persistence(db_session):
    domain_file = create_file_dto(
        title="test_file.pdf",
        size=2048,
        mime_type="application/pdf"
    )

    create_dto = FileCreateDTO(
        title=domain_file.title,
        original_name=domain_file.title,
        stored_name=domain_file.title,
        mime_type=domain_file.mime_type,
        size=domain_file.size,
    )
    repo = FileRepository(db_session)
    await repo.create(create_dto)

    result = await db_session.execute(
        select(StoredFile).filter_by(title="test_file.pdf")
    )
    db_model = result.scalar_one()

    assert db_model.title == domain_file.title
    assert db_model.size == domain_file.size
    assert db_model.mime_type == domain_file.mime_type
    assert db_model.id == create_dto.id


@pytest.mark.asyncio
async def test_alert_mapping_persistence(db_session, file_dep):
    domain_alert = create_alert_dto(file_id=file_dep.id)
    repo = AlertRepository(db_session)
    created_alert = await repo.create(AlertCreateDTO(**domain_alert.model_dump()))

    result = await db_session.execute(
        select(Alert).filter_by(id=created_alert.id)
    )
    db_model = result.scalar_one()

    assert db_model.file_id == domain_alert.file_id
    assert db_model.level == domain_alert.level
    assert db_model.message == domain_alert.message
    assert isinstance(db_model.id, int)

    incorrect_alert = create_alert_dto(file_id=str(uuid.uuid4()))
    with pytest.raises(IntegrityError):
        await repo.create(AlertCreateDTO(**incorrect_alert.model_dump()))
