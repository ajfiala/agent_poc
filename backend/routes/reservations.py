from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from backend.db.session import get_db_session
from backend.schemas.reservation import ReservationSchema
from backend.schemas.guest import GuestSchema
from backend.services.reservation import ReservationService

from pydantic import BaseModel


router = APIRouter()

# Request body models for creating or updating a reservation
class CreateReservationRequest(BaseModel):
    guest_id: int
    full_name: str
    email: str
    room_type: str
    check_in: datetime
    check_out: datetime

class UpdateReservationRequest(BaseModel):
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    room_type: Optional[str] = None


@router.get("/reservations/{guest_id}", response_model=List[ReservationSchema])
async def get_reservations_for_guest(
    guest_id: int, 
    db: AsyncSession = Depends(get_db_session)
) -> List[ReservationSchema]:
    """
    Retrieve all reservations for a given guest_id.
    """
    reservation_service = ReservationService(db=db)
    return await reservation_service.get_reservations_for_guest(guest_id)


@router.post("/reservations", response_model=ReservationSchema)
async def create_reservation(
    req: CreateReservationRequest,
    db: AsyncSession = Depends(get_db_session)
) -> ReservationSchema:
    """
    Create a new reservation for a given guest, specifying room_type, check_in, check_out.
    """
    reservation_service = ReservationService(db=db)

    # Construct a GuestSchema from request data
    guest = GuestSchema(
        guest_id=req.guest_id,
        full_name=req.full_name,
        email=req.email
    )

    try:
        new_res = await reservation_service.create_reservation(
            guest=guest,
            room_type=req.room_type,
            check_in=req.check_in,
            check_out=req.check_out
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    return new_res


@router.patch("/reservations/{reservation_id}", response_model=ReservationSchema)
async def modify_reservation(
    reservation_id: int,
    req: UpdateReservationRequest,
    db: AsyncSession = Depends(get_db_session)
) -> ReservationSchema:
    """
    Partially update an existing reservation's check_in, check_out, or room_type.
    """
    reservation_service = ReservationService(db=db)
    try:
        updated_res = await reservation_service.modify_reservation(
            reservation_id=reservation_id,
            check_in=req.check_in,
            check_out=req.check_out,
            room_type=req.room_type
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    return updated_res


@router.delete("/reservations/{reservation_id}")
async def cancel_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_db_session)
) -> dict:
    """
    Cancel (delete) an existing reservation by its reservation_id.
    """
    reservation_service = ReservationService(db=db)
    try:
        await reservation_service.cancel_reservation(reservation_id)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    return {"detail": f"Reservation {reservation_id} successfully cancelled"}