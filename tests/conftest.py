import pytest

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine, AsyncConnection

from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from datetime import date

from app.main import app
from app.backend.db import Base, DATABASE_URL
from app.backend.db_depends import get_db
from app.models.user import User
from app.models.social_profile import SocialProfile
from app.routers.auth.utils import get_password_hash

test_engine = create_async_engine(DATABASE_URL)
test_async_session_maker = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope='session')
def anyio_backend() -> str:
    """
    Specifies the async backend to be used with pytest-anyio.
    """

    return 'asyncio'


@pytest.fixture(scope='session')
async def db_engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Sets up the asynchronous database engine for testing.
    """

    async with test_engine.begin() as conn:
        conn: AsyncConnection
        await conn.run_sync(Base.metadata.create_all)

    yield test_engine

    async with test_engine.begin() as conn:
        conn: AsyncConnection
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


@pytest.fixture(scope='function')
async def db_session(db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an asynchronous database session for each test.
    """

    async with test_async_session_maker() as session:
        yield session


@pytest.fixture(scope='function', autouse=True)
async def clear_tables(db_engine: AsyncEngine) -> None:
    """
    Clears all tables in the database while keeping their schemas after each test.
    """

    async with db_engine.begin() as conn:
        conn: AsyncConnection
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(delete(table))


@pytest.fixture(scope='function')
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Provides an asynchronous HTTP client for testing the FastAPI application.
    """

    app.dependency_overrides[get_db] = lambda: db_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client

    app.dependency_overrides.pop(get_db, None)


@pytest.fixture(scope='function')
async def test_user(db_session: AsyncSession) -> User:
    user = User(
        email='test@example.com',
        username='testuser',
        password=get_password_hash('Newpassword1!'),
        phone_number='+1234567890',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture(scope='function')
async def test_social_profiles(db_session: AsyncSession, test_user: User) -> list[SocialProfile]:
    profiles = [
        SocialProfile(
            user_id=test_user.id,
            platform='Twitter',
            profile_url='https://twitter.com/testuser',
            profile_type='personal'
        ),
        SocialProfile(
            user_id=test_user.id,
            platform='Facebook',
            profile_url='https://facebook.com/testuser',
            profile_type='business'
        )
    ]
    db_session.add_all(profiles)
    await db_session.commit()
    for profile in profiles:
        await db_session.refresh(profile)
    return profiles


@pytest.fixture(scope='function')
async def test_social_profile(db_session: AsyncSession, test_user: User) -> SocialProfile:
    profile = SocialProfile(
        user_id=test_user.id,
        platform='Instagram',
        profile_url='https://instagram.com/testuser',
        profile_type='personal'
    )
    db_session.add(profile)
    await db_session.commit()
    await db_session.refresh(profile)
    return profile
