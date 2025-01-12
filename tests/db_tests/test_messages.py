import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.message import MessagePairSchema, MessageSchema
from backend.db.repositories.message import MessageRepository

@pytest.mark.asyncio
async def test_add_message_returns_message_pair_schema(async_session: AsyncSession):
    """
    Tests that 'add_message' in 'MessageRepository' returns
    a MessagePairSchema object after adding a new message pair.
    """
    # Arrange
    repo = MessageRepository(db=async_session)

    new_message_pair = MessagePairSchema(
        guest_id=1,             # Assuming a seeded guest with ID=1
        session_id=1,           # Assuming a seeded session with ID=1
        user_message=MessageSchema(
            content="Hello from the user!",
            role="user",
            created_at=None,
            updated_at=None
        ),
        ai_message=MessageSchema(
            content="Hi there, I'm the AI.",
            role="assistant",
            created_at=None,
            updated_at=None
        )
    )

    # Act
    added_message_pair = await repo.add_message(new_message_pair)

    # Assert
    assert added_message_pair == True, "Expected the added message pair to be True"

@pytest.mark.asyncio
async def test_list_messages_returns_list_of_message_pairs(async_session: AsyncSession):
    """
    Tests that 'list_messages' in 'MessageRepository' returns
    a list of MessagePairSchema objects.
    """
    # Arrange
    repo = MessageRepository(db=async_session)

    # Act
    messages = await repo.list_messages()

    # Assert
    assert len(messages) >= 1, "Expected at least one message in the DB"

@pytest.mark.asyncio
async def test_get_messages_by_session_id(async_session: AsyncSession):
    """
    Tests that 'get_messages_by_session_id' in 'MessageRepository' returns
    MessagePairSchema objects for a given session.
    """
    # Arrange
    repo = MessageRepository(db=async_session)
    test_session_id = 1  # or any known session ID

    # Act
    messages = await repo.get_messages_by_session_id(session_id=test_session_id)

    # Assert
    # We expect at least one message for this session if you've seeded or previously added
    assert len(messages) >= 1, "Expected at least one message for this session"
    for msg in messages:
        assert msg.session_id == test_session_id, "Expected session_id to match"

@pytest.mark.asyncio
async def test_delete_messages_by_session_id(async_session: AsyncSession):
    """
    Tests that 'delete_messages_by_session_id' in 'MessageRepository' returns
    a boolean indicating successful deletion of messages for a session.
    """
    # Arrange
    repo = MessageRepository(db=async_session)
    test_session_id = 1

    new_message_pair = MessagePairSchema(
        guest_id=1,
        session_id=test_session_id,
        user_message=MessageSchema(content="I'll be deleted", role="user", created_at=None, updated_at=None),
        ai_message=MessageSchema(content="So will I", role="assistant", created_at=None, updated_at=None)
    )
    await repo.add_message(new_message_pair)

    # Act
    result = await repo.delete_messages_by_session_id(session_id=test_session_id)

    # Assert
    assert result is True, "Expected messages to be deleted for that session"

    # Double-check that no messages remain
    leftover = await repo.get_messages_by_session_id(session_id=test_session_id)
    assert len(leftover) == 0, "Expected all messages for that session to be removed"
