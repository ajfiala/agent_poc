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
async def test_list_available_rooms_by_type(async_session: AsyncSession):
    """
    Tests that 'list_available_rooms_by_type' in 'RoomRepository' returns
    only available rooms of the specified type from our seeded database.
    """
    # Arrange
    repo = RoomRepository(db=async_session)
   
    single_rooms = await repo.list_available_rooms_by_type("single")
    double_rooms = await repo.list_available_rooms_by_type("double")
    suite_rooms = await repo.list_available_rooms_by_type("suite")

    # assert
    print(f"len single rooms: {len(single_rooms)}")

    assert len(single_rooms) == 10, "Expected 10 single rooms to be returned"
    assert isinstance(single_rooms[0], RoomSchema), "Expected item to be an instance of RoomSchema"

    assert len(double_rooms) == 10, "Expected 10 double rooms to be returned"
    assert isinstance(double_rooms[0], RoomSchema), "Expected item to be an instance of RoomSchema"

    assert len(suite_rooms) == 10, "Expected 10 suite rooms to be returned"
    assert isinstance(suite_rooms[0], RoomSchema), "Expected item to be an instance of RoomSchema"


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


@pytest.mark.asyncio
async def test_get_room_by_room_id_returns_correct_room(async_session: AsyncSession):
    """
    Tests that 'get_room_by_room_id' in 'RoomRepository' returns
    the correct room from our seeded database.
    """
    # Arrange
    repo = RoomRepository(db=async_session)

    room = await repo.get_room_by_room_id(101)

    # Assert
    assert room.room_id == 101, "Expected room number to be 101"
    assert room.room_type == "single", "Expected room type to be 'single'"


@pytest.mark.asyncio
async def test_update_room_available_updates_availability_correctly(async_session: AsyncSession):
    """
    Tests that 'update_room_available' in 'RoomRepository' correctly updates
    the availability of a room in our seeded database.
    """
    # Arrange
    repo = RoomRepository(db=async_session)

    room = await repo.get_room_by_room_id(101)

    result = await repo.update_room_availability(room_id=101, available=False)

    # Assert
    assert result is True, "Expected update_room_available to return True"

    updated_room = await repo.get_room_by_room_id(101)
    assert updated_room.available is False, "Expected room availability to be updated to False"


@pytest.mark.asyncio
async def test_update_unavailable_room_to_available_correctly(async_session: AsyncSession):
    """
    Tests that 'update_room_available' in 'RoomRepository' correctly updates
    the availability of a room in our seeded database.
    """
    # Arrange
    repo = RoomRepository(db=async_session)

    room = await repo.get_room_by_room_id(101)

    result = await repo.update_room_availability(room_id=101, available=True)

    # Assert
    assert result is True, "Expected update_room_available to return True"

    updated_room = await repo.get_room_by_room_id(101)
    assert updated_room.available is True, "Expected room availability to be updated to True"


@pytest.mark.asyncio
async def test_update_room_available_returns_false_for_nonexistent_room(async_session: AsyncSession):
    """
    Tests that 'update_room_available' in 'RoomRepository' returns False
    when trying to update the availability of a room that does not exist.
    """
    # Arrange
    repo = RoomRepository(db=async_session)

    result = await repo.update_room_availability(room_id=999, available=False)

    # Assert
    assert result is False, "Expected update_room_available to return False for a nonexistent room"
