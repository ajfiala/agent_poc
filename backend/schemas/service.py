from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class ServiceSchema(BaseModel):
    service_id: int
    name: Literal["room service", "room service with hot meal", "wake up call", "late check in", "hot water", "electricity",
                  "tour in local waste treatment facility", "unstained towel", "supervised visit", "phone use"]
    description: str
    price: float
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True

class ServiceOrderSchema(BaseModel):
    order_id: int = None # let DB autoincrement
    reservation_id: int
    service_id: int
    quantity: int
    status: Literal["pending", "completed", "cancelled"]
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True