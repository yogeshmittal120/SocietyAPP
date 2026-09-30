"""Add accepted_by_id to help_requests.

Revision ID: 0002_add_help_request_accepted_by
Revises: 0001_baseline
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0002_add_help_request_accepted_by"
down_revision: Union[str, Sequence[str], None] = "0001_baseline"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "help_requests",
        sa.Column("accepted_by_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_help_requests_accepted_by_id_users",
        "help_requests",
        "users",
        ["accepted_by_id"],
        ["id"],
    )
    op.create_index(
        "ix_help_requests_accepted_by_id",
        "help_requests",
        ["accepted_by_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_help_requests_accepted_by_id", table_name="help_requests")
    op.drop_constraint(
        "fk_help_requests_accepted_by_id_users",
        "help_requests",
        type_="foreignkey",
    )
    op.drop_column("help_requests", "accepted_by_id")
