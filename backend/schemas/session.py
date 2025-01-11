from pydantic import BaseModel

class SessionSchema(BaseModel):
    session_id: int = None
    guest_id: int