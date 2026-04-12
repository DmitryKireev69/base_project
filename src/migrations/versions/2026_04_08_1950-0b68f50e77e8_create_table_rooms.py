"""Create table rooms

Revision ID: 0b68f50e77e8
Revises: bb2c11c081b0
Create Date: 2026-04-08 19:50:10.500863

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0b68f50e77e8"
down_revision: Union[str, Sequence[str], None] = "bb2c11c081b0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["hotel_id"], ["hotels.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_rooms_id"), "rooms", ["id"], unique=False)

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_rooms_id"), table_name="rooms")
    op.drop_table("rooms")
