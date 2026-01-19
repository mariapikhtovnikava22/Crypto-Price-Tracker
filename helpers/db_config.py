from asyncio import current_task

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, async_sessionmaker, create_async_engine

from settings import DbConfig


async_engine = create_async_engine(
    DbConfig.CONNECTION_SETTINGS["dsn"],
    echo=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=60.0,
)
async_session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

scoped_session = async_scoped_session(async_session, scopefunc=current_task)


def get_async_scoped_session() -> AsyncSession:
    return scoped_session()


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session
