import pytest
import pytest_asyncio
import datetime
from random import randint
from typing import List
import zoneinfo 
from backend.services.reservation import ReservationService
from backend.schemas.guest import GuestSchema
from backend.schemas.reservation import ReservationSchema

@pytest.mark.asyncio
async def test_create_reservation(async_session):
    """
    Tests 'create_reservation' in 'ReservationService' for a new guest & room.
    """
    service = ReservationService(db=async_session)
    
    test_guest = GuestSchema(
        guest_id=None, # let db auto-increment
        full_name="John Tester",
        email=f"test_{randint(10000,99999)}@example.com",
        phone="123-456-7890"
    )

    room_type = "single"
    check_in = datetime.datetime.now()
    check_out = check_in + datetime.timedelta(days=2)

    res = await service.create_reservation(
        guest=test_guest,
        room_type=room_type,
        check_in=check_in,
        check_out=check_out
    )

    assert isinstance(res, ReservationSchema)
    assert res.guest_id is not None
    assert res.reservation_id is not None
    assert res.status == "booked"


@pytest.mark.asyncio
async def test_get_reservations_for_guest(async_session):
    """
    Tests 'get_reservations_for_guest' in 'ReservationService'.
    We assume 'create_reservation' already works, so we create one first.
    """
    service = ReservationService(db=async_session)

    test_guest = GuestSchema(
        full_name="Second Tester",
        email=f"second_{randint(10000,99999)}@example.com",
        phone="555-555-1111"
    )
    check_in = datetime.datetime.now(zoneinfo.ZoneInfo("UTC"))
    check_out = check_in + datetime.timedelta(days=1)

    created = await service.create_reservation(
        guest=test_guest,
        room_type="single",
        check_in=check_in,
        check_out=check_out
    )

    reservations: List[ReservationSchema] = await service.get_reservations_for_guest(created.guest_id)
    assert len(reservations) >= 1
    assert any(r.reservation_id == created.reservation_id for r in reservations)


@pytest.mark.asyncio
async def test_modify_reservation(async_session):
    """
    Tests 'modify_reservation' in 'ReservationService'.
    We'll create a reservation, then update it (date + room).
    """
    service = ReservationService(db=async_session)

    # 1) Create a reservation
    test_guest = GuestSchema(
        full_name="Mod Tester",
        email=f"mod_{randint(10000,99999)}@example.com",
        phone="555-777-2222"
    )
    check_in = datetime.datetime.now(zoneinfo.ZoneInfo("UTC"))
    check_out = check_in + datetime.timedelta(days=2)
    created = await service.create_reservation(
        guest=test_guest,
        room_type="double",
        check_in=check_in,
        check_out=check_out
    )

    # 2) Modify the reservation with new check_in/out
    new_check_in = check_in + datetime.timedelta(days=1)
    new_check_out = new_check_in + datetime.timedelta(days=2)

    updated = await service.modify_reservation(
        reservation_id=created.reservation_id,
        check_in=new_check_in,
        check_out=new_check_out
    )
    # Check the updated in/out
    assert updated.check_in == new_check_in
    assert updated.check_out == new_check_out
    # The room_id should remain the same unless we pass a new room type

    new_updated = await service.modify_reservation(
        reservation_id=created.reservation_id,
        room_type="suite"
    )
    assert new_updated.room_id != updated.room_id, "Expected a different room if we changed the type to suite"


@pytest.mark.asyncio
async def test_cancel_reservation(async_session):
    """
    Tests 'cancel_reservation' in 'ReservationService'.
    We'll create a reservation, then cancel it.
    """
    service = ReservationService(db=async_session)

    test_guest = GuestSchema(
        full_name="Cancel Tester",
        email=f"cancel_{randint(10000,99999)}@example.com",
        phone="555-999-0000"
    )
    check_in = datetime.datetime.now(zoneinfo.ZoneInfo("UTC"))
    check_out = check_in + datetime.timedelta(days=1)
    created = await service.create_reservation(
        guest=test_guest,
        room_type="suite",
        check_in=check_in,
        check_out=check_out
    )

    # now cancel
    result = await service.cancel_reservation(created.reservation_id)
    assert result is True, "Expected successful cancellation"