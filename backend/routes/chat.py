# backend/routes/chat.py
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
import json
from backend.db.session import get_db_session
from backend.services.chat import ChatService

router = APIRouter()

@router.post("/chat")
async def post_chat(
    request: Request,
    db: AsyncSession = Depends(get_db_session)
) -> StreamingResponse:
    data = await request.json()
    user_content = data["message"]

    # hard code for local testing. these will come from the cookies
    session_id = 1
    guest_id = 1
    full_name = "John Tester"
    email = "test@email.org"

    chat_service = ChatService(db=db, guest_id=guest_id, full_name=full_name, email=email)

    # An async generator that yields partial text
    async def streamer():
        async for chunk in chat_service.send_message_stream(session_id, guest_id, user_content):
            yield json.dumps({"message": chunk}) + "\n"

    return StreamingResponse(streamer(), media_type="application/json")
