from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.models.price import TickerEnum
from app.services.price_service import PricesService, get_prices_service
from web.api.prices.schemas import PriceResponse, PricesListResponse


router = APIRouter(
    prefix="/prices",
    tags=["Prices"],
)


@router.get("/prices_by_ticker", response_model=PricesListResponse)
async def get_all_prices_by_ticker(
    ticker: TickerEnum = Query(..., description="Тикер валютной пары"),
    prices_service: PricesService = Depends(get_prices_service),
) -> PricesListResponse:
    prices = await prices_service.get_all_prices_by_ticker(ticker)
    return PricesListResponse(items=prices)


@router.get("/latest_price_by_ticker", response_model=PriceResponse)
async def get_latest_price_by_ticker(
    ticker: TickerEnum = Query(..., description="Тикер валютной пары"),
    prices_service: PricesService = Depends(get_prices_service),
) -> Optional[PriceResponse]:

    return await prices_service.get_latest_price(ticker)


@router.get("/period", response_model=PricesListResponse)
async def get_prices_by_period(
    ticker: TickerEnum = Query(..., description="Тикер валютной пары"),
    date_from: int | None = Query(None, description="Начало периода (UNIX timestamp)"),
    date_to: int | None = Query(None, description="Конец периода (UNIX timestamp)"),
    prices_service: PricesService = Depends(get_prices_service),
) -> PricesListResponse:
    prices = await prices_service.get_prices_by_period(
        ticker=ticker,
        date_from=date_from,
        date_to=date_to,
    )
    return PricesListResponse(items=prices)
