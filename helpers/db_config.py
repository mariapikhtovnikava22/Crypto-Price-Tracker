from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from settings import DbConfig


async_engine = create_async_engine(
    DbConfig.CONNECTION_SETTINGS["dsn"],
    echo=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=60.0,
)
async_session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        except Exception as err:
            await session.rollback()
            raise err
        finally:
            await session.close()


async def get_session():
    async with get_async_session() as session:
        yield session
