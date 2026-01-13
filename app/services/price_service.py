import time
from typing import Optional, Sequence

from app.infrastraction.repositories.price_repository import PricesRepository
from app.models.price import Prices, TickerEnum


class PricesService:
    def __init__(self, repo: PricesRepository):
        self.prices_repository = repo

    async def create_price(self, ticker: TickerEnum, price: float) -> Prices:
        timestamp = int(time.time())
        return await self.prices_repository.create(ticker=ticker, price=price, created_at=timestamp)

    async def get_all_prices(self, ticker: TickerEnum) -> Sequence[Prices]:
        return await self.prices_repository.get_all_by_ticker(ticker)

    async def get_latest_price(self, ticker: TickerEnum) -> Optional[Prices]:
        return await self.prices_repository.get_latest_price(ticker)

    async def get_prices_by_period(
        self, ticker: TickerEnum, date_from: Optional[int] = None, date_to: Optional[int] = None
    ) -> Sequence[Prices]:
        if date_from and date_to and date_from > date_to:
            raise ValueError("date_from cannot be greater than date_to")
        return await self.prices_repository.get_prices_by_period(ticker, date_from, date_to)
