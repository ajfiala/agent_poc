"""create_hotel_schema

Revision ID: 0001_hotel_schema
Revises: 
Create Date: 2025-01-08

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_hotel_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Ensure citext extension is available
    op.execute("CREATE EXTENSION IF NOT EXISTS citext")

    # guests
    op.create_table(
        'guests',
        sa.Column('guest_id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('full_name', sa.String(length=100), nullable=False),
        sa.Column('email', postgresql.CITEXT, unique=True),
        sa.Column('phone', sa.String(length=20)),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
    )

    # rooms
    # room_id is the room number
    op.create_table(
        'rooms',
        sa.Column('room_id', sa.BigInteger(), primary_key=True),
        sa.Column('room_type', sa.String(length=50), nullable=False),
        sa.Column('rate', sa.Numeric(10, 2), nullable=False),
        sa.Column('available', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
    )

    # reservations
    op.create_table(
        'reservations',
        sa.Column('reservation_id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('guest_id', sa.BigInteger(), sa.ForeignKey('guests.guest_id'), nullable=False),
        sa.Column('room_id', sa.BigInteger(), sa.ForeignKey('rooms.room_id'), nullable=False),
        sa.Column('check_in', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('check_out', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
    )

    # services
    op.create_table(
        'services',
        sa.Column('service_id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
    )

    # service_orders
    op.create_table(
        'service_orders',
        sa.Column('order_id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('reservation_id', sa.BigInteger(), sa.ForeignKey('reservations.reservation_id'), nullable=False),
        sa.Column('service_id', sa.BigInteger(), sa.ForeignKey('services.service_id'), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
    )


def downgrade():
    op.drop_table('service_orders')
    op.drop_table('services')
    op.drop_table('reservations')
    op.drop_table('rooms')
    op.drop_table('guests')
    op.execute("DROP EXTENSION IF EXISTS citext")

