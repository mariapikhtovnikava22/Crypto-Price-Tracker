import logging

import aiohttp

from app.models.price import TickerEnum
from settings import DerbitConfig


logger = logging.getLogger(__name__)


class DeribitClient:

    def __init__(self) -> None:
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=DerbitConfig.TIMEOUT))

    async def get_index_price(self, ticker: TickerEnum) -> float:
        currency = DerbitConfig.TICKERS[ticker]
        url = f"{DerbitConfig.BASE_URL}/get_index_price?index_name={currency}"
        logger.info(currency)
        async with self.session.get(url) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return data["result"]["index_price"]

    async def close(self):
        await self.session.close()
