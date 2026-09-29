"""Baseline existing SocietyAPP database schema.

This revision intentionally contains no DDL. The MVP schema was created
before Alembic was introduced. This revision lets Alembic track that
existing database state so future migrations can be incremental.
"""

from typing import Sequence, Union

from alembic import op


revision: str = "0001_baseline"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
