import asyncio
import logging

from app.infrastraction.integrations.deribit import DeribitClient
from app.services.price_service import PricesService
from celery_app import celery_app
from helpers.db_config import get_async_session
from settings.deribit import DerbitConfig


logger = logging.getLogger(__name__)


async def fetch_and_save_prices(client: DeribitClient):
    for ticker in DerbitConfig.TICKERS:
        try:
            price = await client.get_index_price(ticker)
            async with get_async_session() as db:
                service = PricesService(db)
                await service.create_price(ticker, price)
        except Exception as e:
            logger.error(f"Error when receiving the price {ticker}: {e}")


@celery_app.task(name="tasks.fetch_prices.fetch_prices_task")
def fetch_prices_task():
    loop = asyncio.get_event_loop()

    async def main():
        client = DeribitClient()
        try:
            await fetch_and_save_prices(client)
        finally:
            await client.close()

    loop.run_until_complete(main())
