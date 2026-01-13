from typing import Optional, Sequence

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.price import Prices, TickerEnum


class PricesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, ticker: TickerEnum, price: float, created_at: int) -> Prices:
        instance = Prices(ticker=ticker, price=price, created_at=created_at)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get_all_by_ticker(self, ticker: TickerEnum) -> Sequence[Prices]:
        stmt = select(Prices).where(Prices.ticker == ticker)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_latest_price(self, ticker: TickerEnum) -> Optional[Prices]:
        stmt = select(Prices).where(Prices.ticker == ticker).order_by(desc(Prices.created_at)).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_prices_by_period(
        self, ticker: TickerEnum, date_from: Optional[int] = None, date_to: Optional[int] = None
    ) -> Sequence[Prices]:

        stmt = select(Prices).where(Prices.ticker == ticker)

        if date_from is not None:
            stmt = stmt.where(Prices.created_at >= date_from)
        if date_to is not None:
            stmt = stmt.where(Prices.created_at <= date_to)

        stmt = stmt.order_by(Prices.created_at)
        result = await self.session.execute(stmt)
        return result.scalars().all()
