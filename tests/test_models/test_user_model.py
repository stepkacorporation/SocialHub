import pytest

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import date

from app.models.user import User
from app.models.social_profile import SocialProfile

pytestmark = pytest.mark.anyio


async def test_create_user_successfully(db_session: AsyncSession):
    user = User(
        email='test@example.com',
        username='testuser',
        password='hashedpassword',
        phone_number='+1234567890',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user)
    await db_session.commit()

    assert user.id is not None
    assert user.email == 'test@example.com'
    assert user.username == 'testuser'
    assert user.phone_number == '+1234567890'


async def test_create_user_with_duplicate_email(db_session: AsyncSession):
    user1 = User(
        email='test@example.com',
        username='user1',
        password='password1',
        phone_number='+1234567890',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user1)
    await db_session.commit()

    user2 = User(
        email='test@example.com',
        username='user2',
        password='password2',
        phone_number='+0987654321',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        await db_session.commit()


async def test_create_user_with_duplicate_username(db_session: AsyncSession):
    user1 = User(
        email='user1@example.com',
        username='user',
        password='password1',
        phone_number='+1234567890',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user1)
    await db_session.commit()

    user2 = User(
        email='user2@example.com',
        username='user',
        password='password2',
        phone_number='+0987654321',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        await db_session.commit()


async def test_create_user_with_duplicate_phone_number(db_session: AsyncSession):
    user1 = User(
        email='user1@example.com',
        username='user1',
        password='password1',
        phone_number='+1234567890',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user1)
    await db_session.commit()

    user2 = User(
        email='user2@example.com',
        username='user2',
        password='password2',
        phone_number='+1234567890',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        await db_session.commit()


async def test_create_user_without_required_fields(db_session: AsyncSession):
    user = User(
        email=None,
        username=None,
        password=None,
        phone_number=None,
        date_of_birth=None
    )
    db_session.add(user)
    with pytest.raises(IntegrityError):
        await db_session.commit()


async def test_update_user_email(db_session: AsyncSession):
    user = User(
        email='old@example.com',
        username='testuser',
        password='hashedpassword',
        phone_number='+1234567890',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user)
    await db_session.commit()

    user.email = 'new@example.com'
    await db_session.commit()

    updated_user = await db_session.get(User, user.id)
    assert updated_user.email == 'new@example.com'


async def test_update_user_with_duplicate_email(db_session: AsyncSession):
    user1 = User(
        email='unique1@example.com',
        username='user1',
        password='password1',
        phone_number='+1234567890',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user1)
    await db_session.commit()

    user2 = User(
        email='unique2@example.com',
        username='user2',
        password='password2',
        phone_number='+0987654321',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user2)
    await db_session.commit()

    user2.email = 'unique1@example.com'
    with pytest.raises(IntegrityError):
        await db_session.commit()


async def test_update_user_username(db_session: AsyncSession):
    user = User(
        email='user@example.com',
        username='oldusername',
        password='hashedpassword',
        phone_number='+1234567890',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user)
    await db_session.commit()

    user.username = 'newusername'
    await db_session.commit()

    updated_user = await db_session.get(User, user.id)
    assert updated_user.username == 'newusername'


async def test_update_user_with_duplicate_username(db_session: AsyncSession):
    user1 = User(
        email='user1@example.com',
        username='user1',
        password='password1',
        phone_number='+1234567890',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user1)
    await db_session.commit()

    user2 = User(
        email='user2@example.com',
        username='user2',
        password='password2',
        phone_number='+0987654321',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user2)
    await db_session.commit()

    user2.username = 'user1'
    with pytest.raises(IntegrityError):
        await db_session.commit()


async def test_update_user_phone_number(db_session: AsyncSession):
    user = User(
        email='user@example.com',
        username='username',
        password='hashedpassword',
        phone_number='+1234567890',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user)
    await db_session.commit()

    user.phone_number = '+0987654321'
    await db_session.commit()

    updated_user = await db_session.get(User, user.id)
    assert updated_user.phone_number == '+0987654321'


async def test_update_user_with_duplicate_phone_number(db_session: AsyncSession):
    user1 = User(
        email='user1@example.com',
        username='user1',
        password='password1',
        phone_number='+1234567890',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user1)
    await db_session.commit()

    user2 = User(
        email='user2@example.com',
        username='user2',
        password='password2',
        phone_number='+0987654321',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user2)
    await db_session.commit()

    user2.phone_number = '+1234567890'
    with pytest.raises(IntegrityError):
        await db_session.commit()


async def test_delete_user_successfully(db_session: AsyncSession):
    user = User(
        email='user@example.com',
        username='user',
        password='password',
        phone_number='+1234567890',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user)
    await db_session.commit()

    await db_session.delete(user)
    await db_session.commit()

    deleted_user = await db_session.get(User, user.id)
    assert deleted_user is None


async def test_user_relationship_with_social_profiles(db_session: AsyncSession):
    user = User(
        email='user@example.com',
        username='user',
        password='password',
        phone_number='+1234567890',
        date_of_birth=date(1990, 1, 1)
    )
    db_session.add(user)
    await db_session.commit()

    social_profile = SocialProfile(
        platform='Telegram',
        profile_url='https://t.me/testuser',
        profile_type='personal',
        owner=user
    )
    db_session.add(social_profile)
    await db_session.commit()

    retrieved_user = await db_session.scalar(
        select(User)
        .options(selectinload(User.social_profiles))
        .where(User.id == user.id)
    )

    assert len(retrieved_user.social_profiles) == 1
    assert retrieved_user.social_profiles[0].platform == 'Telegram'
    assert retrieved_user.social_profiles[0].profile_url == 'https://t.me/testuser'
    assert retrieved_user.social_profiles[0].profile_type == 'personal'
    assert retrieved_user.social_profiles[0].user_id == user.id
