import asyncio
import threading
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core.config import get_settings

_local = threading.local()

def get_worker_loop():
    if not hasattr(_local, "loop") or _local.loop.is_closed():
        _local.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_local.loop)
    return _local.loop

def run_async(coro):
    loop = get_worker_loop()
    return loop.run_until_complete(coro)


celery_engine = create_async_engine(
    get_settings().database_url,
    poolclass=NullPool
)

CelerySessionLocal = async_sessionmaker(
    bind=celery_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
