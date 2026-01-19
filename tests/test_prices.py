import time
from unittest.mock import AsyncMock

import pytest

from app.models.price import Prices, TickerEnum
from app.services.fetch_prices_service import FetchPricesService
from app.services.price_service import PricesService
from exceptions.custom_exceptions import PriceNotFoundError, TaskDispatchError


@pytest.mark.asyncio
class TestPricesService:

    @pytest.fixture
    def prices_repository(self):
        return AsyncMock()

    @pytest.fixture
    def prices_uow(self, prices_repository):
        uow = AsyncMock()
        uow.__aenter__.return_value = uow
        uow.__aexit__.return_value = None
        uow.prices_repository = prices_repository
        return uow

    @pytest.fixture
    def prices_service(self, prices_uow):
        return PricesService(prices_uow)

    @pytest.mark.parametrize(
        "ticker, price_value",
        [
            (TickerEnum.BTC_USD, 50000),
            (TickerEnum.ETH_USD, 3300),
        ],
    )
    async def test_get_all_prices_by_ticker(self, prices_service, prices_repository, ticker, price_value):
        prices_list = [Prices(ticker=ticker, price=price_value, created_at=int(time.time()))]
        prices_repository.get_all_by_ticker.return_value = prices_list

        result = await prices_service.get_all_prices_by_ticker(ticker)
        assert result == prices_list
        prices_repository.get_all_by_ticker.assert_called_once_with(ticker)

    @pytest.mark.parametrize(
        "ticker, price_value",
        [
            (TickerEnum.BTC_USD, 50000),
            (TickerEnum.ETH_USD, 3300),
        ],
    )
    async def test_get_latest_price(self, prices_service, prices_repository, ticker, price_value):
        timestamp = int(time.time())
        price_obj = Prices(ticker=ticker, price=price_value, created_at=timestamp)
        prices_repository.get_latest_price.return_value = price_obj

        result = await prices_service.get_latest_price(ticker)
        assert result == price_obj
        prices_repository.get_latest_price.assert_called_once_with(ticker)

    @pytest.mark.parametrize("ticker", [TickerEnum.BTC_USD, TickerEnum.ETH_USD])
    async def test_get_latest_price_not_found(self, prices_service, prices_repository, ticker):
        prices_repository.get_latest_price.return_value = None
        with pytest.raises(PriceNotFoundError):
            await prices_service.get_latest_price(ticker)

    @pytest.mark.parametrize(
        "ticker, date_from, date_to",
        [
            (TickerEnum.BTC_USD, 1000, 2000),
            (TickerEnum.ETH_USD, 1000, 2000),
        ],
    )
    async def test_get_prices_by_period(self, prices_service, prices_repository, ticker, date_from, date_to):
        prices_list = [
            Prices(ticker=ticker, price=50000, created_at=date_from),
            Prices(ticker=ticker, price=51000, created_at=date_to),
        ]
        prices_repository.get_prices_by_period.return_value = prices_list

        result = await prices_service.get_prices_by_period(ticker, date_from, date_to)
        assert result == prices_list
        prices_repository.get_prices_by_period.assert_called_once_with(ticker, date_from, date_to)

    @pytest.mark.parametrize(
        "ticker, date_from, date_to",
        [
            (TickerEnum.BTC_USD, 1000, 2000),
            (TickerEnum.ETH_USD, 1000, 2000),
        ],
    )
    async def test_get_prices_by_period_not_found(self, prices_service, prices_repository, ticker, date_from, date_to):
        prices_repository.get_prices_by_period.return_value = []
        with pytest.raises(PriceNotFoundError):
            await prices_service.get_prices_by_period(ticker, date_from, date_to)


@pytest.mark.asyncio
class TestFetchPricesService:

    @pytest.fixture
    def prices_repository(self):
        return AsyncMock()

    @pytest.fixture
    def prices_uow(self, prices_repository):
        uow = AsyncMock()
        uow.__aenter__.return_value = uow
        uow.__aexit__.return_value = None
        uow.prices_repository = prices_repository
        return uow

    @pytest.fixture
    def deribit_client(self):
        client = AsyncMock()
        client.get_index_price.return_value = 12345.67
        client.close.return_value = None
        return client

    @pytest.fixture
    def fetch_prices_service(self, deribit_client, prices_uow):
        return FetchPricesService(
            client=deribit_client, prices_uow=prices_uow, tickers=[TickerEnum.BTC_USD, TickerEnum.ETH_USD]
        )

    async def test_fetch_prices_creates_prices(self, fetch_prices_service, deribit_client, prices_uow):
        await fetch_prices_service.fetch_prices()
        assert deribit_client.get_index_price.call_count == 2
        assert prices_uow.prices_repository.create.call_count == 2
        deribit_client.close.assert_awaited_once()

    async def test_fetch_prices_raises_task_dispatch_error(self, fetch_prices_service, deribit_client):
        deribit_client.get_index_price.side_effect = Exception("Connection error")
        with pytest.raises(TaskDispatchError):
            await fetch_prices_service.fetch_prices()
        deribit_client.close.assert_awaited_once()
