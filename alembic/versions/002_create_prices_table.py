"""create prices table

Revision ID: 002
Revises: 001
Create Date: 2026-01-15 20:53:59.351956

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]


# revision identifiers, used by Alembic.
revision: str = "002"
down_revision: Union[str, Sequence[str], None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(  # pylint: disable=no-member
        "prices",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("ticker", sa.Enum("BTC_USD", "ETH_USD", name="ticker_enum"), nullable=False),
        sa.Column("price", sa.Numeric(precision=18, scale=8), nullable=False),
        sa.Column("created_at", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("prices")  # pylint: disable=no-member
