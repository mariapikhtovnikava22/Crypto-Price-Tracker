import enum
import time
import uuid

from sqlalchemy import BigInteger, Column, Enum, Index, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta


Base: DeclarativeMeta = declarative_base()


class TickerEnum(str, enum.Enum):
    BTC_USD = "BTC_USD"
    ETH_USD = "ETH_USD"


class Prices(Base):
    __tablename__ = "prices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticker = Column(Enum(TickerEnum, name="ticker_enum"), nullable=False)
    price = Column(Numeric(precision=18, scale=8), nullable=False)
    created_at = Column(BigInteger, nullable=False, default=lambda: int(time.time()))

    __table_args__ = (Index("idx_prices_ticker", "ticker"),)
