from typing import Any, Optional, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.repositories.price_repository import PricesRepository, get_prices_repository
from helpers.db_config import get_async_session


class PricesUnitOfWork:

    def __init__(self, prices_repo: PricesRepository, session: AsyncSession) -> None:
        self.prices_repository = prices_repo
        self._session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], tb: Any):
        if exc_type is None:
            await self._session.commit()
        else:
            await self._session.rollback()


async def get_prices_uow(
    prices_repo: PricesRepository = Depends(get_prices_repository), session: AsyncSession = Depends(get_async_session)
):
    return PricesUnitOfWork(prices_repo, session)
