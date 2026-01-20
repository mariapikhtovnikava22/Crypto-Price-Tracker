from typing import Optional, Sequence

from fastapi import Depends

from app.infrastructure.uow.prices_unit_of_work import PricesUnitOfWork, get_prices_uow
from app.models.price import Prices, TickerEnum
from exceptions.custom_exceptions import PriceNotFoundError


class PricesService:
    def __init__(self, prices_uow: PricesUnitOfWork) -> None:
        self.prices_uow = prices_uow

    async def get_all_prices_by_ticker(self, ticker: TickerEnum) -> Sequence[Prices]:
        async with self.prices_uow as uow:
            return await uow.prices_repository.get_all_by_ticker(ticker)

    async def get_latest_price(self, ticker: TickerEnum) -> Optional[Prices]:
        async with self.prices_uow as uow:
            price = await uow.prices_repository.get_latest_price(ticker)
            if not price:
                raise PriceNotFoundError(f"No prices found for ticker {ticker}")
            return price

    async def get_prices_by_period(
        self, ticker: TickerEnum, date_from: Optional[int] = None, date_to: Optional[int] = None
    ) -> Sequence[Prices]:
        if date_from and date_to and date_from > date_to:
            raise ValueError("Date_from cannot be greater than date_to")
        async with self.prices_uow as uow:
            prices = await uow.prices_repository.get_prices_by_period(ticker, date_from, date_to)
            if not prices:
                raise PriceNotFoundError("No prices found for given period")
            return prices


async def get_prices_service(price_uow: PricesUnitOfWork = Depends(get_prices_uow)):
    return PricesService(price_uow)
