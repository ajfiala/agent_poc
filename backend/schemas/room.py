from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

# models a hotel room 
class RoomSchema(BaseModel):
    room_id: int
    room_type: str
    rate: float
    available: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True