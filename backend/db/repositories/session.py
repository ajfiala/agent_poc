from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.schemas.session import SessionSchema
from backend.db.models import Session 

class SessionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_sessions(self) -> list[SessionSchema]:
        """
        Fetch all sessions from the database and return them
        as a list of SessionSchema.
        """
        result = await self.db.execute(select(Session))
        rows = result.scalars().all()

        session_schemas = [SessionSchema.model_validate(r) for r in rows]

        return session_schemas
    
    async def add_session(self, session: SessionSchema) -> SessionSchema:
        """
        Create a new session in the database
        and return it as a SessionSchema.
        """
        new_session = Session(**session.model_dump())
        self.db.add(new_session)
        await self.db.commit()
        await self.db.refresh(new_session)
        
        return SessionSchema.model_validate(new_session)
    
    async def get_session_by_id(self, session_id: int) -> SessionSchema:
        """
        Fetch a session by its ID from the database
        and return it as a SessionSchema.
        """
        result = await self.db.execute(select(Session).where(Session.session_id == session_id))
        row = result.scalar_one_or_none()

        if row is None:
            raise ValueError(f"No session found with id {session_id}")
        
        return SessionSchema.model_validate(row)
    
    async def get_sessions_by_guest_id(self, guest_id: int) -> list[SessionSchema]:
        """
        Fetch all sessions for a specific guest from the database
        and return them as a list of SessionSchema.
        """
        result = await self.db.execute(select(Session).where(Session.guest_id == guest_id))
        rows = result.scalars().all()

        session_schemas = [SessionSchema.model_validate(r) for r in rows]

        return session_schemas
    
    async def delete_sessions(self, guest_id: int) -> bool:
        """
        Delete all sessions for a specific guest from the database.
        """
        result = await self.db.execute(select(Session).where(Session.guest_id == guest_id))
        rows = result.scalars().all()
        
        for row in rows:
            await self.db.delete(row)
        
        await self.db.commit()
        
        return True