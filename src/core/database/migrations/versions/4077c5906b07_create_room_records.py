"""create_room_records

Revision ID: 4077c5906b07
Revises: b9468cc1e145
Create Date: 2026-06-07 19:40:48.889391

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4077c5906b07"
down_revision: Union[str, Sequence[str], None] = "b9468cc1e145"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Накат миграции."""

    rooms_table = sa.table(
        "rooms",
        sa.column("title", sa.String),
        sa.column("description", sa.String),
    )

    op.bulk_insert(
        rooms_table,
        [
            {
                "id": 1,
                "title": "Малый зал",
                "description": "Небольшая переговорная для 2-4 человек.",
            },
            {"id": 2, "title": "Большой зал", "description": None},
            {
                "id": 3,
                "title": "Комната отдыха",
                "description": "Зона для отдыха между встречами.",
            },
            {
                "id": 4,
                "title": "Серверная",
                "description": "Техническое помещение (не предназначено для бронирования).",
            },
            {
                "id": 5,
                "title": "Конференц-зал",
                "description": "Зал для проведения крупных мероприятий и вебинаров.",
            },
        ],
    )


def downgrade() -> None:
    """Откат миграции."""

    op.execute("""
            DELETE FROM rooms
            WHERE title IN (
                'Малый зал',
                'Большой зал',
                'Комната отдыха',
                'Серверная',
                'Конференц-зал'
            )
        """)
