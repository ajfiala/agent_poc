from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from backend.schemas.service import ServiceOrderSchema
from backend.db.models import ServiceOrders 

class ServiceOrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_service_order_by_reservation_id(self, reservation_id: int) -> list[ServiceOrderSchema]:
        """
        Fetch all service order for a particular reservation from the database and return them
        """
        result = await self.db.execute(select(ServiceOrders).where(ServiceOrders.reservation_id == reservation_id))
        rows = result.scalars().all()
        if not rows:
            return []
        service_order_schemas = [ServiceOrderSchema.model_validate(r) for r in rows]

        return service_order_schemas

    async def get_service_order_by_order_id(self, order_id: int) -> ServiceOrderSchema:
        """
        Fetch a single service order by its id and return it as a ServiceOrderSchema.
        """
        result = await self.db.execute(select(ServiceOrders).where(ServiceOrders.order_id == order_id))
        row = result.scalars().first()
        if not row:
            return None
        service_order_schema = ServiceOrderSchema.model_validate(row)

        return service_order_schema
    
    async def create_service_order(self, service_order: ServiceOrderSchema) -> ServiceOrderSchema:
        """
        Create a new service order in the database and return it as a ServiceOrderSchema.
        """
        service_order_model = ServiceOrders(
            reservation_id=service_order.reservation_id,
            service_id=service_order.service_id,
            quantity=service_order.quantity,
            status=service_order.status
        )

        self.db.add(service_order_model)
        await self.db.commit()
        await self.db.refresh(service_order_model)

        return ServiceOrderSchema.model_validate(service_order_model)
    
    async def delete_service_order(self, order_id: int) -> ServiceOrderSchema:
        """
        Delete a service order from the database and return it as a ServiceOrderSchema.
        """
        result = await self.db.execute(select(ServiceOrders).where(ServiceOrders.order_id == order_id))
        row = result.scalars().first()

        service_order_schema = ServiceOrderSchema.model_validate(row)

        await self.db.delete(row)
        await self.db.commit()

        return service_order_schema
    
    async def delete_service_orders_by_reservation_id(
        self, reservation_id: int
    ) -> bool:
        stmt = delete(ServiceOrders).where(ServiceOrders.reservation_id == reservation_id)
        await self.db.execute(stmt)
        await self.db.commit()

        return True
