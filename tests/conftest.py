import asyncio
import pytest
import pytest_asyncio 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@localhost:5432/agentdb"

@pytest_asyncio.fixture(scope="function")
async def async_session():
    """
    Provide an async SQLAlchemy session for database tests,
    using an async fixture so it yields a real AsyncSession object.
    """
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session_factory = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )
    try:
        # Create a session and yield it
        async with async_session_factory() as session:
            yield session
    finally:
        # Dispose of the engine to close all connections
        await engine.dispose()