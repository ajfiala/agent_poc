import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.repositories.reservation import ReservationRepository
from backend.schemas.reservation import ReservationSchema


@pytest.mark.asyncio
async def test_list_reservations_returns_list_of_reservation_schema(async_session: AsyncSession):
    """
    Tests that 'list_reservations' in 'ReservationRepository' returns
    a non-empty list of ReservationSchema objects from our seeded database.
    """

    # arrange 
    repo = ReservationRepository(db=async_session)

    # act
    reservations = await repo.list_reservations()

    # assert
    assert len(reservations) == 10, "Expected at least one reservation to be returned"

    assert isinstance(reservations[0], ReservationSchema), "Expected item to be an instance of ReservationSchema"

@pytest.mark.asyncio
async def test_list_reservations_by_guest_id_returns_list_of_reservation_schema(async_session: AsyncSession):
    """
    Tests that 'list_reservations_by_guest_id' in 'ReservationRepository' returns
    a non-empty list of ReservationSchema objects from our seeded database.
    """
    # arrange 
    repo = ReservationRepository(db=async_session)
    guest_id = 1

    # act
    reservations = await repo.list_reservations_by_guest_id(guest_id=guest_id)

    # assert
    assert len(reservations) == 1, "Expected at least one reservation to be returned"
    assert isinstance(reservations[0], ReservationSchema), "Expected item to be an instance of ReservationSchema"

@pytest.mark.asyncio
async def test_return_empty_list_for_nonexistent_guest_id(async_session: AsyncSession):
    """
    Tests that 'list_reservations_by_guest_id' in 'ReservationRepository' returns
    an empty list of ReservationSchema objects for a non-existent guest id.
    """
    # arrange 
    repo = ReservationRepository(db=async_session)
    guest_id = 1000

    # act
    reservations = await repo.list_reservations_by_guest_id(guest_id=guest_id)

    # assert
    assert len(reservations) == 0, "Expected an empty list to be returned"


@pytest.mark.asyncio
async def test_create_reservation(async_session: AsyncSession):
    repo = ReservationRepository(db=async_session)
    new_res = ReservationSchema(
        guest_id=1,
        room_id=101,
        check_in="2027-10-01T14:00:00Z",
        check_out="2027-10-02T12:00:00Z",
        status="confirmed"
    )
    created_reservation = await repo.create_reservation(new_res)

    assert isinstance(created_reservation, ReservationSchema)
    assert created_reservation.reservation_id is not None


@pytest.mark.asyncio
async def test_create_reservation_invalid_date(async_session: AsyncSession):
    """
    Tests that 'create_reservation' in 'ReservationRepository' raises an exception
    when the check-in date is after the check-out date.
    """
    repo = ReservationRepository(db=async_session)
    new_res = ReservationSchema(
        guest_id=3,
        room_id=103,
        check_in="1999-10-02T14:00:00Z",
        check_out="1999-10-01T12:00:00Z",
        status="confirmed"
    )

    with pytest.raises(ValueError, match="check_in must be before check_out"):
        await repo.create_reservation(new_res)