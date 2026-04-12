"""Create table hotels

Revision ID: bb2c11c081b0
Revises:
Create Date: 2026-04-08 19:49:32.722429

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "bb2c11c081b0"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_hotels_id"), "hotels", ["id"], unique=False)

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_hotels_id"), table_name="hotels")
    op.drop_table("hotels")
