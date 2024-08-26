from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db import async_session_maker


async def get_db() -> AsyncSession:
    """
    Provides a database session to be used within FastAPI endpoints.

    Yields:
        - AsyncSession: The SQLAlchemy async session object for database operations.
    """

    async with async_session_maker() as session:
        yield session
