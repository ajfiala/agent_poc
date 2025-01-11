from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.schemas.guest import GuestSchema
from backend.db.models import Guest 

class GuestRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_guests(self) -> list[GuestSchema]:
        """
        Fetch all guests from the database and return them
        as a list of GuestSchema.
        """
        result = await self.db.execute(select(Guest))
        rows = result.scalars().all()

        guest_schemas = [GuestSchema.model_validate(r) for r in rows]

        return guest_schemas
    
    async def get_guest_by_email(self, email: str) -> GuestSchema:
        """
        Fetch a guest by their email from the database
        and return it as a GuestSchema.
        """
        result = await self.db.execute(select(Guest).where(Guest.email == email))
        row = result.scalar_one_or_none()

        if row is None:
            raise ValueError(f"No guest found with email {email}")
        
        return GuestSchema.model_validate(row)
    
    async def create_guest(self, guest: GuestSchema) -> GuestSchema:
        """
        Create a new guest in the database
        and return it as a GuestSchema.
        """
        new_guest = Guest(**guest.model_dump())
        self.db.add(new_guest)
        await self.db.commit()
        await self.db.refresh(new_guest)
        
        return GuestSchema.model_validate(new_guest)
    
    async def delete_guest(self, email: int) -> bool:
        """
        Delete a guest by their email from the database.
        """
        result = await self.db.execute(select(Guest).where(Guest.email == email))
        row = result.scalar_one_or_none()

        if row is None:
            return False
        
        await self.db.delete(row)
        await self.db.commit()

        return True