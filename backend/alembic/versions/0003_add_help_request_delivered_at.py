"""Add delivered_at to help_requests.

Revision ID: 0003_add_help_request_delivered_at
Revises: 0002_add_help_request_accepted_by
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0003_add_help_request_delivered_at"
down_revision: Union[str, Sequence[str], None] = "0002_add_help_request_accepted_by"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "help_requests",
        sa.Column("delivered_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("help_requests", "delivered_at")
