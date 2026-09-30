"""Allow DELIVERED status for help requests.

Revision ID: 0004_status_delivered
Revises: 0003_delivered_at
"""

from alembic import op


revision = "0004_status_delivered"
down_revision = "0003_delivered_at"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint(
        "help_requests_status_check",
        "help_requests",
        type_="check",
    )
    op.create_check_constraint(
        "help_requests_status_check",
        "help_requests",
        "status IN ('OPEN', 'ACCEPTED', 'IN_PROGRESS', 'DELIVERED', 'COMPLETED', 'CANCELLED', 'DISPUTED')",
    )


def downgrade() -> None:
    op.drop_constraint(
        "help_requests_status_check",
        "help_requests",
        type_="check",
    )
    op.create_check_constraint(
        "help_requests_status_check",
        "help_requests",
        "status IN ('OPEN', 'ACCEPTED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', 'DISPUTED')",
    )
