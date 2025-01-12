from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.schemas.message import MessageSchema, MessagePairSchema
from backend.db.models import MessagePair

class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_message(self, message: MessagePairSchema) -> bool:
        """
        Add a new message pair to the database and return
        it as a MessagePairSchema.
        
        We'll store only the 'content' in user_message / ai_message columns
        and rely on the 'role' field in your Pydantic model if needed for the app logic.
        """
        new_message_pair = MessagePair(
            guest_id=message.guest_id,
            session_id=message.session_id,
            user_message=message.user_message.content,   
            ai_message=message.ai_message.content        
        )

        self.db.add(new_message_pair)
        await self.db.commit()
        await self.db.refresh(new_message_pair)

        return True
    
    async def list_messages(self) -> list[MessagePairSchema]:
        """
        Fetch all messages from the database and return them
        as a list of MessagePairSchema.
        """
        result = await self.db.execute(select(MessagePair))
        rows = result.scalars().all()

        message_pairs = []
        for row in rows:
            message_pairs.append(
                MessagePairSchema(
                    message_id=row.message_id,
                    guest_id=row.guest_id,
                    session_id=row.session_id,
                    user_message=MessageSchema(
                        content=row.user_message,
                        role="user", 
                        created_at=None,
                        updated_at=None,
                    ),
                    ai_message=MessageSchema(
                        content=row.ai_message,
                        role="assistant", 
                        created_at=None,
                        updated_at=None,
                    )
                )
            )
        return message_pairs

    async def get_messages_by_session_id(self, session_id: int) -> list[MessagePairSchema]:
        """
        Fetch all messages for a specific session from the database
        and return them as a list of MessagePairSchema.
        """
        result = await self.db.execute(
            select(MessagePair).where(MessagePair.session_id == session_id)
        )
        rows = result.scalars().all()

        message_pairs = []
        for row in rows:
            message_pairs.append(
                MessagePairSchema(
                    message_id=row.message_id,
                    guest_id=row.guest_id,
                    session_id=row.session_id,
                    user_message=MessageSchema(
                        content=row.user_message,
                        role="user",  
                    ),
                    ai_message=MessageSchema(
                        content=row.ai_message,
                        role="assistant",
                    )
                )
            )
        return message_pairs

    async def delete_messages_by_session_id(self, session_id: int) -> bool:
        """
        Delete all messages for a specific session from the database.
        """
        result = await self.db.execute(
            select(MessagePair).where(MessagePair.session_id == session_id)
        )
        rows = result.scalars().all()
        
        for row in rows:
            await self.db.delete(row)
        
        await self.db.commit()
        
        return True
