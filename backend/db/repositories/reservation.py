# backend/db/repositories/reservation.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime

from backend.schemas.reservation import ReservationSchema
from backend.db.models import Reservation

class ReservationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_reservations(self) -> list[ReservationSchema]:
        """
        Fetch all reservations from the database and return them
        as a list of ReservationSchema.
        """
        result = await self.db.execute(select(Reservation))
        rows = result.scalars().all()

        return [ReservationSchema.model_validate(r) for r in rows]

    async def list_reservations_by_guest_id(self, guest_id: int) -> list[ReservationSchema]:
        """
        Fetch all reservations for a specific guest from the database and return them
        as a list of ReservationSchema.
        """
        result = await self.db.execute(
            select(Reservation).where(Reservation.guest_id == guest_id)
        )
        rows = result.scalars().all()

        return [ReservationSchema.model_validate(r) for r in rows]

    
    async def create_reservation(self, reservation: ReservationSchema) -> ReservationSchema:
        """
        Create a new reservation in the database. 
        - Checks date ranges (check_in < check_out).
        - Checks if there is no overlap for the same room for the given date range.
        """

        # 1. Validate check_in < check_out
        if reservation.check_in >= reservation.check_out:
            raise ValueError("check_in must be before check_out")

        # 2. Check for overlapping reservations
        overlap_stmt = (
            select(Reservation)
            .where(
                (Reservation.room_id == reservation.room_id),
                (Reservation.check_in < reservation.check_out),
                (Reservation.check_out > reservation.check_in),
            )
        )
        overlap_result = await self.db.execute(overlap_stmt)
        overlapping = overlap_result.scalars().first()
        if overlapping:
            raise ValueError(
                f"Room {reservation.room_id} is already booked for the specified date range."
            )

        # 3. Create a SQLAlchemy model object from the Pydantic schema
        new_reservation = Reservation(
            guest_id=reservation.guest_id,
            room_id=reservation.room_id,
            check_in=reservation.check_in,
            check_out=reservation.check_out,
            status=reservation.status,
            # created_at / updated_at may be auto-set by the DB, so no need to specify here.
        )

        # 4. Insert into the DB
        self.db.add(new_reservation)
        await self.db.commit()
        await self.db.refresh(new_reservation)

        # 5. Convert the saved SQLAlchemy model back to a Pydantic schema
        return ReservationSchema.model_validate(new_reservation)