import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends

DATABASE_URL = os.getenv("POSTGRES_CONNECTION_STRING", "postgresql+asyncpg://myuser:mypassword@localhost:5432/agentdb")

engine = create_async_engine(
    DATABASE_URL,
    echo=True,         
    pool_size=5,       
    max_overflow=10
)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an AsyncSession.
    Yields the session, ensuring that it is closed after use.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            # The session context manager handles rollback/close if needed
            await session.close()
