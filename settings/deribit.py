from app.models.price import TickerEnum
from settings.base import env


class DerbitConfig:
    BASE_URL = env("DERIBIT_BASE_URL", default="https://www.deribit.com/api/v2/public")
    TICKERS = {TickerEnum.BTC_USD: "BTC", TickerEnum.ETH_USD: "ETH"}
    POLL_INTERVAL: int = int(env("DERIBIT_POLL_INTERVAL", default=60))
    TIMEOUT: int = int(env("DERIBIT_TIMEOUT", default=10))
