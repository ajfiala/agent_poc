import pytest
from sqlalchemy.ext.asyncio import AsyncSession
import random
from backend.db.repositories.guest import GuestRepository
from backend.schemas.guest import GuestSchema

@pytest.mark.asyncio
async def test_list_guests_returns_list_of_guest_schema(async_session: AsyncSession):
    """
    Tests that 'list_guests' in 'GuestRepository' returns
    a non-empty list of GuestSchema objects from our seeded database.
    """

    # Arrange
    repo = GuestRepository(db=async_session)

    # Act
    guests = await repo.list_guests()

    # Assert
    assert len(guests) == 30, "Expected at least one guest to be returned"

@pytest.mark.asyncio
async def test_get_guest_by_email_returns_guest_schema(async_session: AsyncSession):
    """
    Tests that 'get_guest_by_email' in 'GuestRepository' returns
    a GuestSchema object for a given email from our seeded database.
    """
    # Arrange
    repo = GuestRepository(db=async_session)
    test_email = "chris.cheeseburger@oddmail.net"

    # Act
    guest = await repo.get_guest_by_email(email=test_email)

    # Assert
    assert guest.email == test_email, "Expected guest email to match the test email"

@pytest.mark.asyncio
async def test_create_guest_returns_guest_schema(async_session: AsyncSession):
    """
    Tests that 'create_guest' in 'GuestRepository' returns
    a GuestSchema object for a given email from our seeded database.
    """
    # Arrange
    repo = GuestRepository(db=async_session)
    test_guest = GuestSchema(
        full_name="Test Guest",
        email="test123@email.org",
        phone="1234567890",
        created_at=None,
        updated_at=None
    )

    # Act
    guest = await repo.create_guest(guest=test_guest)

    print(guest)

    # Assert
    assert guest.email == test_guest.email, "Expected guest email to match the test email"
    assert guest.full_name == test_guest.full_name, "Expected guest full name to match the test full name"

@pytest.mark.asyncio
async def test_delete_guest_deletes_guest(async_session: AsyncSession):
    """
    Tests that 'delete_guest' in 'GuestRepository' deletes
    a guest from the database.
    """
    # Arrange
    repo = GuestRepository(db=async_session)
    test_email = "test123@email.org"

    # Act
    res = await repo.delete_guest(email=test_email)

    # Assert
    assert res == True, "Expected one guest to be deleted"