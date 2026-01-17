import time
from typing import Optional, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastraction.repositories.price_repository import PricesRepository
from app.models.price import Prices, TickerEnum
from exceptions.custom_exceptions import PriceNotFoundError
from helpers.db_config import get_session


class PricesService:
    def __init__(self, db: AsyncSession):
        self.prices_repository = PricesRepository(db)

    async def create_price(self, ticker: TickerEnum, price: float) -> Prices:
        timestamp = int(time.time())
        return await self.prices_repository.create(ticker=ticker, price=price, created_at=timestamp)

    async def get_all_prices_by_ticker(self, ticker: TickerEnum) -> Sequence[Prices]:
        return await self.prices_repository.get_all_by_ticker(ticker)

    async def get_latest_price(self, ticker: TickerEnum) -> Optional[Prices]:
        price = await self.prices_repository.get_latest_price(ticker)
        if not price:
            raise PriceNotFoundError(f"No prices found for ticker {ticker}")
        return price

    async def get_prices_by_period(
        self, ticker: TickerEnum, date_from: Optional[int] = None, date_to: Optional[int] = None
    ) -> Sequence[Prices]:
        if date_from and date_to and date_from > date_to:
            raise ValueError("Date_from cannot be greater than date_to")
        prices = await self.prices_repository.get_prices_by_period(ticker, date_from, date_to)
        if not prices:
            raise PriceNotFoundError("No prices found for given period")

        return prices


async def get_prices_service(db=Depends(get_session)):
    return PricesService(db)
