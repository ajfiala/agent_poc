from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from backend.db.session import get_db_session
from backend.schemas.service import ServiceSchema
from backend.schemas.service import ServiceOrderSchema
from backend.services.service_orders import ServiceOrderService

from pydantic import BaseModel

router = APIRouter()

# Request body model for creating a new service order
class CreateServiceOrderRequest(BaseModel):
    reservation_id: int
    service_id: int
    quantity: int
    status: str = "pending"


@router.get("/services", response_model=List[ServiceSchema])
async def list_all_services(
    db: AsyncSession = Depends(get_db_session)
) -> List[ServiceSchema]:
    """
    Return a list of all available services from the database.
    """
    service_order_service = ServiceOrderService(db=db)
    return await service_order_service.list_all_services()


@router.get("/services/{service_id}", response_model=ServiceSchema)
async def get_service_by_id(
    service_id: int, 
    db: AsyncSession = Depends(get_db_session)
) -> ServiceSchema:
    """
    Return a single service by its ID.
    """
    service_order_service = ServiceOrderService(db=db)
    try:
        return await service_order_service.get_service_by_id(service_id)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))


@router.post("/serviceorders", response_model=ServiceOrderSchema)
async def create_service_order(
    req: CreateServiceOrderRequest,
    db: AsyncSession = Depends(get_db_session)
) -> ServiceOrderSchema:
    """
    Create a new service order for a given reservation and service.
    """
    service_order_service = ServiceOrderService(db=db)
    try:
        order = await service_order_service.create_service_order(
            reservation_id=req.reservation_id,
            service_id=req.service_id,
            quantity=req.quantity,
            status=req.status
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    return order


@router.get("/serviceorders/by_reservation/{reservation_id}", response_model=List[ServiceOrderSchema])
async def list_service_orders_for_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_db_session)
) -> List[ServiceOrderSchema]:
    """
    List all service orders for a particular reservation_id.
    """
    service_order_service = ServiceOrderService(db=db)
    return await service_order_service.list_service_orders_by_reservation_id(reservation_id)


@router.delete("/serviceorders/{order_id}")
async def delete_service_order(
    order_id: int,
    db: AsyncSession = Depends(get_db_session)
) -> dict:
    """
    Delete a single service order by its ID.
    """
    service_order_service = ServiceOrderService(db=db)
    try:
        await service_order_service.delete_service_order(order_id)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    return {"detail": f"Service order {order_id} successfully deleted"}


@router.delete("/serviceorders/for_reservation/{reservation_id}")
async def delete_service_orders_for_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_db_session)
) -> dict:
    """
    Delete all service orders for a given reservation_id.
    """
    service_order_service = ServiceOrderService(db=db)
    await service_order_service.delete_service_orders_for_reservation(reservation_id)
    return {"detail": f"All service orders for reservation {reservation_id} deleted"}
