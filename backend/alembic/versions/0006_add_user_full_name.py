"""Add full name to users.

Revision ID: 0006_add_user_full_name
Revises: 0005_reward_unique
"""

from alembic import op
import sqlalchemy as sa


revision = "0006_add_user_full_name"
down_revision = "0005_reward_unique"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("full_name", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "full_name")
