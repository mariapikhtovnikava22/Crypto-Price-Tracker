"""Add b-tree index to the ticker

Revision ID: 003
Revises: 002
Create Date: 2026-01-17 00:02:22.214770

"""

from typing import Sequence, Union

from alembic import op  # type: ignore[attr-defined]


revision: str = "003"
down_revision: Union[str, Sequence[str], None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index("idx_prices_ticker", "prices", ["ticker"], unique=False)  # pylint: disable=no-member


def downgrade() -> None:
    op.drop_index("idx_prices_ticker", table_name="prices")  # pylint: disable=no-member
