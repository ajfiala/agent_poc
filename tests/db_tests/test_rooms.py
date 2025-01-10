import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.repositories.room import RoomRepository
from backend.schemas.room import RoomSchema

@pytest.mark.asyncio
async def test_list_rooms_returns_list_of_room_schema(async_session: AsyncSession):
    """
    Tests that 'list_rooms' in 'RoomRepository' returns
    a non-empty list of RoomSchema objects from our seeded database.
    """

    # Arrange
    repo = RoomRepository(db=async_session)

    # Act
    rooms = await repo.list_rooms()

    # print(f"rooms: {rooms}")

    # Assert
    assert len(rooms) == 30, "Expected at least one room to be returned"
    assert isinstance(rooms[0], RoomSchema), "Expected item to be an instance of RoomSchema"

@pytest.mark.asyncio
async def test_list_rooms_by_type_returns_correct_rooms(async_session: AsyncSession):
    """
    Tests that 'list_rooms_by_type' in 'RoomRepository' returns
    only rooms of the specified type from our seeded database.
    """
    # Arrange
    repo = RoomRepository(db=async_session)
   

    single_rooms = await repo.list_rooms_by_type("single")

    double_rooms = await repo.list_rooms_by_type("double")

    suite_rooms = await repo.list_rooms_by_type("suite")

    # assert

    print(f"len single rooms: {len(single_rooms)}")

    assert len(single_rooms) == 10, "Expected 10 single rooms to be returned"
    assert isinstance(single_rooms[0], RoomSchema), "Expected item to be an instance of RoomSchema"

    assert len(double_rooms) == 10, "Expected 10 double rooms to be returned"
    assert isinstance(double_rooms[0], RoomSchema), "Expected item to be an instance of RoomSchema"

    assert len(suite_rooms) == 10, "Expected 10 suite rooms to be returned"
    assert isinstance(suite_rooms[0], RoomSchema), "Expected item to be an instance of RoomSchema"

