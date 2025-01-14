# backend/services/chat.py

import asyncio
import json
import logging
from typing import AsyncGenerator, List, Literal
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
from dotenv import load_dotenv

from backend.db.repositories.message import MessageRepository
from backend.schemas.message import MessageSchema, MessagePairSchema
from backend.schemas.service import ServiceOrderSchema, ServiceSchema
from backend.schemas.guest import GuestSchema
from backend.schemas.reservation import ReservationSchema
from backend.services.reservation import ReservationService
from backend.services.service_orders import ServiceOrderService

logger = logging.getLogger(__name__)
load_dotenv()

class ChatService:
    def __init__(self, db: AsyncSession, guest_id: int, full_name: str, email: str):
        self.db = db
        self.message_repo = MessageRepository(db=db)
        self.reservation_service = ReservationService(db=db)
        self.service_order_service = ServiceOrderService(db=db)
        self.available_services = Literal["1. room service", "2. room service with hot meal", "3. wake up call",
                                           "4. late check in", "5. hot water", "6. electricity",
                  "7. tour in local waste treatment facility", "8. unstained towel", "9. supervised visit", "10. phone use"]

        self.guest = GuestSchema(
            guest_id=guest_id,
            full_name=full_name,
            email=email
        )
        self.reservations = List[ReservationSchema]

        self.agent = Agent(
            "openai:gpt-4o",
        )

        self._register_tools()

    def _register_tools(self):
        """
        Turn each service method into a "tool" function, 
        which the AI can call when it needs that functionality.
        """

        ####################
        # Reservation Tools
        ####################

        @self.agent.system_prompt
        def get_current_user():

            system_prompt = f"""
            "You are a hotel AI agent assistant for WhipSplash. WhipSplash offers three types of rooms"
            " - single, double, and suite. You can help guests create, modify, or cancel reservations,"
            " and add service orders to their reservations, such as: {self.available_services}."
            " The guest you are assisting is: {self.guest}."
            " Use the get_reservations tool to see all reservations for that guest."
            " We do not rely solely on message history for reservation data."
            """
            return system_prompt

        @self.agent.tool
        async def create_reservation(
            ctx: RunContext[GuestSchema],
            room_type: str,
            check_in: datetime,
            check_out: datetime
        ) -> ReservationSchema:
            """
            Create a new reservation with the (already known) guest, 
            plus room_type, check_in, check_out.

            This tool calls the underlying:
            ReservationService.create_reservation(...)
            """
            data = str(ctx)
            with open("tool_use.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return await self.reservation_service.create_reservation(
                self.guest, room_type, check_in, check_out
            )

        @self.agent.tool
        async def get_reservations(
            ctx: RunContext[GuestSchema]
        ) -> List[ReservationSchema]:
            """
            Get all reservations for the guest, calling:
            ReservationService.get_reservations_for_guest(guest_id)
            """
            data = str(ctx)
            with open("tool_use.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            reservations = await self.reservation_service.get_reservations_for_guest(self.guest.guest_id)
            self.reservations = reservations
            return reservations

        @self.agent.tool
        async def modify_reservation(
            ctx: RunContext[GuestSchema],
            reservation_id: int,
            check_in: datetime = None,
            check_out: datetime = None,
            room_type: str = None
        ) -> ReservationSchema:
            """
            Modify an existing reservation's dates or room_type.
            Calls: ReservationService.modify_reservation(...)
            """
            data = str(ctx)
            with open("tool_use.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return await self.reservation_service.modify_reservation(
                reservation_id, check_in, check_out, room_type
            )

        @self.agent.tool
        async def cancel_reservation(
            ctx: RunContext[GuestSchema],
            reservation_id: int
        ) -> bool:
            """
            Cancel an existing reservation by reservation_id.
            Calls: ReservationService.cancel_reservation(...)
            """
            return await self.reservation_service.cancel_reservation(reservation_id)

        ###########################
        # Service Order Tools
        ###########################

        @self.agent.tool
        async def list_all_services(
            ctx: RunContext[GuestSchema]
        ) -> List[ServiceSchema]:
            """
            List all available hotel services 
            Calls: ServiceOrderService.list_all_services()
            """
            data = str(ctx)
            with open("tool_use.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return await self.service_order_service.list_all_services()

        @self.agent.tool
        async def create_service_order(
            ctx: RunContext[GuestSchema],
            reservation_id: int,
            service_id: int,
            quantity: int,
            status: str = "pending"
        ) -> ServiceOrderSchema:
            """
            Create a new service order for a reservation, 
            calling: ServiceOrderService.create_service_order(...)
            """
            data = str(ctx)
            with open("tool_use.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return await self.service_order_service.create_service_order(
                reservation_id=reservation_id,
                service_id=service_id,
                quantity=quantity,
                status=status
            )

        @self.agent.tool
        async def list_service_orders_by_reservation_id(
            ctx: RunContext[GuestSchema],
            reservation_id: int
        ) -> List[ServiceOrderSchema]:
            """
            List all service orders for a given reservation.
            Calls: ServiceOrderService.list_service_orders_by_reservation_id(...)
            """
            data = str(ctx)
            with open("tool_use.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return await self.service_order_service.list_service_orders_by_reservation_id(reservation_id)

        @self.agent.tool
        async def delete_service_order(
            ctx: RunContext[GuestSchema],
            order_id: int
        ) -> bool:
            """
            Delete a single service order by its order_id.
            Calls: ServiceOrderService.delete_service_order(...)
            """
            return await self.service_order_service.delete_service_order(order_id)

        @self.agent.tool
        async def delete_service_orders_for_reservation(
            ctx: RunContext[GuestSchema],
            reservation_id: int
        ) -> bool:
            """
            Delete all service orders for a given reservation.
            Calls: ServiceOrderService.delete_service_orders_for_reservation(...)
            """
            return await self.service_order_service.delete_service_orders_for_reservation(reservation_id)

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


        prior_pairs = await self.message_repo.get_messages_by_session_id(session_id)
        message_history = []
        for pair in prior_pairs:
    
            user_req = ModelRequest(parts=[UserPromptPart(content=pair.user_message.content)])
            message_history.append(user_req)
 
            ai_resp = ModelResponse(parts=[TextPart(content=pair.ai_message.content)])
            message_history.append(ai_resp)

        print(f"Loaded {len(message_history)} messages from DB")

        async with self.agent.run_stream(
            user_prompt=user_content,
            message_history=message_history,
            deps=[self.guest, self.reservations]
        ) as result:

            final_text = ""

            # Stream chunks back to the UI or caller
            async for chunk in result.stream_text(delta=False, debounce_by=0.01):
                final_text += chunk
                yield chunk

        # The conversation is done; gather new messages from the result
        new_msgs = result.new_messages()

        # For debugging: save the entire conversation to a file
        raw_bytes = result.all_messages_json()
        data = json.loads(raw_bytes)  
        with open("all_messages.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # If we have exactly two new messages (user+assistant), store them in DB
        if len(new_msgs) == 2:
            user_m = new_msgs[0]
            ai_m = new_msgs[1]

            user_schema = MessageSchema(content=user_m.parts[0].content, role="user")
            ai_schema = MessageSchema(content=ai_m.parts[0].content, role="assistant")

            new_pair = MessagePairSchema(
                guest_id=guest_id,
                session_id=session_id,
                user_message=user_schema,
                ai_message=ai_schema,
            )
            await self.message_repo.add_message(new_pair)
