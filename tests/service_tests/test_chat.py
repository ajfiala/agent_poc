import pytest
import pytest_asyncio
from fastapi import FastAPI, Depends
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from starlette.status import HTTP_401_UNAUTHORIZED
import time 
from backend.db.session import get_db_session
from backend.services.auth import get_token_from_cookie, validate_guest, create_access_token
from backend.schemas.message import MessageSchema
from backend.services.chat import ChatService

@pytest.mark.asyncio
async def test_send_message(async_session):
    """
    Tests that 'send_message' in 'MessageService' returns
    a MessageSchema object after adding a new message to the database.
    """
    # arrange
    service = ChatService(db= async_session)
    message = MessageSchema(
        content="Hello, world!",
        role = "user"
    )

    # Act
    response = await service.send_message(msg=message)

    # Assert
    assert isinstance(response, MessageSchema), "Expected the added message to match the input message"
