from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.repositories.session import SessionRepository
from backend.db.repositories.guest import GuestRepository
from backend.schemas.session import SessionSchema

class SessionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.guest_repository = GuestRepository(db=db)
        self.session_repository = SessionRepository(db=db)

    async def create_session(self, guest_id: int) -> SessionSchema:
        """
        Create a new session for a guest and return it as a SessionSchema.
        """
        guest = await self.guest_repository.get_guest_by_id(guest_id)
        new_session = SessionSchema(
            guest_id=guest.guest_id,
        )
        session = await self.session_repository.add_session(new_session)

        return session
    
    async def get_session_from_session_id(self, session_id: int) -> SessionSchema:
        """
        Retrieve a session by its ID and return it as a SessionSchema.
        """
        session = await self.session_repository.get_session_by_id(session_id)

        return session

    async def list_sessions_for_guest_id(self, guest_id: int) -> list[SessionSchema]:
        """
        Retrieve all sessions for a specific guest and return them as a list of SessionSchema.
        """
        sessions = await self.session_repository.get_sessions_by_guest_id(guest_id)

        return sessions