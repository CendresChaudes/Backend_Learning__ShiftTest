"""create_slot_records

Revision ID: 3a60ac7c0612
Revises: 000458aa9b3e
Create Date: 2026-06-07 21:53:38.907594

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3a60ac7c0612"
down_revision: Union[str, Sequence[str], None] = "000458aa9b3e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Накат миграции."""

    slots_table = sa.table(
        "slots",
        sa.column("time", sa.String),
        sa.column("room_id", sa.Integer),
    )

    op.bulk_insert(
        slots_table,
        [
            {
                "id": 1,
                "room_id": 1,
                "time": "13:00-14:30",
            },
            {
                "id": 2,
                "room_id": 2,
                "time": "14:00-14:30",
            },
            {
                "id": 3,
                "room_id": 2,
                "time": "15:00-16:00",
            },
            {
                "id": 4,
                "room_id": 2,
                "time": "18:00-18:30",
            },
            {
                "id": 5,
                "room_id": 3,
                "time": "13:00-13:30",
            },
            {
                "id": 6,
                "room_id": 3,
                "time": "13:45-15:00",
            },
            {
                "id": 7,
                "room_id": 4,
                "time": "11:00-12:00",
            },
            {
                "id": 8,
                "room_id": 5,
                "time": "09:00-11:00",
            },
            {
                "id": 9,
                "room_id": 5,
                "time": "12:00-14:30",
            },
            {
                "id": 10,
                "room_id": 5,
                "time": "17:30-18:00",
            },
        ],
    )


def downgrade() -> None:
    """Откат миграции."""

    op.execute("""
            DELETE FROM slots
            WHERE id IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        """)
