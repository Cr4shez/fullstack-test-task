from unittest.mock import MagicMock, AsyncMock

import pytest

from src.app import app
from src.core.config import Settings
from src.core.dependencies import get_task_scheduler, get_storage


class TestSettings(Settings):
    @property
    def database_url(self) -> str:
        return "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def test_settings():
    return TestSettings()


@pytest.fixture
def mock_scheduler():
    mock = MagicMock()
    app.dependency_overrides[get_task_scheduler] = lambda: mock

    yield mock

    if get_task_scheduler in app.dependency_overrides:
        del app.dependency_overrides[get_task_scheduler]


@pytest.fixture
def mock_storage():
    mock = AsyncMock()
    app.dependency_overrides[get_storage] = lambda: mock

    yield mock

    if get_storage in app.dependency_overrides:
        del app.dependency_overrides[get_storage]


@pytest.fixture
def eager_scheduler():
    from src.core.celery_config import celery_app
    default_eager = celery_app.conf.task_always_eager
    default_propagate = celery_app.conf.task_eager_propagates

    celery_app.conf.task_always_eager = True
    celery_app.conf.task_eager_propagates = True
    yield
    celery_app.conf.task_always_eager = default_eager
    celery_app.conf.task_eager_propagates = default_propagate
