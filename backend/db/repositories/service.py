from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.schemas.service import ServiceSchema
from backend.db.models import Service 

class ServiceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_services(self) -> list[ServiceSchema]:
        """
        Fetch all rooms from the database and return them
        as a list of RoomSchema.
        """
        result = await self.db.execute(select(Service))
        rows = result.scalars().all()

        room_schemas = [ServiceSchema.model_validate(r) for r in rows]

        return room_schemas
    
    async def get_service_by_id(self, service_id: int) -> ServiceSchema:
        """
        Fetch a single service by its id and return it as a ServiceSchema.
        """
        result = await self.db.execute(select(Service).where(Service.service_id == service_id))
        row = result.scalars().first()

        service_schema = ServiceSchema.model_validate(row)

        return service_schema