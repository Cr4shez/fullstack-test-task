from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from .dependencies import get_settings


engine = create_async_engine(
    get_settings().database_url,
    echo=get_settings().db_echo,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)
