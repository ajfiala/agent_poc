from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from typing import Optional

from backend.schemas.reservation import ReservationSchema
from backend.db.models import Reservation

class ReservationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_reservations(self) -> list[ReservationSchema]:
        result = await self.db.execute(select(Reservation))
        rows = result.scalars().all()
        return [ReservationSchema.model_validate(r) for r in rows]

    async def list_reservations_by_guest_id(self, guest_id: int) -> list[ReservationSchema]:
        result = await self.db.execute(
            select(Reservation).where(Reservation.guest_id == guest_id)
        )
        rows = result.scalars().all()
        return [ReservationSchema.model_validate(r) for r in rows]

    async def create_reservation(self, reservation: ReservationSchema) -> ReservationSchema:
        if reservation.check_in >= reservation.check_out:
            raise ValueError("check_in must be before check_out")

        new_reservation = Reservation(
            guest_id=reservation.guest_id,
            room_id=reservation.room_id,
            check_in=reservation.check_in,
            check_out=reservation.check_out,
            status=reservation.status,
        )
        self.db.add(new_reservation)
        await self.db.commit()
        await self.db.refresh(new_reservation)

        return ReservationSchema.model_validate(new_reservation)

    async def update_reservation(
        self,
        reservation_id: int,
        new_check_in: Optional[datetime] = None,
        new_check_out: Optional[datetime] = None,
        new_room_id: Optional[int] = None,
        new_status: Optional[str] = None
    ) -> ReservationSchema:
        """
        Dynamically update a reservation record with any of these new fields:
         - new_check_in
         - new_check_out
         - new_room_id
         - new_status
        """
        # 1) Fetch existing reservation
        result = await self.db.execute(
            select(Reservation).where(Reservation.reservation_id == reservation_id)
        )
        row = result.scalars().first()

        if not row:
            raise ValueError(f"Reservation with id={reservation_id} not found")

        # 2) Update whichever fields are provided
        if new_check_in is not None:
            if new_check_out is not None and new_check_in >= new_check_out:
                raise ValueError("check_in must be before check_out")
            row.check_in = new_check_in

        if new_check_out is not None:
            if new_check_in is not None and new_check_in >= new_check_out:
                raise ValueError("check_in must be before check_out")
            row.check_out = new_check_out

        if new_room_id is not None:
            row.room_id = new_room_id

        if new_status is not None:
            row.status = new_status

        # 3) Commit changes
        await self.db.commit()
        await self.db.refresh(row)

        print(f"Updated reservation: {ReservationSchema.model_validate(row)}")

        return ReservationSchema.model_validate(row)
    
    async def delete_reservation(self, reservation_id: int) -> bool:
        result = await self.db.execute(
            select(Reservation).where(Reservation.reservation_id == reservation_id)
        )
        row = result.scalars().first()

        if not row:
            print(f"Reservation with id={reservation_id} not found")
            return False

        print(f"\n\nrow: {ReservationSchema.model_validate(row)}\n\n")

        self.db.delete(row)

        await self.db.commit()

        return True