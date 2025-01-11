import pytest
import pytest_asyncio
from fastapi import FastAPI, Depends
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from starlette.status import HTTP_401_UNAUTHORIZED
import time 
from backend.db.session import get_db_session
from backend.services.auth import get_token_from_cookie, validate_guest, create_access_token
from backend.services.session import SessionService
from backend.schemas.session import SessionSchema

@pytest.mark.asyncio
async def test_create_session_with_session_service(async_session):
    """
    Tests that 'create_session' in 'SessionService' returns
    a SessionSchema object after adding a new session to the database.
    """
    service = SessionService(db= async_session)

    # Act
    new_session = await service.create_session(guest_id=1) 

    # Assert
    assert isinstance(new_session, SessionSchema), "Expected the added session to match the input session"
    assert new_session.guest_id == 1, "Expected the added session to match the input session"

@pytest.mark.asyncio 
async def test_create_session_with_invalid_guest_id(async_session):
    """
    Tests that 'create_session' in 'SessionService' raises a ValueError
    when an invalid guest ID is provided.
    """
    # arrange
    service = SessionService(db= async_session)

    # Act
    with pytest.raises(ValueError):
        await service.create_session(guest_id=9999)

@pytest.mark.asyncio 
async def test_get_session_from_session_id(async_session):
    """
    Tests that 'get_session_from_session_id' in 'SessionService' returns
    a SessionSchema object after retrieving a session from the database.
    """
    # arrange
    service = SessionService(db= async_session)

    # Act
    session = await service.get_session_from_session_id(session_id=7)

    # Assert
    assert isinstance(session, SessionSchema), "Expected the retrieved session to match the input session"

@pytest.mark.asyncio
async def test_list_sessions_for_guest_id(async_session):
    """
    Tests that 'list_sessions_for_guest_id' in 'SessionService' returns
    a list of SessionSchema objects after retrieving sessions for a guest from the database.
    """
    # arrange
    service = SessionService(db= async_session)

    # Act
    sessions = await service.list_sessions_for_guest_id(guest_id=1)

    # Assert
    assert isinstance(sessions, list), "Expected the retrieved sessions to be a list"