import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.repositories.service import ServiceRepository
from backend.db.repositories.service_order import ServiceOrderRepository
from backend.schemas.service import ServiceSchema, ServiceOrderSchema

#############
## Test the service repository
##############

@pytest.mark.asyncio
async def test_list_available_services_return_list_service_schema(async_session: AsyncSession):
    """
    tests that list_services in 'ServiceRepository' returns a non-empty list of ServiceSchema objects from our seeded database.
    """

    # arrange 
    repo = ServiceRepository(db=async_session)

    # act
    services = await repo.list_services()


    # assert
    assert len(services) >= 1, "Expected at least one service to be returned"

@pytest.mark.asyncio
async def test_get_service_by_id_returns_service_schema(async_session: AsyncSession):
    """
    Tests that 'get_service_by_id' in 'ServiceRepository' returns a single ServiceSchema object from our seeded database.
    """

    # Arrange
    repo = ServiceRepository(db=async_session)

    # Act
    service = await repo.get_service_by_id(service_id=1)

    # Assert
    assert isinstance(service, ServiceSchema), "Expected item to be an instance of ServiceSchema"

#############
## Test the service orders repository
##############

@pytest.mark.asyncio
async def test_create_service_order_for_electricity_for_guest(async_session: AsyncSession):
    """
    Tests that 'create_service_order' in 'ServiceOrderRepository' creates a new service order for electricity for a guest.
    """

    # Arrange
    repo = ServiceOrderRepository(db=async_session)

    service_order = ServiceOrderSchema(
        reservation_id=1,
        service_id=10,
        quantity=1,
        status="pending"
    )

    # Act
    service_order = await repo.create_service_order(service_order=service_order)

    # Assert
    assert service_order.reservation_id == 1, "Expected reservation_id to be 1"
    assert service_order.service_id == 10, "Expected service_id to be 1"
    assert service_order.quantity == 1, "Expected quantity to be 1"
    assert service_order.status == "pending", "Expected status to be 'pending'"

@pytest.mark.asyncio 
async def test_list_service_order_by_reservation_id(async_session: AsyncSession):
    """
    Tests that 'list_service_order_by_guest_id' in 'ServiceOrderRepository' returns a non-empty list of ServiceOrderSchema objects from our seeded database.
    """

    # Arrange
    repo = ServiceOrderRepository(db=async_session)

    # Act
    service_orders = await repo.list_service_order_by_reservation_id(reservation_id=1)

    # Assert
    assert len(service_orders) >= 1, "Expected at least one service order to be returned"

@pytest.mark.asyncio
async def test_delete_service_order_by_order_id(async_session: AsyncSession):
    """
    Tests that 'delete_service_order' in 'ServiceOrderRepository' deletes a service order from the database.
    """

    # Arrange
    repo = ServiceOrderRepository(db=async_session)

    service_order = ServiceOrderSchema(
        reservation_id=1,
        service_id=1,
        quantity=1,
        status="pending"
    )

    service_order = await repo.create_service_order(service_order=service_order)

    # Act
    await repo.delete_service_order(order_id=service_order.order_id)

    # Assert
    service_order = await repo.get_service_order_by_order_id(order_id=service_order.order_id)

    assert service_order is None, "Expected service order to be None"

@pytest.mark.asyncio
async def test_delete_all_service_orders_for_reservation(async_session: AsyncSession):
    """
    Tests that 'delete_service_orders_by_reservation_id' in 'ServiceOrderRepository' deletes all service orders for a reservation from the database.
    """

    # Arrange
    repo = ServiceOrderRepository(db=async_session)

    service_order = ServiceOrderSchema(
        reservation_id=2,
        service_id=1,
        quantity=1,
        status="pending"
    )

    service_order = await repo.create_service_order(service_order=service_order)

    service_order_2 = ServiceOrderSchema(
        reservation_id=2,
        service_id=2,
        quantity=1,
        status="pending"
    )

    service_order_2 = await repo.create_service_order(service_order=service_order_2)

    # Act
    await repo.delete_service_orders_by_reservation_id(reservation_id=service_order.reservation_id)

    # Assert
    service_orders = await repo.list_service_order_by_reservation_id(reservation_id=service_order.reservation_id)

    assert len(service_orders) == 0, "Expected no service orders to be returned"