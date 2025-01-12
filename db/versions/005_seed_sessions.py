"""
005_seed_sessions

Revision ID: 0005_seed_sessions
Revises: 89bcff19b03b
Create Date: 2025-01-11

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0005_seed_sessions'
down_revision = '89bcff19b03b'
branch_labels = None
depends_on = None


def upgrade():
    """
    Seed 5 sessions, each linked to guest_id 1..5.
    """
    sessions = [
        1,
        2,
        3,
        4,
        5
    ]

    for guest_id in sessions:
        stmt = sa.text(
            """
            INSERT INTO sessions (guest_id)
            VALUES (:guest_id)
            """
        ).bindparams(guest_id=guest_id)
        op.execute(stmt)


def downgrade():
    """
    Remove only the sessions we added for guest_id 1..5.
    """
    op.execute(
        """
        DELETE FROM reservations;
        DELETE FROM messages;
        DELETE FROM sessions
        WHERE guest_id IN (1, 2, 3, 4, 5);
        """
    )
