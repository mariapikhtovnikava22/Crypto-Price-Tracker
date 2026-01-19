from typing import Sequence

from pydantic import BaseModel, Field

from app.models.price import TickerEnum


class PriceResponse(BaseModel):
    ticker: TickerEnum = Field(..., description="Тикер валютной пары")
    price: float = Field(..., description="Цена валюты")
    created_at: int = Field(..., description="Время получения цены в UNIX timestamp")

    class Config:
        from_attributes = True


class PricesListResponse(BaseModel):
    items: Sequence[PriceResponse] = Field(..., description="Список цен по валюте")
