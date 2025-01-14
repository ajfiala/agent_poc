import pytest
import pytest_asyncio
from random import randint

from backend.services.service_orders import ServiceOrderService
from backend.schemas.service import ServiceOrderSchema, ServiceSchema

@pytest.mark.asyncio
async def test_list_all_services(async_session):
    """
    Tests 'list_all_services' in 'ServiceOrderService'.
    We assume there's at least one seeded service in the DB.
    """
    service = ServiceOrderService(db=async_session)

    services = await service.list_all_services()
    assert isinstance(services, list)
    assert len(services) >= 1, "Expected at least one service in the database"
    assert all(isinstance(s, ServiceSchema) for s in services)

@pytest.mark.asyncio
async def test_get_service_by_id(async_session):
    """
    Tests 'get_service_by_id' in 'ServiceOrderService'.
    We assume service_id=1 exists in the seeded DB.
    """
    service = ServiceOrderService(db=async_session)

    service_obj = await service.get_service_by_id(service_id=1)
    assert isinstance(service_obj, ServiceSchema), "Expected a valid ServiceSchema object"
    assert service_obj.service_id == 1

    # negative test: non-existent service
    with pytest.raises(ValueError):
        await service.get_service_by_id(999999)

@pytest.mark.asyncio
async def test_create_service_order(async_session):
    """
    Tests 'create_service_order' in 'ServiceOrderService'.
    We assume that service_id=1 exists and reservation_id=1 is valid in your test DB.
    """
    service = ServiceOrderService(db=async_session)

    created_order = await service.create_service_order(
        reservation_id=1,
        service_id=1,
        quantity=2,
        status="pending"
    )
    assert isinstance(created_order, ServiceOrderSchema), "Expected a ServiceOrderSchema on creation"
    assert created_order.reservation_id == 1
    assert created_order.service_id == 1
    assert created_order.quantity == 2
    assert created_order.status == "pending"

@pytest.mark.asyncio
async def test_list_service_orders_by_reservation_id(async_session):
    """
    Tests 'list_service_orders_by_reservation_id' in 'ServiceOrderService'.
    We assume reservation_id=1 has at least one service order from the test above.
    """
    service = ServiceOrderService(db=async_session)

    orders = await service.list_service_orders_by_reservation_id(reservation_id=1)
    assert isinstance(orders, list)
    if orders:
        assert all(isinstance(o, ServiceOrderSchema) for o in orders)
    else:
        # If you don't have seeded data, after the test_create_service_order above,
        # there should be at least 1 order for reservation_id=1.
        pytest.fail("Expected at least one service order for reservation_id=1")

@pytest.mark.asyncio
async def test_delete_service_order(async_session):
    """
    Tests 'delete_service_order' in 'ServiceOrderService'.
    We'll create an order, then delete it and confirm it's gone.
    """
    service = ServiceOrderService(db=async_session)

    # 1) create an order
    created_order = await service.create_service_order(
        reservation_id=2,
        service_id=2,
        quantity=1,
        status="pending"
    )

    # 2) delete the order
    deleted = await service.delete_service_order(order_id=created_order.order_id)
    assert deleted is True, "Expected the order to be successfully deleted"

    # 3) confirm
    orders = await service.list_service_orders_by_reservation_id(reservation_id=2)
    assert all(o.order_id != created_order.order_id for o in orders), "Deleted order should not appear in the list"

@pytest.mark.asyncio
async def test_delete_service_orders_for_reservation(async_session):
    """
    Tests 'delete_service_orders_for_reservation' in 'ServiceOrderService'.
    We'll create a few orders for reservation_id=3, then delete them all.
    """
    service = ServiceOrderService(db=async_session)

    # 1) create multiple orders
    order1 = await service.create_service_order(
        reservation_id=3,
        service_id=1,
        quantity=1,
        status="pending"
    )
    order2 = await service.create_service_order(
        reservation_id=3,
        service_id=2,
        quantity=2,
        status="pending"
    )

    # 2) delete all
    await service.delete_service_orders_for_reservation(reservation_id=3)

    # 3) confirm they're gone
    remaining_orders = await service.list_service_orders_by_reservation_id(reservation_id=3)
    assert len(remaining_orders) == 0, "Expected no service orders for reservation_id=3 after delete"
