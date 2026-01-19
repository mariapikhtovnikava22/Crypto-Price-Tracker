import asyncio
import logging

from app.di.prices_container import FetchPricesContainer
from celery_app import celery_app
from helpers.db_config import scoped_session


logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.fetch_prices.fetch_prices_task")
def fetch_prices_task():
    loop = asyncio.get_event_loop()

    async def main() -> None:
        container = FetchPricesContainer()
        service = await container.fetch_prices_service()

        await service.fetch_prices()
        scoped_session.remove()

    loop.run_until_complete(main())
