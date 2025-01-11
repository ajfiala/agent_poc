import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.session import SessionSchema
from backend.db.repositories.session import SessionRepository

@pytest.mark.asyncio
async def test_list_sessions_returns_list_of_session_schema(async_session: AsyncSession):
    """
    Tests that 'list_sessions' in 'SessionRepository' returns
    a non-empty list of SessionSchema objects from our seeded database.
    """
    
    # Arrange
    repo = SessionRepository(db=async_session)

    # Act
    sessions = await repo.list_sessions()

    # Assert
    assert len(sessions) > 1, "Expected at least one session to be returned"

@pytest.mark.asyncio
async def test_add_session_returns_session_schema(async_session: AsyncSession):
    """
    Tests that 'add_session' in 'SessionRepository' returns
    a SessionSchema object after adding a new session to the database.
    """
    
    # Arrange
    repo = SessionRepository(db=async_session)
    new_session = SessionSchema(
        session_id=8,
        guest_id=1,
        start_time="2023-10-01T00:00:00Z",
        end_time="2023-10-01T01:00:00Z",
        notes="Test session"
    )

    # Act
    added_session = await repo.add_session(new_session)

    # Assert
    assert added_session == new_session, "Expected the added session to match the input session"

@pytest.mark.asyncio
async def test_get_session_by_id_returns_session_schema(async_session: AsyncSession):
    """
    Tests that 'get_session_by_id' in 'SessionRepository' returns
    a SessionSchema object for a given session ID.
    """
    
    # Arrange
    repo = SessionRepository(db=async_session)

    # Act
    session = await repo.get_session_by_id(8)

    # Assert
    assert session.guest_id == 1, "Expected the session ID to match the input ID"

@pytest.mark.asyncio    
async def test_get_sessions_by_guest_id_returns_session_schema(async_session: AsyncSession):
    """
    Tests that 'get_session_by_guest_id' in 'SessionRepository' returns
    a SessionSchema object for a given guest ID.
    """
    
    # Arrange
    repo = SessionRepository(db=async_session)

    # Act
    sessions = await repo.get_sessions_by_guest_id(1)

    # Assert
    assert len(sessions) >= 1, "Expected at least one session to be returned for the guest"

@pytest.mark.asyncio
async def test_delete_sessions_returns_bool(async_session: AsyncSession):
    """
    Tests that 'delete_sessions' in 'SessionRepository' returns
    a boolean indicating whether the sessions were successfully deleted.
    """
    
    # Arrange
    repo = SessionRepository(db=async_session)

    # Act
    result = await repo.delete_sessions(1)

    # Assert
    assert result == True, "Expected the sessions to be deleted successfully"