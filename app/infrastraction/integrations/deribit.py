import aiohttp

from app.models.price import TickerEnum
from settings import DerbitConfig


class DeribitClient:
    BASE_URL = DerbitConfig.BASE_URL
    TIMEOUT = DerbitConfig.TIMEOUT
    TICKERS = DerbitConfig.TICKERS

    async def get_index_price(self, ticker: TickerEnum) -> float:
        currency = self.TICKERS[ticker]
        url = f"{self.BASE_URL}/get_index_price?currency={currency}"
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.TIMEOUT)) as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data["result"]["index_price"]
