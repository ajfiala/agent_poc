from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.repositories.message import MessageRepository
from backend.schemas.message import MessageSchema
from pydantic_ai import Agent

class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.message_repository = MessageRepository(db=db)
        self.main_agent = Agent('openai:gpt-4o')

    async def send_message(self, msg: MessageSchema) -> MessageSchema:
        """
        Send a message and return the AI response as a MessageSchema.
        """
        ai_response = MessageSchema(content="", role="assistant")
        
        # Use self.agent.run_stream(...) to get an async streaming generator
        async with self.main_agent.run_stream(msg.content) as result:
            async for chunk in result.stream(debounce_by=0.02):
                # 'chunk' is a partial string
                # yield chunk
                ai_response.content += chunk
        
        print(f" AI response: {ai_response.content}")
        return ai_response

    

        