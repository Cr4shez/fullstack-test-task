import uuid

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app import app
from src.core.config import get_settings
from src.core.dependencies import get_session
from src.infrastructure.models import Base
from tests.factories import _create_file, _create_alert


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(get_settings().database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(engine):
    async_session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session_factory() as session:
        yield session

        await session.rollback()
        await session.close()


@pytest.fixture(scope="function")
async def client(test_settings, db_session):
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_settings] = lambda: test_settings
    app.dependency_overrides[get_session] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()




@pytest.fixture
async def file_dep(db_session: AsyncSession):
    dto, db_obj = _create_file(stored_name=str(uuid.uuid4()))
    db_session.add(db_obj)
    await db_session.flush()
    return dto


@pytest.fixture
async def ten_files_dep(db_session: AsyncSession):
    dtos, objs = [], []
    for _ in range(10):
        dto, obj = _create_file(stored_name=str(uuid.uuid4()))
        dtos.append(dto)
        objs.append(obj)
    db_session.add_all(objs)
    await db_session.flush()
    return dtos


@pytest.fixture
async def alert_dep(db_session: AsyncSession, file_dep):
    dto, db_obj = _create_alert(file_id=file_dep.id)
    db_session.add(db_obj)
    await db_session.flush()
    return dto


@pytest.fixture
async def ten_alerts_dep(db_session: AsyncSession, ten_files_dep):
    dtos, objs = [], []
    for file in ten_files_dep:
        dto, obj = _create_alert(file_id=file.id)
        dtos.append(dto)
        objs.append(obj)
    db_session.add_all(objs)
    await db_session.flush()
    return dtos
