import asyncio
import json
import logging
from typing import AsyncGenerator, List
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import (
    ModelMessage, 
    ModelRequest, 
    UserPromptPart, 
    ModelResponse, 
    TextPart
)
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.db.repositories.message import MessageRepository
from backend.schemas.message import MessageSchema, MessagePairSchema
from backend.schemas.guest import GuestSchema
from backend.schemas.reservation import ReservationSchema
from backend.services.reservation import ReservationService

logger = logging.getLogger(__name__)
load_dotenv()

class ChatService:
    def __init__(self, db: AsyncSession, guest_id: int, full_name: str, email: str):
        self.db = db
        self.message_repo = MessageRepository(db=db)
        self.reservation_service = ReservationService(db=db)
        self.guest = GuestSchema(
            guest_id=guest_id,
            full_name=full_name,
            email=email
        )
        self.agent = Agent(
            "openai:gpt-4o",          
            
        )
        # Register each reservation method as a tool:
        self._register_tools()

    def _register_tools(self):
        """
        Turn each ReservationService method into a "tool" function.
        The tool must have the signature (RunContext[Deps], <other args>...).
        """

        @self.agent.system_prompt
        def get_current_user():
            system_prompt = f"""
            "You are a hotel AI agent assistant for WhipSplash. WhipSplash offers three types of rooms"
            " - single, double, and suite. You can help guests create, modify, or cancel reservations."
            " You can also provide information about existing reservations."
            "When a user asks to modify a reservation, use the get_reservations tool to see"
            " all reservations for that guest using the provided guest ID. The current guest whom"
            " When users ask for a list of current reservations, use the get_reservations tool to see"
            " all reservations for that guest using the provided guest ID. Don't rely on message history for this."
            " The state for reservations is in the database. the message history isn't as reliable for this. "
            " you are assisting is: {self.guest}."
            """
            return system_prompt

        @self.agent.tool
        async def create_reservation(
            ctx: RunContext[GuestSchema],
            guest: GuestSchema,
            room_type: str,
            check_in: datetime,
            check_out: datetime
        ) -> ReservationSchema:
            """
            Create a new reservation with guest, room_type, check_in, check_out.
            You are to use the guest provided in the RunContext.
            This tool calls this method:
            (method) def create_reservation(
                guest: GuestSchema,
                room_type: str,
                check_in: datetime,
                check_out: datetime
            ) -> Coroutine[Any, Any, ReservationSchema]
            Creates a new reservation for a given guest, room type, and date range, returning a ReservationSchema.
            """
            data = str(ctx)  
            with open("tool_use.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return await self.reservation_service.create_reservation(
                guest, room_type, check_in, check_out
            )

        @self.agent.tool
        async def get_reservations(
            ctx: RunContext[str],
            guest_id: int
        ) -> List[ReservationSchema]:
            """
            Get all reservations for a given guest_id. The function this tool calls is def get_reservations_for_guest(guest_id: int).
            It returns all reservations for the specified guest ID.
            """
            data =str(ctx)
            with open("tool_use.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return await self.reservation_service.get_reservations_for_guest(guest_id)

        @self.agent.tool
        async def modify_reservation(
            ctx: RunContext[str],
            reservation_id: int,
            check_in: datetime = None,
            check_out: datetime = None,
            room_type: str = None
        ) -> ReservationSchema:
            """
            Modify an existing reservation's check_in, check_out, or room_type.
            This tool uses this method: (method) def modify_reservation(
                reservation_id: int,
                check_in: datetime | None = None,
                check_out: datetime | None = None,
                room_type: str | None = None
            ) -> Coroutine[Any, Any, ReservationSchema]
            here's the docstring: 
            Modify an existing reservation, allowing new check_in, check_out, or room_type.
            """
            data =str(ctx)
            with open("tool_use.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return await self.reservation_service.modify_reservation(
                reservation_id, check_in, check_out, room_type
            )

        @self.agent.tool
        async def cancel_reservation(
            ctx: RunContext[str],
            reservation_id: int
        ) -> bool:
            """
            Cancel an existing reservation by its reservation_id.
            Here's the method this tool calls: (method) def cancel_reservation(reservation_id: int) -> Coroutine[Any, Any, bool]
            Cancels (deletes) an existing reservation from the database. Returns True if successful.
            """
            return await self.reservation_service.cancel_reservation(reservation_id)

    async def send_message_stream(
        self,
        session_id: int,
        guest_id: int,
        user_content: str
    ) -> AsyncGenerator[str, None]:
        """
        1) Load message history from DB for session_id
        2) Call agent.run_stream(...) with user prompt + message history
        3) Yield partial text as it arrives
        4) On completion, store new user+AI messages in the DB
        """

        # 1) Build message history from DB
        prior_pairs = await self.message_repo.get_messages_by_session_id(session_id)
        message_history = []
        for pair in prior_pairs:
            # user request
            user_req = ModelRequest(parts=[UserPromptPart(content=pair.user_message.content)])
            message_history.append(user_req)
            # AI response
            ai_resp = ModelResponse(parts=[TextPart(content=pair.ai_message.content)])
            message_history.append(ai_resp)

        print(f"Loaded {len(message_history)} messages from DB")
        # print(f"messages: {message_history}")
        # 2) run the agent with user prompt
        async with self.agent.run_stream(
            user_prompt=user_content,
            message_history=message_history,
            deps=self.guest
        ) as result:

            final_text = ""

            async for chunk in result.stream_text(delta=False, debounce_by=0.01):
                final_text += chunk
                yield chunk

        new_msgs = result.new_messages()

        # write result.all_messages_json() to a file
        raw_bytes = result.all_messages_json()
        data = json.loads(raw_bytes)  
        with open("all_messages.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        if len(new_msgs) == 2:
            user_m = new_msgs[0]
            ai_m = new_msgs[1]

            # Convert so we can store in DB
            user_schema = MessageSchema(content=user_m.parts[0].content, role="user")
            ai_schema = MessageSchema(content=ai_m.parts[0].content, role="assistant")

            new_pair = MessagePairSchema(
                guest_id=guest_id,
                session_id=session_id,
                user_message=user_schema,
                ai_message=ai_schema,
            )
            await self.message_repo.add_message(new_pair)