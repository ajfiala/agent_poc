
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.schemas.room import RoomSchema
from backend.db.models import Room 

class RoomRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_rooms(self) -> list[RoomSchema]:
        """
        Fetch all rooms from the database and return them
        as a list of RoomSchema.
        """
        result = await self.db.execute(select(Room))
        rows = result.scalars().all()

        # Convert each SQLAlchemy row to a RoomSchema
        room_schemas = [RoomSchema(
            room_id=r.room_id,
            room_number=r.room_number,
            room_type=r.room_type,
            rate=float(r.rate),
            available=r.available,
            created_at=r.created_at,
            updated_at=r.updated_at
        ) for r in rows]

        return room_schemas

    async def list_rooms_by_type(self, room_type: str) -> list[RoomSchema]:
        """
        Fetch rooms of a specific type from the database
        and return them as a list of RoomSchema.
        """
        result = await self.db.execute(select(Room).where(Room.room_type == room_type))
        rows = result.scalars().all()

        # Convert each SQLAlchemy row to a RoomSchema
        room_schemas = [RoomSchema(
            room_id=r.room_id,
            room_number=r.room_number,
            room_type=r.room_type,
            rate=float(r.rate),
            available=r.available,
            created_at=r.created_at,
            updated_at=r.updated_at
        ) for r in rows]

        return room_schemas

    async def get_room_by_room_number(self, room_number: str) -> RoomSchema:
        """
        Fetch a room by its room number from the database
        and return it as a RoomSchema.
        """
        result = await self.db.execute(select(Room).where(Room.room_number == room_number))
        row = result.scalar_one_or_none()

        if row is None:
            return None
        
        return RoomSchema(
            room_id=row.room_id,
            room_number=row.room_number,
            room_type=row.room_type,
            rate=float(row.rate),
            available=row.available,
            created_at=row.created_at,
            updated_at=row.updated_at
        )
    
    async def update_room_availability(self, room_number: str, available: bool) -> bool:
        """
        Update the availability of a room by its room number.
        """
        result = await self.db.execute(
            select(Room).where(Room.room_number == room_number)
        )
        row = result.scalar_one_or_none()

        if row is None:
            return False
        
        row.available = available
        
        await self.db.commit()

        return True
    