from pydantic import BaseModel

class SessionSchema(BaseModel):
    session_id: int = None
    guest_id: int

    class Config:
        from_attributes = True