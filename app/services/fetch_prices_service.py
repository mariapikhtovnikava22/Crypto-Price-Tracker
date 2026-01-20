import logging
import time
from typing import Iterable

from app.infrastructure.integrations.deribit import DeribitClient
from app.infrastructure.uow.prices_unit_of_work import PricesUnitOfWork
from app.models.price import Prices, TickerEnum
from exceptions.custom_exceptions import TaskDispatchError


logger = logging.getLogger(__name__)


class FetchPricesService:
    def __init__(
        self,
        client: DeribitClient,
        prices_uow: PricesUnitOfWork,
        tickers: Iterable[TickerEnum],
    ) -> None:
        self.client = client
        self.uow = prices_uow
        self.tickers = tickers

    async def __create_price(self, ticker: TickerEnum, price: float) -> Prices:
        timestamp = int(time.time())
        async with self.uow as prices_uow:
            return await prices_uow.prices_repository.create(ticker=ticker, price=price, created_at=timestamp)

    async def fetch_prices(self) -> None:
        try:
            for ticker in self.tickers:
                price = await self.client.get_index_price(ticker)
                await self.__create_price(ticker, price)
        except Exception:
            logger.error("Fetch prices task failed")
            raise TaskDispatchError()
        finally:
            await self.client.close()
