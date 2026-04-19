"""Добавление уникальности полю email

Revision ID: 00624346862c
Revises: f1432e8737de
Create Date: 2026-04-18 21:03:25.702717

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "00624346862c"
down_revision: Union[str, Sequence[str], None] = "f1432e8737de"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
