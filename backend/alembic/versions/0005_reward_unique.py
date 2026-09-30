"""Prevent duplicate rewards for one help request.

Revision ID: 0005_reward_unique
Revises: 0004_status_delivered
"""

from alembic import op
from sqlalchemy import text


revision = "0005_reward_unique"
down_revision = "0004_status_delivered"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        "uq_point_transactions_earn_help_request",
        "point_transactions",
        ["help_request_id"],
        unique=True,
        postgresql_where=text(
            "type = 'EARN' AND help_request_id IS NOT NULL"
        ),
    )


def downgrade() -> None:
    op.drop_index(
        "uq_point_transactions_earn_help_request",
        table_name="point_transactions",
    )
