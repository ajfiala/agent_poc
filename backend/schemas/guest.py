from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class GuestSchema(BaseModel):
    guest_id: Optional[int] = None
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
