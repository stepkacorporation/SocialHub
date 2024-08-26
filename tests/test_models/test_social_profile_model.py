import pytest

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.social_profile import SocialProfile

pytestmark = pytest.mark.anyio


async def test_create_social_profile_successfully(db_session: AsyncSession, test_user: User):
    social_profile = SocialProfile(
        platform='Telegram',
        profile_url='https://t.me/testuser',
        profile_type='personal',
        owner=test_user
    )
    db_session.add(social_profile)
    await db_session.commit()

    assert social_profile.id is not None
    assert social_profile.platform == 'Telegram'
    assert social_profile.profile_url == 'https://t.me/testuser'
    assert social_profile.profile_type == 'personal'
    assert social_profile.user_id == test_user.id


async def test_create_social_profile_without_user_id(db_session: AsyncSession):
    social_profile = SocialProfile(
        platform='Telegram',
        profile_url='https://t.me/testuser',
        profile_type='personal'
    )
    db_session.add(social_profile)
    with pytest.raises(IntegrityError):
        await db_session.commit()


async def test_create_social_profile_without_required_fields(db_session: AsyncSession, test_user: User):
    social_profile = SocialProfile(
        owner=test_user,
        platform=None,
        profile_url=None,
        profile_type=None
    )
    db_session.add(social_profile)
    with pytest.raises(IntegrityError):
        await db_session.commit()


async def test_update_social_profile_platform(db_session: AsyncSession, test_user: User):
    social_profile = SocialProfile(
        owner=test_user,
        platform='Telegram',
        profile_url='https://t.me/testuser',
        profile_type='personal'
    )
    db_session.add(social_profile)
    await db_session.commit()

    social_profile.platform = 'Instagram'
    await db_session.commit()

    updated_profile = await db_session.get(SocialProfile, social_profile.id)
    assert updated_profile.platform == 'Instagram'


async def test_update_social_profile_url(db_session: AsyncSession, test_user: User):
    social_profile = SocialProfile(
        owner=test_user,
        platform='Telegram',
        profile_url='https://t.me/testuser',
        profile_type='personal'
    )
    db_session.add(social_profile)
    await db_session.commit()

    social_profile.profile_url = 'https://instagram.com/testuser'
    await db_session.commit()

    updated_profile = await db_session.get(SocialProfile, social_profile.id)
    assert updated_profile.profile_url == 'https://instagram.com/testuser'


async def test_update_social_profile_type(db_session: AsyncSession, test_user: User):
    social_profile = SocialProfile(
        owner=test_user,
        platform='Telegram',
        profile_url='https://t.me/testuser',
        profile_type='personal'
    )
    db_session.add(social_profile)
    await db_session.commit()

    social_profile.profile_type = 'business'
    await db_session.commit()

    updated_profile = await db_session.get(SocialProfile, social_profile.id)
    assert updated_profile.profile_type == 'business'


async def test_delete_social_profile_successfully(db_session: AsyncSession, test_user: User):
    social_profile = SocialProfile(
        owner=test_user,
        platform='Telegram',
        profile_url='https://t.me/testuser',
        profile_type='personal'
    )
    db_session.add(social_profile)
    await db_session.commit()

    await db_session.delete(social_profile)
    await db_session.commit()

    deleted_profile = await db_session.get(SocialProfile, social_profile.id)
    assert deleted_profile is None


async def test_social_profile_relationship_with_user(db_session: AsyncSession, test_user: User):
    social_profile = SocialProfile(
        owner=test_user,
        platform='Telegram',
        profile_url='https://t.me/testuser',
        profile_type='personal'
    )
    db_session.add(social_profile)
    await db_session.commit()

    retrieved_profile = await db_session.get(SocialProfile, social_profile.id)
    assert retrieved_profile.owner == test_user
    assert retrieved_profile.user_id == test_user.id


async def test_create_social_profile_with_invalid_user_id(db_session: AsyncSession):
    social_profile = SocialProfile(
        user_id=99999,
        platform='Telegram',
        profile_url='https://t.me/testuser',
        profile_type='personal'
    )
    db_session.add(social_profile)
    with pytest.raises(IntegrityError):
        await db_session.commit()


async def test_create_multiple_social_profiles_for_user(db_session: AsyncSession, test_user: User):
    social_profile1 = SocialProfile(
        owner=test_user,
        platform='Telegram',
        profile_url='https://t.me/testuser',
        profile_type='personal'
    )
    social_profile2 = SocialProfile(
        owner=test_user,
        platform='Instagram',
        profile_url='https://instagram.com/testuser',
        profile_type='business'
    )
    db_session.add_all([social_profile1, social_profile2])
    await db_session.commit()

    retrieved_user = await db_session.scalar(
        select(User)
        .options(selectinload(User.social_profiles))
        .where(User.id == test_user.id)
    )

    assert len(retrieved_user.social_profiles) == 2
    assert retrieved_user.social_profiles[0].platform == 'Telegram'
    assert retrieved_user.social_profiles[1].platform == 'Instagram'
    assert retrieved_user.social_profiles[0].profile_url == 'https://t.me/testuser'
    assert retrieved_user.social_profiles[1].profile_url == 'https://instagram.com/testuser'
    assert retrieved_user.social_profiles[0].profile_type == 'personal'
    assert retrieved_user.social_profiles[1].profile_type == 'business'
    assert retrieved_user.social_profiles[0].user_id == test_user.id
    assert retrieved_user.social_profiles[1].user_id == test_user.id
