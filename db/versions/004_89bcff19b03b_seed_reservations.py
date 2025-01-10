"""seed_reservations

Revision ID: 89bcff19b03b
Revises: 0003_seed_guests
Create Date: 2025-01-10 12:46:47.732043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89bcff19b03b'
down_revision: Union[str, None] = '0003_seed_guests'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    reservations = [
        (1, 101, '2025-01-15', '2025-01-20', 'confirmed'),
        (2, 102, '2025-01-16', '2025-01-21', 'confirmed'),
        (3, 103, '2025-01-17', '2025-01-22', 'confirmed'),
        (4, 104, '2025-01-18', '2025-01-23', 'confirmed'),
        (5, 105, '2025-01-19', '2025-01-24', 'confirmed'),
        (6, 106, '2025-01-20', '2025-01-25', 'confirmed'),
        (7, 107, '2025-01-21', '2025-01-26', 'confirmed'),
        (8, 108, '2025-01-22', '2025-01-27', 'confirmed'),
        (9, 109, '2025-01-23', '2025-01-28', 'confirmed'),
        (10, 110, '2025-01-24', '2025-01-29', 'confirmed'),
    ]

    for (guest_id, room_id, check_in, check_out, status) in reservations:
        stmt = sa.text(
            """
            INSERT INTO reservations (guest_id, room_id, check_in, check_out, status)
            VALUES (:guest_id, :room_id, :check_in, :check_out, :status)
            """
        ).bindparams(guest_id=guest_id, room_id=room_id, check_in=check_in, check_out=check_out, status=status)
        op.execute(stmt)


def downgrade():
    op.execute("DELETE FROM reservations WHERE guest_id <= 10")
