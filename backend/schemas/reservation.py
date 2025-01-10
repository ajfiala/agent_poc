from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReservationSchema(BaseModel):
    reservation_id: Optional[int] = None
    guest_id: int
    room_id: int
    check_in: datetime
    check_out: datetime
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True