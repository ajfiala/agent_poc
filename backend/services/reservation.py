import logging
from datetime import datetime
from typing import List, Optional

from backend.db.repositories.guest import GuestRepository
from backend.db.repositories.room import RoomRepository
from backend.db.repositories.reservation import ReservationRepository
from backend.schemas.guest import GuestSchema
from backend.schemas.room import RoomSchema
from backend.schemas.reservation import ReservationSchema

logger = logging.getLogger(__name__)

class ReservationService:
    """
    A service layer class for managing reservations, 
    orchestrating Guest, Room, and Reservation repositories.
    
    Exposed methods (AI-agent friendly):
    - create_reservation(...)
    - get_reservations_for_guest(...)
    - modify_reservation(...)
    - cancel_reservation(...)
    """

    def __init__(self, db):
        self.db = db
        self.guest_repo = GuestRepository(db=db)
        self.room_repo = RoomRepository(db=db)
        self.reservation_repo = ReservationRepository(db=db)

    async def create_reservation(
        self,
        guest: GuestSchema,
        room_type: str,
        check_in: datetime,
        check_out: datetime
    ) -> ReservationSchema:
        """
        Creates a new reservation for a given guest, room type, 
        and date range, returning a ReservationSchema.
        
        Steps:
        1) If guest doesn't exist, create them.
        2) Find an available room of the specified type.
        3) Create the reservation record.
        4) Mark the room as unavailable if needed.
        """

        try:
            existing_guest = await self.guest_repo.get_guest_by_id(guest.guest_id)
        except ValueError:
            existing_guest = await self.guest_repo.create_guest(guest)

        available_rooms = await self.room_repo.list_available_rooms_by_type(room_type)
        if not available_rooms:
            raise ValueError(f"No available {room_type} rooms for the requested date range.")

        selected_room = available_rooms[0]  # For simplicity, pick the first available

        # 3) Create the reservation
        new_reservation = ReservationSchema(
            guest_id=existing_guest.guest_id,
            room_id=selected_room.room_id,
            check_in=check_in,
            check_out=check_out,
            status="booked"
        )
        created_reservation = await self.reservation_repo.create_reservation(new_reservation)

        return created_reservation

    async def get_reservations_for_guest(self, guest_id: int) -> List[ReservationSchema]:
        """
        Return all reservations for the specified guest ID.
        """
        return await self.reservation_repo.list_reservations_by_guest_id(guest_id)

    async def modify_reservation(
        self,
        reservation_id: int,
        check_in: Optional[datetime] = None,
        check_out: Optional[datetime] = None,
        room_type: Optional[str] = None
    ) -> ReservationSchema:
        """
        Modify an existing reservation, allowing new check_in, check_out, or room_type.

        Steps:
        1) If room_type is changing, find an available room of that type.
        2) Call the repository's update_reservation with the relevant fields.
        3) If we changed room_id, mark the old room as available, and the new one as unavailable (for real system).
        We'll do a simpler approach here for demonstration.
        """

        # 1) If the user wants to change room_type, pick a new available room
        new_room_id = None
        if room_type is not None:
            # find an available room of that type
            available_rooms = await self.room_repo.list_available_rooms_by_type(room_type)
            if not available_rooms:
                raise ValueError(f"No available {room_type} rooms for the requested date range.")
            new_room = available_rooms[0]
            new_room_id = new_room.room_id

        # 2) Update the reservation with new check_in/check_out/room_id
        updated = await self.reservation_repo.update_reservation(
            reservation_id=reservation_id,
            new_check_in=check_in,
            new_check_out=check_out,
            new_room_id=new_room_id
        )

        return updated


    async def cancel_reservation(self, reservation_id: int) -> bool:
        """
        Cancels (deletes) an existing reservation from the database.
        Returns True if successful.
        """
        res = await self.reservation_repo.delete_reservation(reservation_id)

        if not res:
            raise ValueError(f"Reservation with id={reservation_id} not found")
        
        return True