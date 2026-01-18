import time
from unittest.mock import AsyncMock

import pytest

from app.models.price import Prices, TickerEnum
from app.services.price_service import PricesService
from exceptions.custom_exceptions import PriceNotFoundError


@pytest.mark.asyncio
class TestPricesService:

    @pytest.fixture
    def prices_repository(self):
        return AsyncMock()

    @pytest.fixture
    def prices_service(self, prices_repository):
        return PricesService(prices_repository)

    @pytest.mark.parametrize(
        "ticker, price_value",
        [
            (TickerEnum.BTC_USD, 50000),
            (TickerEnum.ETH_USD, 3300),
        ],
    )
    async def test_create_price(self, prices_service, prices_repository, ticker, price_value):
        timestamp = int(time.time())
        price_obj = Prices(ticker=ticker, price=price_value, created_at=timestamp)

        prices_repository.create.return_value = price_obj

        result = await prices_service.create_price(ticker, price_value)

        assert result == price_obj
        prices_repository.create.assert_called_once_with(
            ticker=ticker, price=price_value, created_at=pytest.approx(timestamp, abs=1)
        )
        prices_repository.create.reset_mock()

    @pytest.mark.parametrize(
        "ticker, prices_list",
        [
            (
                TickerEnum.BTC_USD,
                [
                    Prices(ticker=TickerEnum.BTC_USD, price=50000, created_at=1),
                    Prices(ticker=TickerEnum.BTC_USD, price=50100, created_at=2),
                ],
            ),
            (
                TickerEnum.ETH_USD,
                [
                    Prices(ticker=TickerEnum.ETH_USD, price=3300, created_at=1),
                    Prices(ticker=TickerEnum.ETH_USD, price=3320, created_at=2),
                ],
            ),
        ],
    )
    async def test_get_all_prices_by_ticker(self, prices_service, prices_repository, ticker, prices_list):
        prices_repository.get_all_by_ticker.return_value = prices_list
        result = await prices_service.get_all_prices_by_ticker(ticker)

        assert result == prices_list
        prices_repository.get_all_by_ticker.assert_called_once_with(ticker)
        prices_repository.get_all_by_ticker.reset_mock()

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
        prices_repository.get_latest_price.reset_mock()

    @pytest.mark.parametrize(
        "ticker",
        [
            TickerEnum.BTC_USD,
            TickerEnum.ETH_USD,
        ],
    )
    async def test_get_latest_price_not_found(self, prices_service, prices_repository, ticker):
        prices_repository.get_latest_price.return_value = None

        with pytest.raises(PriceNotFoundError):
            await prices_service.get_latest_price(ticker)
        prices_repository.get_latest_price.reset_mock()

    @pytest.mark.parametrize(
        "ticker, date_from, date_to, prices_list",
        [
            (
                TickerEnum.BTC_USD,
                1000,
                2000,
                [
                    Prices(ticker=TickerEnum.BTC_USD, price=50000, created_at=1000),
                    Prices(ticker=TickerEnum.BTC_USD, price=51000, created_at=2000),
                ],
            ),
            (
                TickerEnum.ETH_USD,
                1000,
                2000,
                [
                    Prices(ticker=TickerEnum.ETH_USD, price=3300, created_at=1000),
                    Prices(ticker=TickerEnum.ETH_USD, price=3350, created_at=2000),
                ],
            ),
        ],
    )
    async def test_get_prices_by_period(
        self, prices_service, prices_repository, ticker, date_from, date_to, prices_list
    ):
        prices_repository.get_prices_by_period.return_value = prices_list

        result = await prices_service.get_prices_by_period(ticker, date_from, date_to)
        assert result == prices_list
        prices_repository.get_prices_by_period.assert_called_once_with(ticker, date_from, date_to)
        prices_repository.get_prices_by_period.reset_mock()

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
        prices_repository.get_prices_by_period.reset_mock()
